import { Router } from 'express';
import { AppDataSource } from '../../infra/data-source';
import { HealthMetric } from './health-metric.entity';
import { authMiddleware, AuthRequest } from '../auth/authMiddleware';
import { User } from '../users/user.entity';

export const metricsRouter = Router();

const metricRepo = () => AppDataSource.getRepository(HealthMetric);
const userRepo = () => AppDataSource.getRepository(User);

metricsRouter.post(
  '/health/batch',
  authMiddleware,
  async (req: AuthRequest, res) => {
    const userId = req.userId!;
    const repo = metricRepo();
    const uRepo = userRepo();

    const user = await uRepo.findOne({ where: { id: userId } });
    if (!user) {
      return res.status(404).json({ message: 'Foydalanuvchi topilmadi' });
    }

    const items = req.body.items as Array<{
      timestamp: string;
      restingHR?: number;
      hrv?: number;
      respRate?: number;
      skinTempDiff?: number;
    }>;

    if (!Array.isArray(items) || items.length === 0) {
      return res.status(400).json({ message: 'items bo\'sh bo\'lmasligi kerak' });
    }

    const entities = items.map((i) =>
      repo.create({
        user,
        timestamp: new Date(i.timestamp),
        restingHR: i.restingHR ?? null,
        hrv: i.hrv ?? null,
        respRate: i.respRate ?? null,
        skinTempDiff: i.skinTempDiff ?? null,
      }),
    );

    await repo.save(entities);

    return res.status(201).json({ inserted: entities.length });
  },
);

metricsRouter.get(
  '/health',
  authMiddleware,
  async (req: AuthRequest, res) => {
    const userId = req.userId!;
    const { from, to } = req.query as { from?: string; to?: string };

    const repo = metricRepo();

    const qb = repo
      .createQueryBuilder('m')
      .leftJoin('m.user', 'user')
      .where('user.id = :userId', { userId })
      .orderBy('m.timestamp', 'ASC');

    if (from) {
      qb.andWhere('m.timestamp >= :from', { from });
    }

    if (to) {
      qb.andWhere('m.timestamp <= :to', { to });
    }

    const list = await qb.getMany();

    return res.json(
      list.map((m) => ({
        id: m.id,
        timestamp: m.timestamp,
        restingHR: m.restingHR,
        hrv: m.hrv,
        respRate: m.respRate,
        skinTempDiff: m.skinTempDiff,
      })),
    );
  },
);

// Get daily summary for a specific date
metricsRouter.get(
  '/daily-summary',
  authMiddleware,
  async (req: AuthRequest, res) => {
    const userId = req.userId!;
    const { date } = req.query as { date?: string };

    if (!date) {
      return res.status(400).json({ message: 'date parametri kerak' });
    }

    try {
      const targetDate = new Date(date);
      const startOfDay = new Date(targetDate);
      startOfDay.setHours(0, 0, 0, 0);
      const endOfDay = new Date(targetDate);
      endOfDay.setHours(23, 59, 59, 999);

      // Get daily summary from posts (workout data)
      const { Post } = await import('../posts/post.entity');
      const postRepo = AppDataSource.getRepository(Post);

      const posts = await postRepo
        .createQueryBuilder('post')
        .where('post.userId = :userId', { userId })
        .andWhere('post.createdAt >= :startOfDay', { startOfDay })
        .andWhere('post.createdAt <= :endOfDay', { endOfDay })
        .orderBy('post.createdAt', 'DESC')
        .getMany();

      // Calculate aggregated metrics from posts
      let totalDistance = 0;
      let totalCalories = 0;
      let totalStrain = 0;
      let totalDuration = 0;
      let avgHR = 0;
      let maxHR = 0;
      let hrSum = 0;
      let hrCount = 0;

      for (const post of posts) {
        if (post.distance) totalDistance += post.distance;
        if (post.calories) totalCalories += post.calories;
        if (post.strain) totalStrain += post.strain;
        if (post.durationSeconds) totalDuration += post.durationSeconds;
        if (post.avgHeartRate) {
          hrSum += post.avgHeartRate;
          hrCount++;
        }
        if (post.maxHeartRate && post.maxHeartRate > maxHR) {
          maxHR = post.maxHeartRate;
        }
      }

      if (hrCount > 0) {
        avgHR = Math.round(hrSum / hrCount);
      }

      // Get health metrics for the day
      const repo = metricRepo();
      const healthMetrics = await repo
        .createQueryBuilder('m')
        .leftJoin('m.user', 'user')
        .where('user.id = :userId', { userId })
        .andWhere('m.timestamp >= :startOfDay', { startOfDay })
        .andWhere('m.timestamp <= :endOfDay', { endOfDay })
        .orderBy('m.timestamp', 'ASC')
        .getMany();

      // Calculate averages from health metrics
      let avgHRV = 0;
      let avgRespRate = 0;
      let avgTemp = 0;
      let restingHR = 0;
      let hrvSum = 0;
      let hrvCount = 0;
      let respSum = 0;
      let respCount = 0;
      let tempSum = 0;
      let tempCount = 0;
      let restingHRSum = 0;
      let restingHRCount = 0;

      for (const metric of healthMetrics) {
        if (metric.hrv != null) {
          hrvSum += metric.hrv;
          hrvCount++;
        }
        if (metric.respRate != null) {
          respSum += metric.respRate;
          respCount++;
        }
        if (metric.skinTempDiff != null) {
          tempSum += metric.skinTempDiff;
          tempCount++;
        }
        if (metric.restingHR != null) {
          restingHRSum += metric.restingHR;
          restingHRCount++;
        }
      }

      if (hrvCount > 0) avgHRV = hrvSum / hrvCount;
      if (respCount > 0) avgRespRate = respSum / respCount;
      if (tempCount > 0) avgTemp = tempSum / tempCount;
      if (restingHRCount > 0) restingHR = Math.round(restingHRSum / restingHRCount);

      // Estimate recovery and sleep scores (simplified)
      // In real app, these would be calculated from HRV, sleep data, etc.
      const recoveryScore = avgHRV > 0 ? Math.min(100, Math.round(50 + (avgHRV / 10))) : 50;
      const sleepScore = posts.length > 0 ? 85 : 0; // Simplified

      return res.json({
        date: targetDate.toISOString().split('T')[0],
        recoveryScore,
        strainScore: totalStrain,
        sleepScore,
        avgHR,
        restingHR,
        maxHR,
        avgHRV: Math.round(avgHRV * 10) / 10,
        steps: 0, // Would need to track separately
        distance: Math.round(totalDistance * 100) / 100,
        calories: Math.round(totalCalories * 100) / 100,
        activeMinutes: Math.round(totalDuration / 60),
        avgRespiratoryRate: Math.round(avgRespRate * 10) / 10,
        avgTemperature: Math.round(avgTemp * 10) / 10,
        workoutsCount: posts.length,
      });
    } catch (error) {
      console.error('Error getting daily summary:', error);
      return res.status(500).json({ message: 'Xatolik yuz berdi' });
    }
  },
);


