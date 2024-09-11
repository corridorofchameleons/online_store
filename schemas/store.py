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
