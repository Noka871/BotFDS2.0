# init_db.py
import asyncio
import os
import sys

# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def main():
    from services.database.core import create_db
    await create_db()
    print("✅ База данных успешно создана!")

if __name__ == '__main__':
    asyncio.run(main())