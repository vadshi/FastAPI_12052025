# from database import engine
from database import async_engine, get_db

# print(engine.connect())
print(async_engine.connect())
print(get_db())