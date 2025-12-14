import express, { Request, Response } from 'express';
import { asyncHandler } from '../../../infra/middleware/asyncHandler';
import portsService from './index';

const router = express.Router();

// GET /api/ports - List all port scans
router.get('/', asyncHandler(async (req: Request, res: Response) => {
  const ports = await portsService.findAll();
  res.json({ data: ports });
}));

// POST /api/ports - Create port scan result(s)
router.post('/', asyncHandler(async (req: Request, res: Response) => {
  const result = await portsService.create(req.body);
  res.status(201).json({ data: result });
}));

// GET /api/ports/count - Get count of all ports
router.get('/count', asyncHandler(async (req: Request, res: Response) => {
  const count = await portsService.count();
  res.json({ count });
}));

// GET /api/ports/:id - Get specific port scan
router.get('/:id', asyncHandler(async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  const ports = await portsService.findById(id);
  res.json({ data: ports });
}));

export default router;
