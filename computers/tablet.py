from dataclasses import dataclass
from base_class import BaseDevice

@dataclass
class Tablet(BaseDevice):
    category: str = "Tablet"
    screen_inch: float = 10.1
    battery_wh: int = 30
