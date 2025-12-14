import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity({
  name: 'job',
  orderBy: {
    id: 'DESC',
  },
  synchronize: true,
})
export default class jobEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'text', nullable: false })
  targetURL: string;

  @Column({ type: 'text', nullable: false })
  knownInfo: string;

  @Column({ type: 'text', nullable: false })
  recursiveLevel: string;

  @Column({ type: 'boolean', default: false, nullable: false })
  done: boolean;

  @Column({ type: 'text', nullable: false })
  maximumProcess: string;

  constructor(
    targetURL: string,
    knownInfo: string,
    recursiveLevel: string,
    done: boolean,
    maximumProcess: string
  ) {
    this.targetURL = targetURL;
    this.knownInfo = knownInfo;
    this.recursiveLevel = recursiveLevel;
    this.done = done;
    this.maximumProcess = maximumProcess;
  }
}
