from presenter.inventory_presenter import InventoryPresenter
from model.db import init_db
import sys, os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS   # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Example
img_delete = resource_path("images/delete.png")
img_edit = resource_path("images/edit.png")

if __name__ == "__main__":
    # ensure DB + tables exist
    init_db()
    app = InventoryPresenter()
    app.run()
