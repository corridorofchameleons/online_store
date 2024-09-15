from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete

from database.db_config import engine, async_session_maker
from models.store import items, cart
from schemas.store import ItemOutModel, ItemCreateUpdateModel, ItemCreateUpdateOutModel, ItemDeleteModel, \
    CartOutItemModel


async def get_available_items() -> list[ItemOutModel]:
    '''
    Возвращает список доступных товаров
    '''
    async with async_session_maker() as session:
        stmt = select(items.c.id, items.c.name, items.c.price).where(items.c.is_active)
        result = await session.execute(stmt)
        data = result.fetchall()
        item_list = []
        for d in data:
            item_list.append(ItemOutModel(id=d[0], name=d[1], price=d[2]))
        return item_list


async def get_item(item_id: int) -> ItemOutModel:
    '''
    Возвращает товар по его id
    '''
    async with async_session_maker() as session:
        stmt = select(items.c.id, items.c.name, items.c.price).where(
            items.c.is_active &
            (items.c.id == item_id)
        )
        result = await session.execute(stmt)
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
    async with async_session_maker() as session:
        stmt = insert(items).returning(items.c.id).values(name=item.name, price=item.price, is_active=item.is_active)
        result = await session.execute(stmt)
        item_id = result.fetchone()[0]
        await session.commit()
        return ItemCreateUpdateOutModel(id=item_id, name=item.name, price=item.price, is_active=item.is_active)


async def update_item(item_id: int, item: ItemCreateUpdateModel) -> ItemCreateUpdateOutModel:
    '''
    Изменяет запись в таблице товаров
    '''
    async with async_session_maker() as session:
        stmt = update(items).where(items.c.id == item_id).values(name=item.name, price=item.price, is_active=item.is_active)
        await session.execute(stmt)
        await session.commit()
        return ItemCreateUpdateOutModel(id=item_id, name=item.name, price=item.price, is_active=item.is_active)


async def delete_item(item_id: int) -> ItemDeleteModel:
    '''
    Удаляет запись в таблице товаров
    '''
    async with async_session_maker() as session:
        stmt = delete(items).returning(items.c.name).where(items.c.id == item_id)
        result = await session.execute(stmt)
        data = result.fetchone()
        if data:
            item_name = data[0]
            await session.commit()
            return ItemDeleteModel(id=item_id, name=item_name)
        else:
            raise HTTPException(status_code=404, detail='Item not found')


async def add_item_to_cart(item, user):
    '''
    Создает запись  в таблице корзины
    '''
    async with async_session_maker() as session:
        stmt = insert(cart).values(item_id=item.item_id, user_id=user.id, qty=item.qty)
        try:
            await session.execute(stmt)
            await session.commit()
        except:
            raise HTTPException(status_code=422, detail='Товар уже добавлен')


async def select_from_cart(user) -> tuple[list[CartOutItemModel], int]:
    '''
    Получает список товаров в корзине
    '''
    async with async_session_maker() as session:
        stmt = select(cart.c.id, cart.c.item_id, items.c.name, items.c.price, cart.c.qty).where(cart.c.user_id == user.id).join(items, items.c.id == cart.c.item_id)
        result = await session.execute(stmt)
        data = result.fetchall()

        total = 0
        item_list = []

        for d in data:
            item_list.append(CartOutItemModel(id=d[0], item_id=d[1], item_name=d[2], item_price=d[3], qty=d[4]))
            total += d[3] * d[4]

    return item_list, total


async def update_qty(item, user):
    '''
    Обновляет количество товара в корзине
    '''
    async with async_session_maker() as session:
        stmt = update(cart).where((cart.c.user_id == user.id) & (cart.c.item_id == item.item_id)).values(qty=item.qty)
        await session.execute(stmt)
        await session.commit()


async def remove_from_cart(item, user):
    '''
    Удаляет товар из корзины
    '''
    async with async_session_maker() as session:
        stmt = delete(cart).where((cart.c.user_id == user.id) & (cart.c.item_id == item.item_id))
        await session.execute(stmt)
        await session.commit()


async def clear_everything(user):
    '''
    Очищает корзину по id юзера
    '''
    async with async_session_maker() as session:
        stmt = delete(cart).where(cart.c.user_id == user.id)
        await session.execute(stmt)
        await session.commit()
