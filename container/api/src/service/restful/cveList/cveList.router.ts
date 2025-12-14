import express, { Request, Response } from 'express';
import { asyncHandler } from '../../../infra/middleware/asyncHandler';
import cveListService from './index';

const router = express.Router();

// GET /api/cve/search/:framework/:version - Search CVEs by framework and version
router.get('/search/:framework/:version', asyncHandler(async (req: Request, res: Response) => {
  const { framework, version } = req.params;
  const cves = await cveListService.search(framework, version);
  res.json({ data: cves });
}));

// GET /api/cve/search/:framework/:version/count - Get count of search results
router.get('/search/:framework/:version/count', asyncHandler(async (req: Request, res: Response) => {
  const { framework, version } = req.params;
  const count = await cveListService.searchCount(framework, version);
  res.json({ count });
}));

export default router;
