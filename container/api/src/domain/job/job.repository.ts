import { Repository } from 'typeorm';
import jobEntity from './job.entity';

export default class jobRepository extends Repository<jobEntity> {
  async findByTargetURL(targetURL: string): Promise<jobEntity[]> {
    return this.find({ where: { targetURL } });
  }

  async findPendingJobs(): Promise<jobEntity[]> {
    return this.find({ where: { done: false } });
  }

  async findCompletedJobs(): Promise<jobEntity[]> {
    return this.find({ where: { done: true } });
  }

  async markJobAsDone(id: number): Promise<void> {
    await this.update(id, { done: true });
  }
}
