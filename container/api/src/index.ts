import 'reflect-metadata';
import app from './app';
import env from './infra/module/dotenv';
import database from './infra/connector/database';

const PORT = env.HTTP_PORT || 3000;

async function bootstrap() {
    try {
        // 데이터베이스 연결
        await database.initPromise;
        console.log('Database connected successfully');

        // 서버 시작
        app.listen(PORT, () => {
            console.log(`Server is running on port ${PORT}`);
        });
    } catch (error) {
        console.error('Failed to start server:', error);
        process.exit(1);
    }
}

bootstrap();

