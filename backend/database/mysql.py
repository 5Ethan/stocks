import aiomysql
import config

async def connect_to_mysql():
    pool = await aiomysql.create_pool(**config.db_config)
    return pool

async def execute_query(query):
    pool = await connect_to_mysql()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query)
            result = await cur.fetchall()
    pool.close()
    await pool.wait_closed()
    return result

async def execute_insert(table, data):
    keys = ','.join(data.keys())
    values_template = ','.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({keys}) VALUES ({values_template})"
    
    pool = await connect_to_mysql()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, list(data.values()))
            await conn.commit()

    pool.close()
    await pool.wait_closed()

    return True

async def execute_delete(table, condition):
    query = f"DELETE FROM {table} WHERE {condition}"
    
    pool = await connect_to_mysql()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
            await conn.commit()

    pool.close()
    await pool.wait_closed()

    return True