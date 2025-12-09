# model/devices.py
from sqlalchemy import Column, Integer, String, Float
from .db import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=True)
    category = Column(String, nullable=True)
    videocard_type = Column(String, nullable=True)
    price = Column(Float, nullable=True)

    def __init__(self, name, model, category, videocart_type, price):
        self.name = name
        self.model = model
        self.category = category
        self.videocard_type = videocart_type
        try:
            self.price = float(price)
        except Exception:
            self.price = None

    def short(self):
        return f"{self.name} | {self.model} | {self.category} | {self.videocard_type} | {self.price}€"
