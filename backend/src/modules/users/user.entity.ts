import {
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity({ name: 'users' })
export class User {
  @PrimaryGeneratedColumn('uuid')
  id!: string;

  @Column({ type: 'varchar', unique: true, nullable: true })
  email!: string | null;

  @Column({ type: 'varchar', unique: true, nullable: true })
  phone!: string | null;

  @Column()
  passwordHash!: string;

  @Column({ default: '' })
  name!: string;

  @Column({ type: 'varchar', length: 16, nullable: true })
  gender!: string | null;

  @Column({ type: 'date', nullable: true })
  birthDate!: string | null;

  @Column({ type: 'int', nullable: true })
  heightCm!: number | null;

  @Column({ type: 'float', nullable: true })
  weightKg!: number | null;

  @CreateDateColumn()
  createdAt!: Date;

  @UpdateDateColumn()
  updatedAt!: Date;
}


