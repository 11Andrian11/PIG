from dataclasses import dataclass
from base_class import BaseDevice

@dataclass
class PC(BaseDevice):
    category: str = "PC"
    gpu: str = "Integrated"
    psu_watt: int = 450
    case_format: str = "ATX"
