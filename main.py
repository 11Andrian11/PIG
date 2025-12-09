from model import InventoryModel
from view import AppView
from presenter import InventoryPresenter

def main():
    model = InventoryModel()
    view = AppView()
    InventoryPresenter(model, view)  # wires everything
    view.mainloop()

if __name__ == "__main__":
    main()
