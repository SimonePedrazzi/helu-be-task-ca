from abc import ABC, abstractmethod

from .model import Item


class ItemRepositoryInterface(ABC):
    @abstractmethod
    def find_item_by_name(self, name: str) -> Item | None:
        raise NotImplementedError

    @abstractmethod
    def get_all_items(self) -> list[Item]:
        raise NotImplementedError

    @abstractmethod
    def save_item(self, item: Item) -> Item:
        raise NotImplementedError
