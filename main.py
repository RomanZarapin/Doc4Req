from aiohttp import web
from dotenv import load_dotenv
from services.log import create_loggers
from middleware.auth import auth_middleware
import os
from services.cors import setup_cors
from config.jinja_init import jinja_init
from middleware.errors import errors_middleware


import logging
from config import setup_config
from config.connect_redis import redis_connect
from config.db import init_pg, close_pg
from aiohttp_session import setup
from routes import apply_routes
from aiojobs.aiohttp import setup as setup_aiojobs


# async def dispose_redis_pool(app):
#     redis_pool.close()
#     await redis_pool.wait_closed()


load_dotenv()
app = web.Application()

# Add config to app
setup_config(app)

jinja_init(app)


# Redis connect
# storage, redis_pool = redis_connect(app)
# setup(app, storage)

# Add routes
apply_routes(app)

# Add CORS
setup_cors(app)

app.middlewares.append(errors_middleware)
app.middlewares.append(auth_middleware)

create_loggers(app)


app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
# app.on_cleanup.append(dispose_redis_pool)
setup_aiojobs(app)


if __name__ == '__main__':
    database = os.getenv('DB_NAME')
    web.run_app(app, host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', '8080')))
