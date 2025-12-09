# presenter/inventory_presenter.py
from model.devices import Device
from view.app_view import AppView
from view.plot_view import PlotView
import random
import string

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
    
    def generate_random_devices(self, count=5):
        """Generate random devices with different values."""
        device_names = [
            "Dell XPS", "HP Pavilion", "Lenovo ThinkPad", "ASUS VivoBook", "MacBook Pro",
            "Samsung Galaxy Tab", "iPad Air", "Surface Pro", "Razer Blade", "MSI GS66"
        ]
        models = [
            "13", "14", "15", "16", "17", "Pro", "Max", "Plus", "Ultra", "Gaming"
        ]
        categories = ["Laptop", "Tablet", "PC"]
        videocards = [
            "NVIDIA GTX 1050", "NVIDIA RTX 3050", "NVIDIA RTX 3060", "AMD Radeon RX 5500",
            "Intel Iris Xe", "NVIDIA GTX 1080", "NVIDIA RTX 4060", "AMD Radeon RX 6600"
        ]
        
        for i in range(count):
            kwargs = {
                "name": f"{random.choice(device_names)} {i+1}",
                "model": random.choice(models),
                "category": random.choice(categories),
                "videocard_type": random.choice(videocards),
                "price": str(round(random.uniform(500, 3000), 2))
            }
            self.add_device(kwargs)

    def run(self):
        self.view.mainloop()
