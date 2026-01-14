import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
  OneToMany,
} from 'typeorm';
import { User } from '../users/user.entity';

export enum PostPrivacy {
  PUBLIC_ALL = 'public_all',      // Barcha foydalanuvchilarga
  COMMUNITY = 'community',         // Faqat community
  PRIVATE = 'private',             // Faqat o'zimda
}

export enum PostType {
  WORKOUT = 'workout',
  ACHIEVEMENT = 'achievement',
  STATUS = 'status',
}

@Entity('posts')
export class Post {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @Column({ name: 'user_id' })
  userId: string;

  @Column({ type: 'enum', enum: PostType, default: PostType.WORKOUT })
  type: PostType;

  @Column({ type: 'enum', enum: PostPrivacy, default: PostPrivacy.PRIVATE })
  privacy: PostPrivacy;

  @Column({ type: 'text', nullable: true })
  content: string | null;

  // Workout specific data
  @Column({ name: 'workout_type', type: 'varchar', nullable: true })
  workoutType: string | null;

  @Column({ type: 'float', nullable: true })
  distance: number | null;

  @Column({ name: 'duration_seconds', type: 'int', nullable: true })
  durationSeconds: number | null;

  @Column({ name: 'avg_heart_rate', type: 'int', nullable: true })
  avgHeartRate: number | null;

  @Column({ name: 'max_heart_rate', type: 'int', nullable: true })
  maxHeartRate: number | null;

  @Column({ type: 'float', nullable: true })
  calories: number | null;

  @Column({ type: 'float', nullable: true })
  strain: number | null;

  @Column({ name: 'avg_speed', type: 'float', nullable: true })
  avgSpeed: number | null;

  @Column({ name: 'elevation_gain', type: 'float', nullable: true })
  elevationGain: number | null;

  // Route data (GPS coordinates as JSON)
  @Column({ type: 'jsonb', nullable: true })
  route: any | null;

  // Map image/screenshot URL
  @Column({ name: 'map_image_url', type: 'varchar', nullable: true })
  mapImageUrl: string | null;

  // Engagement
  @Column({ name: 'likes_count', type: 'int', default: 0 })
  likesCount: number;

  @Column({ name: 'comments_count', type: 'int', default: 0 })
  commentsCount: number;

  @OneToMany(() => PostLike, (like) => like.post)
  likes: PostLike[];

  @OneToMany(() => PostComment, (comment) => comment.post)
  comments: PostComment[];

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;
}

@Entity('post_likes')
export class PostLike {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => Post, (post) => post.likes, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'post_id' })
  post: Post;

  @Column({ name: 'post_id' })
  postId: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @Column({ name: 'user_id' })
  userId: string;

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;
}

@Entity('post_comments')
export class PostComment {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => Post, (post) => post.comments, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'post_id' })
  post: Post;

  @Column({ name: 'post_id' })
  postId: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @Column({ name: 'user_id' })
  userId: string;

  @Column({ type: 'text' })
  content: string;

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;
}

