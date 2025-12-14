import 'reflect-metadata';
import { DataSource } from 'typeorm';
import env from '../../module/dotenv';

class Database {
    public source: DataSource;
    public initPromise: Promise<DataSource>;

    constructor() {
        this.init();
    }

    // entities: [process.cwd() + "/{src,dist}/domain/**/*.entity.{js,ts}"],
    // entities: [process.cwd() + '/dist/domain/**/*.entity.js'],
    init() {
        this.source = new DataSource({
            driver: undefined,
            type: 'postgres',
            host: env.DB_HOST,
            port: env.DB_PORT,
            username: env.DB_USER,
            password: env.DB_PASS,
            database: env.DB_NAME,
            entities: [
                process.cwd() + '/{src,dist}/domain/**/*.entity.{js,ts}',
            ],
            migrations: [],
            subscribers: [],
            synchronize: true,
            useUTC: true,
        });

        this.initPromise = this.source.initialize();
    }
}

const database = new Database();

export default database;
