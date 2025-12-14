import { Repository } from 'typeorm';
import cveListEntity from './cveList.entity';

export default class cveListRepository extends Repository<cveListEntity> {
  async findByYear(year: string): Promise<cveListEntity[]> {
    return this.find({ where: { year } });
  }

  async findByDescriptionPattern(pattern: string): Promise<cveListEntity[]> {
    return this.createQueryBuilder('cvelist')
      .where('cvelist.description LIKE :pattern', { pattern: `%${pattern}%` })
      .getMany();
  }

  async findRecentCVEs(limit: number = 10): Promise<cveListEntity[]> {
    return this.find({
      order: { year: 'DESC', id: 'DESC' },
      take: limit
    });
  }
}
