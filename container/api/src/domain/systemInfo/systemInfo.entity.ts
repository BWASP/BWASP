import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity({
  name: 'systemInfo',
  orderBy: {
    id: 'DESC',
  },
  synchronize: true,
})
export default class systemInfoEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'text', nullable: false })
  url: string;

  @Column({ type: 'text', nullable: false })
  data: string;

  constructor(url: string, data: string) {
    this.url = url;
    this.data = data;
  }
}
