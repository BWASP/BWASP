import { config } from 'dotenv';

class Env {
    public readonly TZ: string;

    public readonly HTTP_PORT: number;

    public readonly DB_HOST: string;
    public readonly DB_PORT: number;
    public readonly DB_USER: string;
    public readonly DB_PASS: string;
    public readonly DB_NAME: string;

    constructor() {
        config();

        this.TZ = process.env.TZ ?? 'KST';

        this.HTTP_PORT = parseInt(String(process.env.HTTP_PORT), 10) ?? 5000;

        this.DB_HOST = process.env.DB_HOST ?? '';
        this.DB_PORT = parseInt(String(process.env.DB_PORT), 10) ?? 5432;
        this.DB_USER = process.env.DB_USER ?? '';
        this.DB_PASS = process.env.DB_PASS ?? '';
        this.DB_NAME = process.env.DB_NAME ?? '';
    }
}

const env = new Env();

export default env;
