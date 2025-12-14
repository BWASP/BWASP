import express, { Request, Response } from 'express';
import { asyncHandler } from '../../../infra/middleware/asyncHandler';
import taskManagerService from './index';

const router = express.Router();

// POST /api/task - Create task
router.post('/', asyncHandler(async (req: Request, res: Response) => {
  const result = await taskManagerService.create(req.body);
  res.status(201).json({ data: result });
}));

// GET /api/task/count - Get count of all tasks
router.get('/count', asyncHandler(async (req: Request, res: Response) => {
  const count = await taskManagerService.count();
  res.json({ count });
}));

// POST /api/task/database/create - Create new task-specific database
router.post('/database/create', asyncHandler(async (req: Request, res: Response) => {
  const { task_id } = req.body;

  if (!task_id) {
    return res.status(400).json({ error: 'task_id is required' });
  }

  const result = await taskManagerService.createTaskDatabase(task_id);
  res.status(201).json(result);
}));

// GET /api/task/:id - Get specific task
router.get('/:id', asyncHandler(async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  const task = await taskManagerService.findById(id);
  res.json({ data: task });
}));

export default router;
