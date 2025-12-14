import { Repository } from 'typeorm';
import cspEvaluatorEntity from './cspEvaluator.entity';

export default class cspEvaluatorRepository extends Repository<cspEvaluatorEntity> {
  async findByHeader(header: string): Promise<cspEvaluatorEntity[]> {
    return this.find({ where: { header } });
  }

  async findByHeaderPattern(pattern: string): Promise<cspEvaluatorEntity[]> {
    return this.createQueryBuilder('cspevaluator')
      .where('cspevaluator.header LIKE :pattern', { pattern: `%${pattern}%` })
      .getMany();
  }
}
