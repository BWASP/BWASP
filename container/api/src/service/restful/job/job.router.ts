import express, { Request, Response } from 'express';
import { asyncHandler } from '../../../infra/middleware/asyncHandler';
import jobService from './index';

const router = express.Router();

// GET /api/job - List all jobs
router.get('/', asyncHandler(async (req: Request, res: Response) => {
  const jobs = await jobService.findAll();
  res.json({ data: jobs });
}));

// POST /api/job - Create job(s)
router.post('/', asyncHandler(async (req: Request, res: Response) => {
  const result = await jobService.create(req.body);
  res.status(201).json({ data: result });
}));

// PATCH /api/job - Update job(s) with done status
router.patch('/', asyncHandler(async (req: Request, res: Response) => {
  const result = await jobService.update(req.body);
  res.json({ data: result });
}));

// GET /api/job/:id - Get specific job
router.get('/:id', asyncHandler(async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  const job = await jobService.findById(id);
  res.json({ data: job });
}));

export default router;
