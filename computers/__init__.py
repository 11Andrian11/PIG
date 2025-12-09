from .laptop import Laptop
from .pc import PC
from .tablet import Tablet

DEVICE_TYPES = {
    "Laptop": Laptop,
    "PC": PC,
    "Tablet": Tablet,
}
