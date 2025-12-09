# model/device.py
class Device:
    def __init__(self, name, model, category, videocart_type, price):
        self.name = name
        self.model = model
        self.category = category
        self.videocard_type = videocart_type
        self.price = float(price)

    def short(self):
        return f"{self.name} | {self.model} | {self.category} | {self.videocard_type} | {self.price}€"
