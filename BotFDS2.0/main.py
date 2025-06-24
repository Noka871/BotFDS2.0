from core.bot import dp, bot
from handlers import register_handlers
import logging

async def main():
    register_handlers(dp)
    await dp.start_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())