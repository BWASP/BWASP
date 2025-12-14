import express from 'express';

// Import routers
import packetRouter from './restful/packet/packet.router';
import domainRouter from './restful/domain/domain.router';
import jobRouter from './restful/job/job.router';
import portsRouter from './restful/ports/ports.router';
import systemInfoRouter from './restful/systemInfo/systemInfo.router';
import cspEvaluatorRouter from './restful/cspEvaluator/cspEvaluator.router';
import cveListRouter from './restful/cveList/cveList.router';
import taskManagerRouter from './restful/taskManager/taskManager.router';
import manualRouter from './manual/manual.router';

const router = express.Router();

// Register restful API routes
router.use('/api/packet', packetRouter);
router.use('/api/domain', domainRouter);
router.use('/api/job', jobRouter);
router.use('/api/ports', portsRouter);
router.use('/api/systeminfo', systemInfoRouter);
router.use('/api/cspevaluator', cspEvaluatorRouter);
router.use('/api/cve', cveListRouter);
router.use('/api/task', taskManagerRouter);

// Register manual API route
router.use('/manual', manualRouter);

export default router;
