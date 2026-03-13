import {
  Column,
  CreateDateColumn,
  Entity,
  ManyToOne,
  PrimaryGeneratedColumn,
} from 'typeorm';
import { User } from '../users/user.entity';

@Entity({ name: 'health_metrics' })
export class HealthMetric {
  @PrimaryGeneratedColumn('uuid')
  id!: string;

  @ManyToOne(() => User, { eager: true })
  user!: User;

  @Column({ type: 'timestamptz' })
  timestamp!: Date;

  @Column({ type: 'int', nullable: true })
  restingHR!: number | null;

  @Column({ type: 'int', nullable: true })
  hrv!: number | null;

  @Column({ type: 'float', nullable: true })
  respRate!: number | null;

  @Column({ type: 'float', nullable: true })
  skinTempDiff!: number | null;

  @CreateDateColumn()
  createdAt!: Date;
}


