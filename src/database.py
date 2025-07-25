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
            print("Connect PostgreSQL")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
            print("Disconnect")

    async def check_user(self, tg_user_id: int):
        await self.connect()
        query = "SELECT EXISTS (SELECT 1 FROM users WHERE tg_user_id = $1)"
        result = await self.connection.fetchval(query, tg_user_id)
        return result
    
    async def register_user(self,tg_user_id: int, email: str, password_application: str, is_active: bool):
        await self.connect()
        query = """ INSERT INTO users (tg_user_id, email, password_application, is_active) 
                    VALUES ($1, $2, $3, $4)
        """
        await self.connection.execute(query, tg_user_id, email, password_application, is_active)
        print("Сreate user")



db_helper = DataBaseHelper()




