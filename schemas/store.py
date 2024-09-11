from pydantic import BaseModel


class ItemOutModel(BaseModel):
    """
    Валидатор ответа модели товара
    """
    id: int
    name: str
    price: int


class ItemListModel(BaseModel):
    """
    Валидатор списка товаров
    """
    items: list[ItemOutModel]


class ItemCreateUpdateModel(BaseModel):
    """
    Валидатор создания товара
    """
    name: str
    price: int
    is_active: bool


class ItemCreateUpdateOutModel(ItemCreateUpdateModel):
    """
    Валидатор ответа после создания товара
    """
    id: int


class ItemDeleteModel(BaseModel):
    """
    Валидатор ответа после удаления товара
    """
    id: int
    name: str


class CartItemModel(BaseModel):
    """
    Валидатор объекта в корзине
    """
    item_id: int
    item_qty: int | None = 1


class CartOutItemModel(CartItemModel):
    """
    Валидатор публичного представления объекта в корзине
    """
    id: int
    item_name: str
    item_price: int


class CartItemListModel(BaseModel):
    """
    Валидатор публичного представления списка объектов в корзине
    """
    items: list[CartOutItemModel]
