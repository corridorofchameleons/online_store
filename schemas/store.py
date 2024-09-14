from pydantic import BaseModel


class ItemOutModel(BaseModel):
    """
    Сериализатор ответа модели товара
    """
    id: int
    name: str
    price: int


class ItemListModel(BaseModel):
    """
    Сериализатор списка товаров
    """
    items: list[ItemOutModel]


class ItemCreateUpdateModel(BaseModel):
    """
    Сериализатор создания товара
    """
    name: str
    price: int
    is_active: bool


class ItemCreateUpdateOutModel(ItemCreateUpdateModel):
    """
    Сериализатор ответа после создания товара
    """
    id: int


class ItemDeleteModel(BaseModel):
    """
    Сериализатор ответа после удаления товара
    """
    id: int
    name: str


class CartDeleteItem(BaseModel):
    """
    Сериализатор удаления товара из корзины
    """
    item_id: int


class CartItemModel(CartDeleteItem):
    """
    Сериализатор объекта в корзине
    """
    qty: int | None = 1


class CartOutItemModel(CartItemModel):
    """
    Сериализатор публичного представления объекта в корзине
    """
    id: int
    item_name: str
    item_price: int


class CartItemListModel(BaseModel):
    """
    Сериализатор публичного представления списка объектов в корзине
    """
    items: list[CartOutItemModel]
    total: int
