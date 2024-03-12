import asyncio
import os
import psycopg2
import aiopg

instance = "dbname={database} user={user} password={password} host={host} port={port}".format(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
)


async def notify(conn):
    async with conn.cursor() as cur:
        for i in range(5):
            msg = f"message {i}"
            print("Send ->", msg)
            await cur.execute("NOTIFY channel, %s", (msg,))

        await cur.execute("NOTIFY channel, 'finish'")


async def listen(conn):
    async with conn.cursor() as cur:
        await cur.execute("LISTEN channel")
        while True:
            try:
                msg = await conn.notifies.get()
            except psycopg2.Error as ex:
                print("ERROR: ", ex)
                return
            if msg.payload == "finish":
                return
            else:
                print("Receive <-", msg.payload)


async def main():
    async with aiopg.connect(instance) as listenConn:
        async with aiopg.create_pool(instance) as notifyPool:
            async with notifyPool.acquire() as notifyConn:
                listener = listen(listenConn)
                notifier = notify(notifyConn)
                await asyncio.gather(listener, notifier)
    print("ALL DONE")


asyncio.run(main())
