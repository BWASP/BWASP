import express, { Request, Response } from 'express';
import { asyncHandler } from '../../../infra/middleware/asyncHandler';
import cspEvaluatorService from './index';

const router = express.Router();

// GET /api/cspevaluator - List all CSP evaluator data
router.get('/', asyncHandler(async (req: Request, res: Response) => {
  const cspEvaluators = await cspEvaluatorService.findAll();
  res.json({ data: cspEvaluators });
}));

// POST /api/cspevaluator - Create CSP evaluator data
router.post('/', asyncHandler(async (req: Request, res: Response) => {
  const result = await cspEvaluatorService.create(req.body);
  res.status(201).json({ data: result });
}));

// GET /api/cspevaluator/:id - Get specific CSP evaluator
router.get('/:id', asyncHandler(async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  const cspEvaluator = await cspEvaluatorService.findById(id);
  res.json({ data: cspEvaluator });
}));

export default router;
