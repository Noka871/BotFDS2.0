[alembic]
script_location = alembic
sqlalchemy.url = sqlite+aiosqlite:///db.sqlite3

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic