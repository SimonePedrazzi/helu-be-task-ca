from dataclasses import dataclass

from sqlalchemy.orm import Session

from .interfaces import ItemRepositoryInterface
from .model import Item


@dataclass
class SqlItemRepository(ItemRepositoryInterface):
    db: Session

    def find_item_by_name(self, name: str) -> Item | None:
        return self.db.query(Item).filter(Item.name == name).first()

    def get_all_items(self) -> list[Item]:
        return self.db.query(Item).all()

    def save_item(self, item: Item) -> Item:
        self.db.add(item)
        self.db.commit()
        return item
