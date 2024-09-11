from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete

from database.db_config import engine
from models.store import items
from schemas.store import ItemOutModel, ItemCreateUpdateModel, ItemCreateUpdateOutModel, ItemDeleteModel


async def get_available_items() -> list[ItemOutModel]:
    '''
    Возвращает список доступных товаров
    '''
    async with engine.connect() as conn:
        stmt = select(items.c.id, items.c.name, items.c.price).where(items.c.is_active)
        result = await conn.execute(stmt)
        data = result.fetchall()
        item_list = []
        for d in data:
            item_list.append(ItemOutModel(id=d[0], name=d[1], price=d[2]))
        return item_list


async def get_item(item_id: int) -> ItemOutModel:
    '''
    Возвращает товар по его id
    '''
    async with engine.connect() as conn:
        stmt = select(items.c.id, items.c.name, items.c.price).where(
            items.c.is_active &
            (items.c.id == item_id)
        )
        result = await conn.execute(stmt)
        data = result.fetchone()
        if data:
            item = data._mapping
        else:
            raise HTTPException(status_code=404, detail='Item not found')

    return ItemOutModel(**item)


async def create_item(item: ItemCreateUpdateModel) -> ItemCreateUpdateOutModel:
    '''
    Создает запись в таблице товаров
    '''
    async with engine.connect() as conn:
        stmt = insert(items).returning(items.c.id).values(name=item.name, price=item.price, is_active=item.is_active)
        result = await conn.execute(stmt)
        item_id = result.fetchone()[0]
        await conn.commit()
        return ItemCreateUpdateOutModel(id=item_id, name=item.name, price=item.price, is_active=item.is_active)


async def update_item(item_id: int, item: ItemCreateUpdateModel) -> ItemCreateUpdateOutModel:
    '''
    Изменяет запись в таблице товаров
    '''
    async with engine.connect() as conn:
        stmt = update(items).where(items.c.id == item_id).values(name=item.name, price=item.price, is_active=item.is_active)
        await conn.execute(stmt)
        await conn.commit()
        return ItemCreateUpdateOutModel(id=item_id, name=item.name, price=item.price, is_active=item.is_active)


async def delete_item(item_id: int) -> ItemDeleteModel:
    '''
    Удаляет запись в таблице товаров
    '''
    async with engine.connect() as conn:
        stmt = delete(items).returning(items.c.name).where(items.c.id == item_id)
        result = await conn.execute(stmt)
        data = result.fetchone()
        if data:
            item_name = data[0]
            await conn.commit()
            return ItemDeleteModel(id=item_id, name=item_name)
        else:
            raise HTTPException(status_code=404, detail='Item not found')