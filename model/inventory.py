# model/inventory.py
from typing import List
from .devices import Device
from .db import get_session, init_db
init_db()  # ensures tables exist


class InventoryModel:
    def __init__(self):
        pass

    def add(self, device: Device):
        """Persist a device to the DB."""
        session = get_session()
        try:
            session.add(device)
            session.commit()
            session.refresh(device)
            return device
        finally:
            session.close()

    def remove(self, device: Device):
        session = get_session()
        try:
            obj = session.query(Device).get(device.id)
            if obj:
                session.delete(obj)
                session.commit()
        finally:
            session.close()

    def all(self) -> List[Device]:
        session = get_session()
        try:
            return session.query(Device).all()
        finally:
            session.close()
