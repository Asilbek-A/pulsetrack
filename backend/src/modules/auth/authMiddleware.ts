import { NextFunction, Request, Response } from 'express';
import jwt from 'jsonwebtoken';

export interface AuthRequest extends Request {
  userId?: string;
}

export function authMiddleware(
  req: AuthRequest,
  res: Response,
  next: NextFunction,
) {
  const header = req.headers.authorization;
  if (!header) {
    return res.status(401).json({ message: 'Token kerak' });
  }

  const [, token] = header.split(' ');

  if (!token) {
    return res.status(401).json({ message: 'Token noto\'g\'ri' });
  }

  try {
    const secret = process.env.JWT_SECRET || 'dev-secret';
    const payload = jwt.verify(token, secret) as { sub: string };
    req.userId = payload.sub;
    return next();
  } catch (e) {
    return res.status(401).json({ message: 'Token yaroqsiz' });
  }
}


