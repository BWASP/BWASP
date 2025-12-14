import database from '../../../infra/connector/database';
import portsEntity from '../../../domain/ports/ports.entity';
import { AppError } from '../../../infra/middleware/errorHandler';
import { Repository } from 'typeorm';

export class PortsService {
  private repository: Repository<portsEntity>;

  constructor() {
    this.repository = database.source.getRepository(portsEntity);
  }

  async findAll(): Promise<portsEntity[]> {
    return this.repository.find();
  }

  async findById(id: number): Promise<portsEntity> {
    const ports = await this.repository.findOne({ where: { id } });
    if (!ports) {
      throw new AppError('Ports record not found', 404);
    }
    return ports;
  }

  async count(): Promise<number> {
    return this.repository.count();
  }

  async create(data: Partial<portsEntity> | Partial<portsEntity>[]): Promise<portsEntity | portsEntity[]> {
    const portsData = Array.isArray(data) ? data : [data];

    const entities = portsData.map(p => {
      return new portsEntity(
        p.service ?? '',
        p.target ?? '',
        p.port ?? '',
        p.result ?? ''
      );
    });

    const saved = await this.repository.save(entities);
    return Array.isArray(data) ? saved : saved[0];
  }
}

export default new PortsService();
