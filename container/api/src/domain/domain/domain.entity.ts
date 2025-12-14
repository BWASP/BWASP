import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity({
  name: 'domain',
  orderBy: {
    id: 'DESC',
  },
  synchronize: true,
})
export default class domainEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'int', nullable: false })
  related_Packet: number;

  @Column({ type: 'text', nullable: false })
  URL: string;

  @Column({ type: 'text', nullable: false })
  URI: string;

  @Column({ type: 'text', nullable: false })
  action_URL: string;

  @Column({ type: 'text', nullable: false })
  action_URL_Type: string;

  @Column({ type: 'text', nullable: false })
  params: string;

  @Column({ type: 'text', nullable: false })
  comment: string;

  @Column({ type: 'text', nullable: false })
  attackVector: string;

  @Column({ type: 'int', nullable: false })
  impactRate: number;

  @Column({ type: 'text', nullable: false })
  description: string;

  @Column({ type: 'text', nullable: false })
  Details: string;

  constructor(
    related_Packet: number,
    URL: string,
    URI: string,
    action_URL: string,
    action_URL_Type: string,
    params: string,
    comment: string,
    attackVector: string,
    impactRate: number,
    description: string,
    Details: string
  ) {
    this.related_Packet = related_Packet;
    this.URL = URL;
    this.URI = URI;
    this.action_URL = action_URL;
    this.action_URL_Type = action_URL_Type;
    this.params = params;
    this.comment = comment;
    this.attackVector = attackVector;
    this.impactRate = impactRate;
    this.description = description;
    this.Details = Details;
  }
}
