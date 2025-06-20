import asyncio
import argparse
from database.session import engine, Base


async def init_db(recreate: bool = False):
    async with engine.begin() as conn:
        if recreate:
            print("Пересоздание всех таблиц...")
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных инициализирована")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--recreate", action="store_true", help="Пересоздать все таблицы")
    args = parser.parse_args()

    asyncio.run(init_db(args.recreate))

from database.session import engine, Base
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
