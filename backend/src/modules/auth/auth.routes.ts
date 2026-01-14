import { Router } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { AppDataSource } from '../../infra/data-source';
import { User } from '../users/user.entity';

export const authRouter = Router();

const userRepo = () => AppDataSource.getRepository(User);

authRouter.post('/register', async (req, res) => {
  try {
    const { email, phone, password, name } = req.body as {
      email?: string;
      phone?: string;
      password: string;
      name?: string;
    };

    if (!password || (!email && !phone)) {
      return res.status(400).json({ message: 'Email yoki telefon va parol kerak' });
    }

    const repo = userRepo();

    if (email) {
      const existing = await repo.findOne({ where: { email } });
      if (existing) {
        return res.status(409).json({ message: 'Bu email allaqachon ro\'yxatdan o\'tgan' });
      }
    }

    if (phone) {
      const existingPhone = await repo.findOne({ where: { phone } });
      if (existingPhone) {
        return res.status(409).json({ message: 'Bu telefon allaqachon ro\'yxatdan o\'tgan' });
      }
    }

    const passwordHash = await bcrypt.hash(password, 10);

    const user = repo.create({
      email: email ?? null,
      phone: phone ?? null,
      passwordHash,
      name: name ?? '',
    });

    await repo.save(user);

    const token = createAccessToken(user.id);

    return res.status(201).json({
      user: {
        id: user.id,
        email: user.email,
        phone: user.phone,
        name: user.name,
      },
      token,
    });
  } catch (e) {
    // eslint-disable-next-line no-console
    console.error(e);
    return res.status(500).json({ message: 'Server xatosi' });
  }
});

authRouter.post('/login', async (req, res) => {
  try {
    const { email, phone, password } = req.body as {
      email?: string;
      phone?: string;
      password: string;
    };

    if (!password || (!email && !phone)) {
      return res.status(400).json({ message: 'Email yoki telefon va parol kerak' });
    }

    const repo = userRepo();

    const user = await repo.findOne({
      where: email ? { email } : { phone },
    });

    if (!user) {
      return res.status(401).json({ message: 'Noto\'g\'ri ma\'lumotlar' });
    }

    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) {
      return res.status(401).json({ message: 'Noto\'g\'ri ma\'lumotlar' });
    }

    const token = createAccessToken(user.id);

    return res.json({
      user: {
        id: user.id,
        email: user.email,
        phone: user.phone,
        name: user.name,
      },
      token,
    });
  } catch (e) {
    // eslint-disable-next-line no-console
    console.error(e);
    return res.status(500).json({ message: 'Server xatosi' });
  }
});

function createAccessToken(userId: string): string {
  const secret = process.env.JWT_SECRET || 'dev-secret';
  return jwt.sign({ sub: userId }, secret, { expiresIn: '7d' });
}


