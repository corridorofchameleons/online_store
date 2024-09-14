from fastapi import Depends
from fastapi.routing import APIRouter

from database.store import get_available_items, get_item, create_item, update_item, delete_item, add_item_to_cart, \
    select_from_cart, update_qty, remove_from_cart, clear_everything
from models.users import users
from schemas.store import ItemListModel, ItemOutModel, ItemCreateUpdateModel, ItemCreateUpdateOutModel, ItemDeleteModel, \
    CartItemModel, CartItemListModel, CartDeleteItem
from services.services import get_current_user, user_is_admin

router = APIRouter()


@router.get('/items', response_model=ItemListModel)
async def get_list(user: users = Depends(get_current_user)):
    items = await get_available_items()
    return {'items': items}


@router.get('/items/{item_id}', response_model=ItemOutModel)
async def get_one(item_id: int, user: users = Depends(get_current_user)):
    item = await get_item(item_id)
    return item


@router.post('/items/create', response_model=ItemCreateUpdateOutModel)
async def create(item: ItemCreateUpdateModel, user: users = Depends(user_is_admin)):
    result = await create_item(item)
    return result


@router.put('/items/update/{item_id}', response_model=ItemCreateUpdateOutModel)
async def update(item_id: int, item: ItemCreateUpdateModel, user: users = Depends(user_is_admin)):
    result = await update_item(item_id, item)
    return result


@router.delete('/items/delete/{item_id}', response_model=ItemDeleteModel)
async def delete(item_id: int, user: users = Depends(user_is_admin)):
    result = await delete_item(item_id)
    return result


@router.post('/cart/add')
async def add_to_cart(item: CartItemModel, user: users = Depends(get_current_user)):
    await add_item_to_cart(item, user)
    return {"status": "ok"}


@router.get('/cart', response_model=CartItemListModel)
async def view_cart(user: users = Depends(get_current_user)):
    items, total = await select_from_cart(user)
    return {"items": items, "total": total}


@router.put('/cart/update')
async def update_item_qty(item: CartItemModel, user: users = Depends(get_current_user)):
    await update_qty(item, user)
    return {"status": "ok"}


@router.delete('/cart/delete')
async def delete_item(item: CartDeleteItem, user: users = Depends(get_current_user)):
    await remove_from_cart(item, user)
    return {"status": "ok"}


@router.delete('/cart/clear')
async def clear_cart(user: users = Depends(get_current_user)):
    await clear_everything(user)
    return {"status": "ok"}
