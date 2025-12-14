import express, { Request, Response } from 'express';
import { asyncHandler } from '../../infra/middleware/asyncHandler';
import manualService from './index';

const router = express.Router();

// POST / - Manual analysis endpoint
router.post('/', asyncHandler(async (req: Request, res: Response) => {
  const result = await manualService.processManualPackets(req.body);
  res.json(result);
}));

// GET / - Health check
router.get('/', (req: Request, res: Response) => {
  res.send('Success');
});

export default router;
