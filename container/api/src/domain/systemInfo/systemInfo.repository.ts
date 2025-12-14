import { Repository } from 'typeorm';
import systemInfoEntity from './systemInfo.entity';

export default class systemInfoRepository extends Repository<systemInfoEntity> {
  async findByUrl(url: string): Promise<systemInfoEntity[]> {
    return this.find({ where: { url } });
  }

  async findByUrlPattern(pattern: string): Promise<systemInfoEntity[]> {
    return this.createQueryBuilder('systeminfo')
      .where('systeminfo.url LIKE :pattern', { pattern: `%${pattern}%` })
      .getMany();
  }
}
