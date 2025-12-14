import 'reflect-metadata';
import { DataSource } from 'typeorm';
import env from '../../module/dotenv';

// Entity 직접 import (glob 패턴 대신 - 런타임 오류 방지)
import packetEntity from '../../../domain/packet/packet.entity';
import domainEntity from '../../../domain/domain/domain.entity';
import jobEntity from '../../../domain/job/job.entity';
import portsEntity from '../../../domain/ports/ports.entity';
import systemInfoEntity from '../../../domain/systemInfo/systemInfo.entity';
import cspEvaluatorEntity from '../../../domain/cspEvaluator/cspEvaluator.entity';
import cveListEntity from '../../../domain/cveList/cveList.entity';
import taskManagerEntity from '../../../domain/taskManager/taskManager.entity';

class Database {
    public source: DataSource;
    public initPromise: Promise<DataSource>;

    constructor() {
        this.init();
    }

    init() {
        this.source = new DataSource({
            type: 'postgres',
            host: env.DB_HOST,
            port: env.DB_PORT,
            username: env.DB_USER,
            password: env.DB_PASS,
            database: env.DB_NAME,
            entities: [
                packetEntity,
                domainEntity,
                jobEntity,
                portsEntity,
                systemInfoEntity,
                cspEvaluatorEntity,
                cveListEntity,
                taskManagerEntity,
            ],
            migrations: [],
            subscribers: [],
            synchronize: true,
            useUTC: true,
            logging: process.env.NODE_ENV !== 'production',
        });

        this.initPromise = this.source.initialize();
    }
}

const database = new Database();

export default database;
