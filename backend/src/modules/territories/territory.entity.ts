import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
  Index,
} from 'typeorm';
import { User } from '../users/user.entity';

@Entity('territories')
@Index(['lat', 'lng'])
@Index(['userId'])
export class Territory {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @Column({ name: 'user_id' })
  userId: string;

  // Grid cell coordinates (simplified territory system)
  // Each cell is approximately 100m x 100m
  @Column({ type: 'float' })
  lat: number;

  @Column({ type: 'float' })
  lng: number;

  // Grid cell ID (for faster lookups)
  @Column({ name: 'cell_id', type: 'varchar' })
  cellId: string;

  // User's territory color (stored as string to handle large color values)
  @Column({ type: 'varchar' })
  color: string;

  @Column({ name: 'color_name', type: 'varchar' })
  colorName: string;

  // Capture statistics
  @Column({ name: 'capture_count', type: 'int', default: 1 })
  captureCount: number;

  @Column({ name: 'total_distance', type: 'float', default: 0 })
  totalDistance: number;

  @Column({ name: 'total_time_seconds', type: 'int', default: 0 })
  totalTimeSeconds: number;

  // Last captured workout details
  @Column({ name: 'last_workout_id', type: 'uuid', nullable: true })
  lastWorkoutId: string | null;

  @Column({ name: 'last_captured_at', type: 'timestamp' })
  lastCapturedAt: Date;

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;
}

@Entity('workout_routes')
export class WorkoutRoute {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ name: 'user_id' })
  userId: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'user_id' })
  user: User;

  // Workout details
  @Column({ name: 'workout_type', type: 'varchar' })
  workoutType: string;

  @Column({ type: 'float' })
  distance: number;

  @Column({ name: 'duration_seconds', type: 'int' })
  durationSeconds: number;

  @Column({ name: 'avg_speed', type: 'float' })
  avgSpeed: number;

  // Territory stats
  @Column({ name: 'territories_captured', type: 'int', default: 0 })
  territoriesCaptured: number;

  @Column({ name: 'territories_lost', type: 'int', default: 0 })
  territoriesLost: number;

  @Column({ name: 'new_territory_area', type: 'float', default: 0 })
  newTerritoryArea: number;

  // Route data (array of GPS coordinates)
  @Column({ type: 'jsonb' })
  route: Array<{ lat: number; lng: number; timestamp: string }>;

  // Captured territory cells
  @Column({ name: 'captured_cells', type: 'jsonb', nullable: true })
  capturedCells: Array<string> | null;

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;
}

