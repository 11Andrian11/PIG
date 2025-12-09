# model/inventory.py
from typing import List
from .base import BaseDevice

class InventoryModel:
    def __init__(self):
        self.items: List[BaseDevice] = []

    def add(self, device: BaseDevice):
        self.items.append(device)

    def remove(self, device: BaseDevice):
        if device in self.items:
            self.items.remove(device)

    def all(self):
        return list(self.items)
