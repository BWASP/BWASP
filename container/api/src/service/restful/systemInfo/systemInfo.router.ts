import express, { Request, Response } from 'express';
import { asyncHandler } from '../../../infra/middleware/asyncHandler';
import systemInfoService from './index';

const router = express.Router();

// GET /api/systeminfo - List all system info
router.get('/', asyncHandler(async (req: Request, res: Response) => {
  const systemInfo = await systemInfoService.findAll();
  res.json({ data: systemInfo });
}));

// POST /api/systeminfo - Create system info
router.post('/', asyncHandler(async (req: Request, res: Response) => {
  const result = await systemInfoService.create(req.body);
  res.status(201).json({ data: result });
}));

// PATCH /api/systeminfo - Update system info
router.patch('/', asyncHandler(async (req: Request, res: Response) => {
  const result = await systemInfoService.update(req.body);
  res.json({ data: result });
}));

// GET /api/systeminfo/:id - Get specific system info
router.get('/:id', asyncHandler(async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  const systemInfo = await systemInfoService.findById(id);
  res.json({ data: systemInfo });
}));

export default router;
