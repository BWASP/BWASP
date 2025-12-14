import express, { Request, Response } from 'express';
import { asyncHandler } from '../../../infra/middleware/asyncHandler';
import packetService from './index';

const router = express.Router();

// GET /api/packet - List all packets
router.get('/', asyncHandler(async (req: Request, res: Response) => {
  const packets = await packetService.findAll();
  res.json({ data: packets });
}));

// GET /api/packet/automation - Get all automation packets
router.get('/automation', asyncHandler(async (req: Request, res: Response) => {
  const packets = await packetService.findAutomation();
  res.json({ data: packets });
}));

// POST /api/packet/automation - Create automation packet(s)
router.post('/automation', asyncHandler(async (req: Request, res: Response) => {
  const data = Array.isArray(req.body)
    ? req.body.map(p => ({ ...p, category: 0 }))
    : { ...req.body, category: 0 };

  const result = await packetService.create(data);
  res.status(201).json({ data: result });
}));

// GET /api/packet/automation/index - Get list of automation packet IDs
router.get('/automation/index', asyncHandler(async (req: Request, res: Response) => {
  const ids = await packetService.getAutomationIds();
  res.json({ data: ids });
}));

// GET /api/packet/automation/count - Get count of automation packets
router.get('/automation/count', asyncHandler(async (req: Request, res: Response) => {
  const count = await packetService.countAutomation();
  res.json({ count });
}));

// GET /api/packet/automation/:id - Get single automation packet
router.get('/automation/:id', asyncHandler(async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  const packet = await packetService.findById(id);

  if (packet.category !== 0) {
    return res.status(404).json({ error: 'Automation packet not found' });
  }

  res.json({ data: packet });
}));

// GET /api/packet/manual - Get all manual packets
router.get('/manual', asyncHandler(async (req: Request, res: Response) => {
  const packets = await packetService.findManual();
  res.json({ data: packets });
}));

// POST /api/packet/manual - Create manual packet(s)
router.post('/manual', asyncHandler(async (req: Request, res: Response) => {
  const data = Array.isArray(req.body)
    ? req.body.map(p => ({ ...p, category: 1 }))
    : { ...req.body, category: 1 };

  const result = await packetService.create(data);
  res.status(201).json({ data: result });
}));

// GET /api/packet/manual/index - Get list of manual packet IDs
router.get('/manual/index', asyncHandler(async (req: Request, res: Response) => {
  const ids = await packetService.getManualIds();
  res.json({ data: ids });
}));

// GET /api/packet/manual/count - Get count of manual packets
router.get('/manual/count', asyncHandler(async (req: Request, res: Response) => {
  const count = await packetService.countManual();
  res.json({ count });
}));

// GET /api/packet/manual/:id - Get single manual packet
router.get('/manual/:id', asyncHandler(async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  const packet = await packetService.findById(id);

  if (packet.category !== 1) {
    return res.status(404).json({ error: 'Manual packet not found' });
  }

  res.json({ data: packet });
}));

// GET /api/packet/:id - Get specific packet by ID
router.get('/:id', asyncHandler(async (req: Request, res: Response) => {
  const id = parseInt(req.params.id);
  const packet = await packetService.findById(id);
  res.json({ data: packet });
}));

export default router;
