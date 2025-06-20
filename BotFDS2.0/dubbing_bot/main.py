# main.py
from handlers.admin import register_handlers_admin
from handlers.dubber import register_handlers_dubber
from middlewares.throttle import ThrottlingMiddleware

def main():
    dp.middleware.setup(ThrottlingMiddleware())
    register_handlers_admin(dp)
    register_handlers_dubber(dp)


