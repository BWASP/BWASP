import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity({
  name: 'packets',
  orderBy: {
    id: 'DESC',
  },
  synchronize: true,
})
export default class packetEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'int', nullable: false })
  category: number;

  @Column({ type: 'int', nullable: false })
  statusCode: number;

  @Column({ type: 'text', nullable: false })
  requestType: string;

  @Column({ type: 'text', nullable: false })
  requestJson: string;

  @Column({ type: 'text', nullable: false })
  responseHeader: string;

  @Column({ type: 'text', nullable: false })
  responseBody: string;

  constructor(
    category: number,
    statusCode: number,
    requestType: string,
    requestJson: string,
    responseHeader: string,
    responseBody: string
  ) {
    this.category = category;
    this.statusCode = statusCode;
    this.requestType = requestType;
    this.requestJson = requestJson;
    this.responseHeader = responseHeader;
    this.responseBody = responseBody;
  }
}
