import database from '../../../infra/connector/database';
import cspEvaluatorEntity from '../../../domain/cspEvaluator/cspEvaluator.entity';
import { AppError } from '../../../infra/middleware/errorHandler';
import { Repository } from 'typeorm';

export class CspEvaluatorService {
  private repository: Repository<cspEvaluatorEntity>;

  constructor() {
    this.repository = database.source.getRepository(cspEvaluatorEntity);
  }

  async findAll(): Promise<cspEvaluatorEntity[]> {
    return this.repository.find();
  }

  async findById(id: number): Promise<cspEvaluatorEntity> {
    const cspEvaluator = await this.repository.findOne({ where: { id } });
    if (!cspEvaluator) {
      throw new AppError('CSP Evaluator not found', 404);
    }
    return cspEvaluator;
  }

  async create(data: Partial<cspEvaluatorEntity>): Promise<cspEvaluatorEntity> {
    const entity = new cspEvaluatorEntity(data.header ?? '');
    return this.repository.save(entity);
  }
}

export default new CspEvaluatorService();
