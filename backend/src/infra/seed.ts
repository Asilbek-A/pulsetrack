import bcrypt from 'bcryptjs';
import { AppDataSource } from './data-source';
import { User } from '../modules/users/user.entity';

export async function seedDefaultUser(): Promise<void> {
  const userRepo = AppDataSource.getRepository(User);

  const existingUser = await userRepo.findOne({
    where: { email: 'admin@pulsetrack.com' },
  });

  if (existingUser) {
    console.log('Default admin user already exists, skipping seed.');
    return;
  }

  const passwordHash = await bcrypt.hash('Admin123!', 10);

  const adminUser = userRepo.create({
    email: 'admin@pulsetrack.com',
    name: 'Admin User',
    passwordHash,
    gender: 'OTHER',
    heightCm: 175,
    weightKg: 70,
  });

  await userRepo.save(adminUser);
  console.log('Default admin user created: admin@pulsetrack.com / Admin123!');
}

