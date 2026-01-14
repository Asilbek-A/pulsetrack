import 'reflect-metadata';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { AppDataSource } from './infra/data-source';
import { authRouter } from './modules/auth/auth.routes';
import { usersRouter } from './modules/users/users.routes';
import { metricsRouter } from './modules/metrics/metrics.routes';
import postsRouter from './modules/posts/posts.routes';
import territoriesRouter from './modules/territories/territories.routes';
import { seedDefaultUser } from './infra/seed';

dotenv.config();

const app = express();

app.use(helmet());
// CORS: Use environment variable for production, allow all in development
app.use(
  cors({
    origin: process.env.CORS_ORIGIN || '*',
    credentials: true,
  }),
);
app.use(express.json());

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', version: '1.0.0' });
});

app.use('/auth', authRouter);
app.use('/users', usersRouter);
app.use('/metrics', metricsRouter);
app.use('/posts', postsRouter);
app.use('/territories', territoriesRouter);

const PORT = process.env.PORT || 4000;

AppDataSource.initialize()
  .then(async () => {
    // Seed default admin user
    await seedDefaultUser();

    app.listen(Number(PORT), '0.0.0.0', () => {
      // eslint-disable-next-line no-console
      console.log(`API server listening on http://0.0.0.0:${PORT}`);
    });
  })
  .catch((err) => {
    // eslint-disable-next-line no-console
    console.error('Failed to initialize data source', err);
    process.exit(1);
  });


