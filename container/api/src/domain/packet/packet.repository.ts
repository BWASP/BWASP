import { Repository } from 'typeorm';
import packetEntity from './packet.entity';

export default class packetRepository extends Repository<packetEntity> {
  async findByCategory(category: number): Promise<packetEntity[]> {
    return this.find({ where: { category } });
  }

  async findByStatusCode(statusCode: number): Promise<packetEntity[]> {
    return this.find({ where: { statusCode } });
  }

  async findByRequestType(requestType: string): Promise<packetEntity[]> {
    return this.find({ where: { requestType } });
  }
}
