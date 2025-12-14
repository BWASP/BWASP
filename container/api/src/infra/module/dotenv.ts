class Env {
    public readonly TZ: string;

    public readonly HTTP_PORT: number;

    public readonly DB_HOST: string;
    public readonly DB_PORT: number;
    public readonly DB_USER: string;
    public readonly DB_PASS: string;
    public readonly DB_NAME: string;

    constructor() {
        this.TZ = process.env.TZ ?? 'KST';

        this.HTTP_PORT = parseInt(String(process.env.HTTP_PORT ?? '3000'), 10);

        this.DB_HOST = process.env.DB_HOST ?? 'db';
        this.DB_PORT = parseInt(String(process.env.DB_PORT ?? '5432'), 10);
        this.DB_USER = process.env.DB_USER ?? 'root';
        // docker-compose에서 DB_PASSWORD를 사용하므로 둘 다 확인
        this.DB_PASS = process.env.DB_PASS ?? process.env.DB_PASSWORD ?? 'root';
        this.DB_NAME = process.env.DB_NAME ?? 'bwasp';
    }
}

const env = new Env();

export default env;
