import { Repository } from 'typeorm';
import taskManagerEntity from './taskManager.entity';

export default class taskManagerRepository extends Repository<taskManagerEntity> {
  async findByTargetURL(targetURL: string): Promise<taskManagerEntity[]> {
    return this.find({ where: { targetURL } });
  }

  async findByTaskId(taskId: string): Promise<taskManagerEntity | null> {
    return this.findOne({ where: { task_id: taskId } });
  }

  async deleteByTaskId(taskId: string): Promise<void> {
    await this.delete({ task_id: taskId });
  }
}
