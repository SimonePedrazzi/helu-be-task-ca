from uuid import uuid4

from .interfaces import ItemRepositoryInterface
from .model import Item
from .schema import AllItemsResponse, CreateItemRequest, CreateItemResponse


class ItemAlreadyExistsError(Exception):
    def __init__(self, message: str, **extra):
        self.message = message
        self.extra = extra
        super().__init__(self.message)


def create_item(
    item: CreateItemRequest, repo: ItemRepositoryInterface
) -> CreateItemResponse:
    if repo.find_item_by_name(item.name) is not None:
        raise ItemAlreadyExistsError("An item with this name already exists")

    new_item = Item(
        id=uuid4(),
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

    repo.save_item(new_item)
    return model_to_schema(new_item)


def get_all(repo: ItemRepositoryInterface) -> AllItemsResponse:
    item_list = repo.get_all_items()
    return AllItemsResponse(items=list(map(model_to_schema, item_list)))


def model_to_schema(item: Item) -> CreateItemResponse:
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )
