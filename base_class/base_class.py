# model/base.py
from dataclasses import dataclass

@dataclass
class BaseDevice:
<<<<<<< HEAD:model/base.py
    category: str = "Device"

    def short(self):
        """Simple string representation shown in UI."""
        fields = vars(self)
        parts = [f"{k}={v}" for k, v in fields.items()]
        return f"{self.category}: " + ", ".join(parts)
=======
    name: str
    cpu: str
    ram_gb: int
    storage_gb: int
    price: float

    category: str = "Device"  # overridden by subclasses

    def to_dict(self) -> dict:
        d = asdict(self)
        d["category"] = self.category
        return d

    def short(self) -> str:
        return f"{self.category}: {self.name} | {self.cpu} | {self.ram_gb}GB RAM | {self.storage_gb}GB | ${self.price:.2f}"
>>>>>>> parent of 8bfd4a8 (lab3):base_class/base_class.py
