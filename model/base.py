# model/base.py
from dataclasses import dataclass

@dataclass
class BaseDevice:
    category: str = "Device"

    def short(self):
        """Simple string representation shown in UI."""
        fields = vars(self)
        parts = [f"{k}={v}" for k, v in fields.items()]
        return f"{self.category}: " + ", ".join(parts)
