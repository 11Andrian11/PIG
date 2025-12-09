from typing import List, Optional
from .base import BaseDevice

class InventoryModel:
    def __init__(self):
        self.items: List[BaseDevice] = []

    def add(self, dev: BaseDevice) -> None:
        self.items.append(dev)

    def remove_index(self, idx: int) -> None:
        if 0 <= idx < len(self.items):
            self.items.pop(idx)

    def set_index(self, idx: int, dev: BaseDevice) -> None:
        if 0 <= idx < len(self.items):
            self.items[idx] = dev

    def get_index(self, idx: int) -> Optional[BaseDevice]:
        if 0 <= idx < len(self.items):
            return self.items[idx]
        return None

    def all(self) -> List[BaseDevice]:
        return list(self.items)
