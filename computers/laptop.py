from dataclasses import dataclass
from base_class import BaseDevice

@dataclass
class Laptop(BaseDevice):
    category: str = "Laptop"
    gpu: str = "Integrated"
    screen_inch: float = 15.6
    battery_wh: int = 50
