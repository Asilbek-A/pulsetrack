import 'reflect-metadata';
import { DataSource } from 'typeorm';
import { User } from '../modules/users/user.entity';
import { HealthMetric } from '../modules/metrics/health-metric.entity';
import { Post, PostLike, PostComment } from '../modules/posts/post.entity';
import { Territory, WorkoutRoute } from '../modules/territories/territory.entity';

/**
 * Supabase Database Configuration
 * 
 * Supabase connection string format:
 * postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
 * 
 * Environment variables:
 * - DB_HOST: db.[PROJECT-REF].supabase.co
 * - DB_PORT: 5432
 * - DB_USER: postgres
 * - DB_PASSWORD: [YOUR-SUPABASE-PASSWORD]
 * - DB_NAME: postgres
 * - DB_SSL: true
 */
export const AppDataSource = new DataSource({
  type: 'postgres',
  host: process.env.DB_HOST || 'localhost',
  port: Number(process.env.DB_PORT || 5432),
  username: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
  database: process.env.DB_NAME || 'postgres',
  // SSL required for Supabase
  ssl: process.env.DB_SSL === 'true' ? { rejectUnauthorized: false } : false,
  // CRITICAL: synchronize only in development, NEVER in production
  synchronize: process.env.NODE_ENV !== 'production',
  // Enable logging in development for debugging
  logging: process.env.NODE_ENV === 'development',
  entities: [User, HealthMetric, Post, PostLike, PostComment, Territory, WorkoutRoute],
  // In production, use migrations instead of synchronize
  // migrations: process.env.NODE_ENV === 'production' ? ['dist/migrations/*.js'] : [],
});
