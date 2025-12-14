import database from '../../../infra/connector/database';
import cveListEntity from '../../../domain/cveList/cveList.entity';
import { Repository, Like } from 'typeorm';

export class CveListService {
  private repository: Repository<cveListEntity>;

  constructor() {
    this.repository = database.source.getRepository(cveListEntity);
  }

  async search(framework: string, version: string, limit: number = 9): Promise<cveListEntity[]> {
    // Search for CVEs by framework and version in description
    // The Python version searches with LIKE pattern containing framework and version
    const searchPattern = `%${framework}%${version}%`;

    return this.repository.find({
      where: {
        description: Like(searchPattern),
      },
      take: limit,
      order: { id: 'DESC' },
    });
  }

  async searchCount(framework: string, version: string): Promise<number> {
    const searchPattern = `%${framework}%${version}%`;

    return this.repository.count({
      where: {
        description: Like(searchPattern),
      },
    });
  }
}

export default new CveListService();
