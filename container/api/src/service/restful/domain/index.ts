import database from '../../../infra/connector/database';
import domainEntity from '../../../domain/domain/domain.entity';
import { AppError } from '../../../infra/middleware/errorHandler';
import { Repository } from 'typeorm';

export class DomainService {
  private repository: Repository<domainEntity>;

  constructor() {
    this.repository = database.source.getRepository(domainEntity);
  }

  async findAll(): Promise<domainEntity[]> {
    return this.repository.find();
  }

  async findById(id: number): Promise<domainEntity> {
    const domain = await this.repository.findOne({ where: { id } });
    if (!domain) {
      throw new AppError('Domain not found', 404);
    }
    return domain;
  }

  async findPaginated(start: number, count: number): Promise<domainEntity[]> {
    return this.repository.find({
      skip: start,
      take: count,
      order: { id: 'DESC' },
    });
  }

  async count(): Promise<number> {
    return this.repository.count();
  }

  async create(data: Partial<domainEntity> | Partial<domainEntity>[]): Promise<domainEntity | domainEntity[]> {
    const domains = Array.isArray(data) ? data : [data];

    const entities = domains.map(d => {
      return new domainEntity(
        d.related_Packet ?? 0,
        d.URL ?? '',
        d.URI ?? '',
        d.action_URL ?? '',
        d.action_URL_Type ?? '',
        d.params ?? '',
        d.comment ?? '',
        d.attackVector ?? '',
        d.impactRate ?? 0,
        d.description ?? '',
        d.Details ?? ''
      );
    });

    const saved = await this.repository.save(entities);
    return Array.isArray(data) ? saved : saved[0];
  }
}

export default new DomainService();
