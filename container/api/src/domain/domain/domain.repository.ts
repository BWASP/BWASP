import { Repository } from 'typeorm';
import domainEntity from './domain.entity';

export default class domainRepository extends Repository<domainEntity> {
  async findByURL(url: string): Promise<domainEntity[]> {
    return this.find({ where: { URL: url } });
  }

  async findByRelatedPacket(packetId: number): Promise<domainEntity[]> {
    return this.find({ where: { related_Packet: packetId } });
  }

  async findByImpactRate(impactRate: number): Promise<domainEntity[]> {
    return this.find({ where: { impactRate } });
  }
}
