import os

import aiopg.sa

from config import config


async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        minsize=1,
        maxsize=5,
        loop=app.loop)
    config['db'] = engine
    setattr(app, 'db', engine)


async def close_pg(app):
    app.db.close()
    await app.db.wait_closed()
