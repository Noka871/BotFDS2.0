import asyncio
from database.models import User
from database.session import async_session
from sqlalchemy import select

async def test_db():
    # ... (код выше)

if __name__ == "__main__":
    asyncio.run(test_db())