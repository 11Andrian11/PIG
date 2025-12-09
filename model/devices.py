from dataclasses import dataclass
from .base import BaseDevice

@dataclass
class Laptop(BaseDevice):
    category: str = "Laptop"
    gpu: str = "Integrated"
    screen_inch: float = 15.6
    battery_wh: int = 50

@dataclass
class PC(BaseDevice):
    category: str = "PC"
    gpu: str = "Integrated"
    psu_watt: int = 450
    case_format: str = "ATX"

@dataclass
class Tablet(BaseDevice):
    category: str = "Tablet"
    screen_inch: float = 10.1
    battery_wh: int = 30

DEVICE_TYPES = {
    "Laptop": Laptop,
    "PC": PC,
    "Tablet": Tablet,
}
