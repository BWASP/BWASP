import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity({
  name: 'ports',
  orderBy: {
    id: 'DESC',
  },
  synchronize: true,
})
export default class portsEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'text', nullable: false })
  service: string;

  @Column({ type: 'text', nullable: false })
  target: string;

  @Column({ type: 'text', nullable: false })
  port: string;

  @Column({ type: 'text', nullable: false })
  result: string;

  constructor(service: string, target: string, port: string, result: string) {
    this.service = service;
    this.target = target;
    this.port = port;
    this.result = result;
  }
}
