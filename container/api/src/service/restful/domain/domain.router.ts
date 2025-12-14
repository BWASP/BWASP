import express, { Request, Response } from 'express';
import { asyncHandler } from '../../../infra/middleware/asyncHandler';
import domainService from './index';

const router = express.Router();

// GET /api/domain - List all domains
router.get('/', asyncHandler(async (req: Request, res: Response) => {
  const domains = await domainService.findAll();
  res.json({ data: domains });
}));

// POST /api/domain - Create domain(s)
router.post('/', asyncHandler(async (req: Request, res: Response) => {
  const result = await domainService.create(req.body);
  res.status(201).json({ data: result });
}));

// GET /api/domain/count - Get count of all domains
router.get('/count', asyncHandler(async (req: Request, res: Response) => {
  const count = await domainService.count();
  res.json({ count });
}));

// GET /api/domain/:start/:counting - Get paginated domain data
router.get('/:start/:counting', asyncHandler(async (req: Request, res: Response) => {
  const start = parseInt(req.params.start);
  const counting = parseInt(req.params.counting);

  const domains = await domainService.findPaginated(start, counting);
  res.json({ data: domains });
}));

// GET /api/domain/:id - Get specific domain
router.get('/:id', asyncHandler(async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  const domain = await domainService.findById(id);
  res.json({ data: domain });
}));

export default router;
