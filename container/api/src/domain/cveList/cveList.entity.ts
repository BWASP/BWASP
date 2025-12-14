import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity({
  name: 'cveList',
  orderBy: {
    id: 'DESC',
  },
  synchronize: true,
})
export default class cveListEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'text', nullable: false })
  year: string;

  @Column({ type: 'text', nullable: false })
  description: string;

  constructor(year: string, description: string) {
    this.year = year;
    this.description = description;
  }
}
