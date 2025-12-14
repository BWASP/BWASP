import database from '../../../infra/connector/database';
import jobEntity from '../../../domain/job/job.entity';
import { AppError } from '../../../infra/middleware/errorHandler';
import { Repository } from 'typeorm';

export class JobService {
  private repository: Repository<jobEntity>;

  constructor() {
    this.repository = database.source.getRepository(jobEntity);
  }

  async findAll(): Promise<jobEntity[]> {
    return this.repository.find();
  }

  async findById(id: number): Promise<jobEntity> {
    const job = await this.repository.findOne({ where: { id } });
    if (!job) {
      throw new AppError('Job not found', 404);
    }
    return job;
  }

  async create(data: Partial<jobEntity> | Partial<jobEntity>[]): Promise<jobEntity | jobEntity[]> {
    const jobs = Array.isArray(data) ? data : [data];

    const entities = jobs.map(j => {
      return new jobEntity(
        j.targetURL ?? '',
        j.knownInfo ?? '',
        j.recursiveLevel ?? '',
        j.done ?? false,
        j.maximumProcess ?? ''
      );
    });

    const saved = await this.repository.save(entities);
    return Array.isArray(data) ? saved : saved[0];
  }

  async update(data: Partial<jobEntity> | Partial<jobEntity>[]): Promise<jobEntity | jobEntity[]> {
    const jobs = Array.isArray(data) ? data : [data];

    const updated: jobEntity[] = [];

    for (const jobData of jobs) {
      if (!jobData.id) {
        throw new AppError('Job ID is required for update', 400);
      }

      const job = await this.findById(jobData.id);

      // Update fields
      if (jobData.done !== undefined) job.done = jobData.done;
      if (jobData.targetURL !== undefined) job.targetURL = jobData.targetURL;
      if (jobData.knownInfo !== undefined) job.knownInfo = jobData.knownInfo;
      if (jobData.recursiveLevel !== undefined) job.recursiveLevel = jobData.recursiveLevel;
      if (jobData.maximumProcess !== undefined) job.maximumProcess = jobData.maximumProcess;

      const saved = await this.repository.save(job);
      updated.push(saved);
    }

    return Array.isArray(data) ? updated : updated[0];
  }
}

export default new JobService();
