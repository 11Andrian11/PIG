<<<<<<< HEAD
from presenter.inventory_presenter import InventoryPresenter

if __name__ == "__main__":
    app = InventoryPresenter()
    app.run()
=======
from interface import App, InventoryModel

if __name__ == "__main__":
    model = InventoryModel()
    app = App(model)
    app.mainloop()
>>>>>>> parent of 8bfd4a8 (lab3)
