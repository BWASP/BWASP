import database from '../../../infra/connector/database';
import systemInfoEntity from '../../../domain/systemInfo/systemInfo.entity';
import { AppError } from '../../../infra/middleware/errorHandler';
import { Repository } from 'typeorm';

export class SystemInfoService {
  private repository: Repository<systemInfoEntity>;

  constructor() {
    this.repository = database.source.getRepository(systemInfoEntity);
  }

  async findAll(): Promise<systemInfoEntity[]> {
    return this.repository.find();
  }

  async findById(id: number): Promise<systemInfoEntity> {
    const systemInfo = await this.repository.findOne({ where: { id } });
    if (!systemInfo) {
      throw new AppError('SystemInfo not found', 404);
    }
    return systemInfo;
  }

  async create(data: Partial<systemInfoEntity>): Promise<systemInfoEntity> {
    const entity = new systemInfoEntity(
      data.url ?? '',
      data.data ?? ''
    );

    return this.repository.save(entity);
  }

  async update(data: Partial<systemInfoEntity>): Promise<systemInfoEntity> {
    if (!data.id) {
      throw new AppError('SystemInfo ID is required for update', 400);
    }

    const systemInfo = await this.findById(data.id);

    if (data.url !== undefined) systemInfo.url = data.url;
    if (data.data !== undefined) systemInfo.data = data.data;

    return this.repository.save(systemInfo);
  }
}

export default new SystemInfoService();
