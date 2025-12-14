import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity({
  name: 'cspEvaluator',
  orderBy: {
    id: 'DESC',
  },
  synchronize: true,
})
export default class cspEvaluatorEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'text', nullable: false })
  header: string;

  constructor(header: string) {
    this.header = header;
  }
}
