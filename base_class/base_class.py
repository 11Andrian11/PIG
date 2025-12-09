from dataclasses import dataclass, asdict

@dataclass
class BaseDevice:
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
