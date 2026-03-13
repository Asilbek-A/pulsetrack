import { Router, Request, Response } from 'express';
import { AppDataSource } from '../../infra/data-source';
import { Territory, WorkoutRoute } from './territory.entity';
import { authMiddleware } from '../auth/authMiddleware';

const router = Router();

// Get territories in a bounding box
router.get('/map', authMiddleware, async (req: Request, res: Response) => {
  try {
    const { minLat, maxLat, minLng, maxLng } = req.query;

    if (!minLat || !maxLat || !minLng || !maxLng) {
      return res.status(400).json({ message: 'Bounding box parameters required' });
    }

    const territoryRepo = AppDataSource.getRepository(Territory);

    const territories = await territoryRepo
      .createQueryBuilder('territory')
      .leftJoinAndSelect('territory.user', 'user')
      .where('territory.lat BETWEEN :minLat AND :maxLat', {
        minLat: Number(minLat),
        maxLat: Number(maxLat),
      })
      .andWhere('territory.lng BETWEEN :minLng AND :maxLng', {
        minLng: Number(minLng),
        maxLng: Number(maxLng),
      })
      .getMany();

    res.json(territories);
  } catch (error) {
    console.error('Get territories error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get user's territories
router.get('/my', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const territoryRepo = AppDataSource.getRepository(Territory);

    const territories = await territoryRepo.find({
      where: { userId },
      order: { lastCapturedAt: 'DESC' },
    });

    const stats = {
      totalCells: territories.length,
      totalDistance: territories.reduce((sum, t) => sum + t.totalDistance, 0),
      totalTime: territories.reduce((sum, t) => sum + t.totalTimeSeconds, 0),
      mostCaptured: territories.sort((a, b) => b.captureCount - a.captureCount)[0] || null,
    };

    res.json({ territories, stats });
  } catch (error) {
    console.error('Get my territories error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Save workout route and capture territories
router.post('/workout', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const {
      workoutType,
      distance,
      durationSeconds,
      avgSpeed,
      route,
      color,
      colorName,
    } = req.body;

    if (!route || !Array.isArray(route) || route.length === 0) {
      return res.status(400).json({ message: 'Route data required' });
    }

    // Convert color to string to handle large color values
    const colorStr = String(color);

    const territoryRepo = AppDataSource.getRepository(Territory);
    const routeRepo = AppDataSource.getRepository(WorkoutRoute);

    // Calculate grid cells from route
    const capturedCells = new Set<string>();
    const cellSize = 0.001; // Approximately 100m at equator

    route.forEach((point: { lat: number; lng: number }) => {
      const cellLat = Math.floor(point.lat / cellSize) * cellSize;
      const cellLng = Math.floor(point.lng / cellSize) * cellSize;
      const cellId = `${cellLat.toFixed(6)},${cellLng.toFixed(6)}`;
      capturedCells.add(cellId);
    });

    // Process each captured cell
    let newCells = 0;
    let takenCells = 0;

    for (const cellId of capturedCells) {
      const [lat, lng] = cellId.split(',').map(Number);

      // Check if cell already exists
      const existing = await territoryRepo.findOne({
        where: { cellId },
      });

      if (existing) {
        if (existing.userId !== userId) {
          // Take over from another user
          existing.userId = userId;
          existing.color = colorStr;
          existing.colorName = colorName;
          existing.captureCount += 1;
          existing.lastCapturedAt = new Date();
          await territoryRepo.save(existing);
          takenCells++;
        } else {
          // Already owned by this user, just update
          existing.captureCount += 1;
          existing.totalDistance += distance / capturedCells.size;
          existing.totalTimeSeconds += durationSeconds / capturedCells.size;
          existing.lastCapturedAt = new Date();
          await territoryRepo.save(existing);
        }
      } else {
        // New territory
        const territory = territoryRepo.create({
          userId,
          lat,
          lng,
          cellId,
          color: colorStr,
          colorName,
          captureCount: 1,
          totalDistance: distance / capturedCells.size,
          totalTimeSeconds: durationSeconds / capturedCells.size,
          lastCapturedAt: new Date(),
        });
        await territoryRepo.save(territory);
        newCells++;
      }
    }

    // Save workout route
    const workoutRoute = routeRepo.create({
      userId,
      workoutType,
      distance,
      durationSeconds,
      avgSpeed,
      route,
      territoriesCaptured: newCells,
      territoriesLost: 0, // TODO: Track if user lost territories
      newTerritoryArea: newCells * cellSize * cellSize * 111320 * 111320, // Convert to m²
      capturedCells: Array.from(capturedCells),
    });

    await routeRepo.save(workoutRoute);

    res.status(201).json({
      message: 'Workout saved',
      workoutId: workoutRoute.id,
      stats: {
        totalCells: capturedCells.size,
        newCells,
        takenCells,
        area: newCells * cellSize * cellSize * 111320 * 111320,
      },
    });
  } catch (error) {
    console.error('Save workout error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get workout routes
router.get('/workouts', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const { limit = '10' } = req.query;

    const routeRepo = AppDataSource.getRepository(WorkoutRoute);

    const routes = await routeRepo.find({
      where: { userId },
      order: { createdAt: 'DESC' },
      take: Number(limit),
    });

    res.json(routes);
  } catch (error) {
    console.error('Get workouts error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get leaderboard (most territories)
router.get('/leaderboard', authMiddleware, async (req: Request, res: Response) => {
  try {
    const territoryRepo = AppDataSource.getRepository(Territory);

    const leaderboard = await territoryRepo
      .createQueryBuilder('territory')
      .select('territory.userId', 'userId')
      .addSelect('user.firstName', 'firstName')
      .addSelect('user.lastName', 'lastName')
      .addSelect('territory.colorName', 'colorName')
      .addSelect('COUNT(territory.id)', 'territoryCount')
      .addSelect('SUM(territory.totalDistance)', 'totalDistance')
      .leftJoin('territory.user', 'user')
      .groupBy('territory.userId')
      .addGroupBy('user.firstName')
      .addGroupBy('user.lastName')
      .addGroupBy('territory.colorName')
      .orderBy('territoryCount', 'DESC')
      .limit(100)
      .getRawMany();

    res.json(leaderboard);
  } catch (error) {
    console.error('Get leaderboard error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

export default router;

