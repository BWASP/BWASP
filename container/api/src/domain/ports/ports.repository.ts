import { Repository } from 'typeorm';
import portsEntity from './ports.entity';

export default class portsRepository extends Repository<portsEntity> {
  async findByService(service: string): Promise<portsEntity[]> {
    return this.find({ where: { service } });
  }

  async findByTarget(target: string): Promise<portsEntity[]> {
    return this.find({ where: { target } });
  }

  async findByPort(port: string): Promise<portsEntity[]> {
    return this.find({ where: { port } });
  }

  async findByTargetAndPort(target: string, port: string): Promise<portsEntity[]> {
    return this.find({ where: { target, port } });
  }
}
