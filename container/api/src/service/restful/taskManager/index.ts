import database from '../../../infra/connector/database';
import taskManagerEntity from '../../../domain/taskManager/taskManager.entity';
import { AppError } from '../../../infra/middleware/errorHandler';
import { Repository, DataSource } from 'typeorm';
import env from '../../../infra/module/dotenv';

export class TaskManagerService {
  private repository: Repository<taskManagerEntity>;

  constructor() {
    this.repository = database.source.getRepository(taskManagerEntity);
  }

  async findById(id: number): Promise<taskManagerEntity> {
    const task = await this.repository.findOne({ where: { id } });
    if (!task) {
      throw new AppError('Task not found', 404);
    }
    return task;
  }

  async count(): Promise<number> {
    return this.repository.count();
  }

  async create(data: Partial<taskManagerEntity>): Promise<taskManagerEntity> {
    const entity = new taskManagerEntity(
      data.targetURL ?? '',
      data.task_id ?? ''
    );

    return this.repository.save(entity);
  }

  async createTaskDatabase(taskId: string): Promise<{ message: string; database: string }> {
    // Create a new database for the task
    const dbName = `task_${taskId}`;

    try {
      // Create a temporary connection to create the new database
      const tempDataSource = new DataSource({
        type: 'postgres',
        host: env.DB_HOST,
        port: env.DB_PORT,
        username: env.DB_USER,
        password: env.DB_PASS,
        database: 'postgres', // Connect to default postgres database
      });

      await tempDataSource.initialize();

      // Create the new database
      await tempDataSource.query(`CREATE DATABASE "${dbName}"`);

      await tempDataSource.destroy();

      return {
        message: 'Task database created successfully',
        database: dbName,
      };
    } catch (error: any) {
      if (error.code === '42P04') {
        // Database already exists
        throw new AppError('Task database already exists', 409);
      }
      throw error;
    }
  }
}

export default new TaskManagerService();
