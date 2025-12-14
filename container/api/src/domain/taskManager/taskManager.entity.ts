import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity({
  name: 'taskManager',
  orderBy: {
    id: 'DESC',
  },
  synchronize: true,
})
export default class taskManagerEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'text', nullable: false })
  targetURL: string;

  @Column({ type: 'text', nullable: false, unique: true })
  task_id: string;

  constructor(targetURL: string, task_id: string) {
    this.targetURL = targetURL;
    this.task_id = task_id;
  }
}
