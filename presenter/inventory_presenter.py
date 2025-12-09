# presenter/inventory_presenter.py
from model.devices import Device
from model.inventory import InventoryModel
from view.app_view import AppView
from view.plot_view import PlotView
import random


class InventoryPresenter:
    def __init__(self):
        self.inventory = InventoryModel()
        self.view = AppView(self)

    @property
    def devices(self):
        """Return current list of devices (keeps compatibility with previous code)."""
        return self.inventory.all()

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
            saved = self.inventory.add(device)
            devices = self.inventory.all()
            self.view.refresh_frames(devices)
        except Exception as e:
            self.view.show_error(f"Failed to add device: {e}")

    def edit_device(self, device, kwargs):
        try:
            # update fields
            device.name = kwargs.get("name", device.name)
            device.model = kwargs.get("model", device.model)
            device.category = kwargs.get("category", device.category)
            device.videocard_type = kwargs.get("videocard_type", device.videocard_type)
            device.price = float(kwargs.get("price", device.price))

            # persist changes
            # Re-use InventoryModel's add (session.add will merge/attach)
            self.inventory.add(device)
            devices = self.inventory.all()
            self.view.refresh_frames(devices)
        except Exception as e:
            self.view.show_error(f"Failed to edit device: {e}")

    def delete_device(self, device):
        try:
            self.inventory.remove(device)
            devices = self.inventory.all()
            self.view.refresh_frames(devices)
        except Exception as e:
            self.view.show_error(f"Failed to delete device: {e}")

    def generate_random_devices(self, count=5):
        """Generate random devices with different values and persist them."""
        device_names = [
            "Dell XPS", "HP Pavilion", "Lenovo ThinkPad", "ASUS VivoBook", "MacBook Pro",
            "Samsung Galaxy Tab", "iPad Air", "Surface Pro", "Razer Blade", "MSI GS66"
        ]
        models = [
            "13", "14", "15", "16", "Pro", "Max", "Plus", "Ultra", "Gaming"
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
        # populate view with current DB items
        devices = self.inventory.all()
        self.view.refresh_frames(devices)
        self.view.mainloop()
