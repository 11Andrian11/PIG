from interface import App, InventoryModel

if __name__ == "__main__":
    model = InventoryModel()
    app = App(model)
    app.mainloop()
