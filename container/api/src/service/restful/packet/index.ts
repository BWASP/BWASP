import database from '../../../infra/connector/database';
import packetEntity from '../../../domain/packet/packet.entity';
import packetRepository from '../../../domain/packet/packet.repository';
import { AppError } from '../../../infra/middleware/errorHandler';

export class PacketService {
  private repository: packetRepository;

  constructor() {
    this.repository = database.source.getRepository(packetEntity).extend(packetRepository.prototype);
  }

  async findAll(): Promise<packetEntity[]> {
    return this.repository.find();
  }

  async findById(id: number): Promise<packetEntity> {
    const packet = await this.repository.findOne({ where: { id } });
    if (!packet) {
      throw new AppError('Packet not found', 404);
    }
    return packet;
  }

  async findAutomation(): Promise<packetEntity[]> {
    return this.repository.findByCategory(0);
  }

  async findManual(): Promise<packetEntity[]> {
    return this.repository.findByCategory(1);
  }

  async getAutomationIds(): Promise<number[]> {
    const packets = await this.repository.find({
      where: { category: 0 },
      select: ['id'],
    });
    return packets.map(p => p.id);
  }

  async getManualIds(): Promise<number[]> {
    const packets = await this.repository.find({
      where: { category: 1 },
      select: ['id'],
    });
    return packets.map(p => p.id);
  }

  async countAutomation(): Promise<number> {
    return this.repository.count({ where: { category: 0 } });
  }

  async countManual(): Promise<number> {
    return this.repository.count({ where: { category: 1 } });
  }

  async create(data: Partial<packetEntity> | Partial<packetEntity>[]): Promise<packetEntity | packetEntity[]> {
    const packets = Array.isArray(data) ? data : [data];

    const entities = packets.map(p => {
      return new packetEntity(
        p.category ?? 0,
        p.statusCode ?? 0,
        p.requestType ?? '',
        p.requestJson ?? '',
        p.responseHeader ?? '',
        p.responseBody ?? ''
      );
    });

    const saved = await this.repository.save(entities);
    return Array.isArray(data) ? saved : saved[0];
  }
}

export default new PacketService();
