import { Router } from 'express';
import { AppDataSource } from '../../infra/data-source';
import { User } from './user.entity';
import { authMiddleware, AuthRequest } from '../auth/authMiddleware';

export const usersRouter = Router();

const userRepo = () => AppDataSource.getRepository(User);

usersRouter.get('/me', authMiddleware, async (req: AuthRequest, res) => {
  const repo = userRepo();
  const user = await repo.findOne({ where: { id: req.userId } });

  if (!user) {
    return res.status(404).json({ message: 'Foydalanuvchi topilmadi' });
  }

  return res.json({
    id: user.id,
    email: user.email,
    phone: user.phone,
    name: user.name,
    gender: user.gender,
    birthDate: user.birthDate,
    heightCm: user.heightCm,
    weightKg: user.weightKg,
  });
});

usersRouter.put('/me', authMiddleware, async (req: AuthRequest, res) => {
  const repo = userRepo();
  const user = await repo.findOne({ where: { id: req.userId } });

  if (!user) {
    return res.status(404).json({ message: 'Foydalanuvchi topilmadi' });
  }

  const { name, gender, birthDate, heightCm, weightKg } = req.body as {
    name?: string;
    gender?: string;
    birthDate?: string;
    heightCm?: number;
    weightKg?: number;
  };

  if (name !== undefined) user.name = name;
  if (gender !== undefined) user.gender = gender;
  if (birthDate !== undefined) user.birthDate = birthDate;
  if (heightCm !== undefined) user.heightCm = heightCm;
  if (weightKg !== undefined) user.weightKg = weightKg;

  await repo.save(user);

  return res.json({ message: 'Yangilandi' });
});


