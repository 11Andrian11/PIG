# presenter/inventory_presenter.py
from model.devices import Device
from view.app_view import AppView

class InventoryPresenter:
    def __init__(self):
        self.devices = []  
        self.view = AppView(self)

    # accept a dictionary from the popup
    def add_device(self, kwargs):
        try:
            device = Device(
                name=kwargs["name"],
                model=kwargs["model"],
                category=kwargs["category"],
                videocart_type=kwargs["videocard_type"],
                price=kwargs["price"]
            )
            self.devices.append(device)
            self.view.refresh_frames(self.devices)
        except Exception as e:
            self.view.show_error(f"Failed to add device: {e}")

    def edit_device(self, device, kwargs):
        try:
            if device not in self.devices:
                raise ValueError("Device not found")

            device.name = kwargs.get("name", device.name)
            device.model = kwargs.get("model", device.model)
            device.category = kwargs.get("category", device.category)
            device.videocard_type = kwargs.get("videocard_type", device.videocard_type)
            device.price = float(kwargs.get("price", device.price))

            self.view.refresh_frames(self.devices)
        except Exception as e:
            self.view.show_error(f"Failed to edit device: {e}")

    def delete_device(self, device):
        if device in self.devices:
            self.devices.remove(device)
            self.view.refresh_frames(self.devices)

    def run(self):
        self.view.mainloop()
