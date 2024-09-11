from fastapi import Depends
from fastapi.routing import APIRouter

from database.store import get_available_items, get_item, create_item, update_item, delete_item, add_item_to_cart, \
    select_from_cart
from models.users import users
from routers.auth import get_current_user, user_is_admin
from schemas.store import ItemListModel, ItemOutModel, ItemCreateUpdateModel, ItemCreateUpdateOutModel, ItemDeleteModel, \
    CartItemModel, CartItemListModel

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
async def create(item: ItemCreateUpdateModel, user: users = Depends(get_current_user)):
    await user_is_admin(user.email)
    result = await create_item(item)
    return result


@router.put('/items/update/{item_id}', response_model=ItemCreateUpdateOutModel)
async def update(item_id: int, item: ItemCreateUpdateModel, user: users = Depends(get_current_user)):
    await user_is_admin(user.email, )
    result = await update_item(item_id, item)
    return result


@router.delete('/items/delete/{item_id}', response_model=ItemDeleteModel)
async def delete(item_id: int, user: users = Depends(get_current_user)):
    await user_is_admin(user.email)
    result = await delete_item(item_id)
    return result


@router.post('/cart/add')
async def add_to_cart(item: CartItemModel, user: users = Depends(get_current_user)):
    await add_item_to_cart(item, user)
    return {"status": "ok"}


@router.get('/cart', response_model=CartItemListModel)
async def view_cart(user: users = Depends(get_current_user)):
    items = await select_from_cart(user)
    return {"items": items}
