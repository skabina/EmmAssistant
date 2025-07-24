from config import settings
import asyncpg

class DataBaseHelper:
    def __init__(self):
        self.connection: asyncpg.Connection | None = None

    async def connect(self):
        if not self.connection:
            self.connection = await asyncpg.connect(
                dsn=settings.env.DATABASE_DSN
            )
            print("Підключено до PostgreSQL через DSN")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
            print("З'єднання закрито")


db_helper = DataBaseHelper()

