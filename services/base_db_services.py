import datetime
from uuid import UUID
from config import config


def as_dict(obj: dict, add_fields: dict | None = None):
    if add_fields:
        for name, add_field in add_fields.items():
            obj[name] = add_field
    if isinstance(obj, list):
        for items in obj:
            for item in items:
                if isinstance(items[item], datetime.datetime):
                    items[item] = str(items[item])
                if isinstance(items[item], datetime.timedelta):
                    items[item] = str(items[item])
        return obj
    if isinstance(obj, dict):
        for item in obj:
            if isinstance(obj[item], datetime.datetime):
                obj[item] = str(obj[item])
            if isinstance(obj[item], datetime.timedelta):
                obj[item] = str(obj[item])
            if isinstance(obj[item], UUID):
                obj[item] = str(obj[item])
        return obj
    return obj


async def get_pagination_data(per_page: int, base_query: str, schema=None, search: str | None = None):
    select = f"""COUNT(*) as total_rows, CEILING(COUNT(*)/{per_page}::float)::integer as total_pages"""
    if schema:
        query = base_query.format(select=select, schema=schema)
    else:
        query = base_query.format(select=select)
    async with config['db'].acquire() as conn:
        if search:
            search = f"%{search}%"
            execute = await conn.execute(query, search)
        else:
            execute = await conn.execute(query)
        return await execute.first()

