from __future__ import annotations
from typing import List, Tuple
import random

from model import InventoryModel, DEVICE_TYPES, Laptop, PC, Tablet, BaseDevice

Row = Tuple[int, str, str, str, int, int, float, str]  # (#, Type, Name, CPU, RAM, Storage, Price, Extra)

class InventoryPresenter:
    """
    Presenter glues Model <-> View. It owns the business logic.
    The View calls presenter handlers; the Presenter updates Model and instructs View.
    """
    def __init__(self, model: InventoryModel, view):
        self.model = model
        self.view = view
        self.view.set_presenter(self)
        self.refresh_table()

    # ---------- Formatting ----------
    def _build_rows(self) -> List[Row]:
        rows: List[Row] = []
        for i, d in enumerate(self.model.all()):
            dd = d.to_dict()
            extra = ""
            for k in ("gpu", "screen_inch", "battery_wh", "psu_watt", "case_format"):
                if k in dd:
                    extra = dd[k]
                    break
            rows.append((
                i,
                dd.get("category", ""),
                dd.get("name", ""),
                dd.get("cpu", ""),
                int(dd.get("ram_gb", 0)),
                int(dd.get("storage_gb", 0)),
                float(dd.get("price", 0.0)),
                extra,
            ))
        return rows

    def refresh_table(self, keep_selection: bool = True) -> None:
        rows = self._build_rows()
        self.view.refresh_table(rows, keep_selection=keep_selection)

    # ---------- Event handlers from View ----------
    def on_type_changed(self, new_type: str) -> None:
        # UI logic belongs in View; Presenter just validates/mediates if needed.
        if new_type not in DEVICE_TYPES:
            self.view.show_error(f"Unknown type: {new_type}")
            return
        self.view.show_optional_fields_for_type(new_type)

    def on_add_clicked(self) -> None:
        try:
            dtype, kwargs = self.view.get_current_form_data()
            cls = DEVICE_TYPES[dtype]
            self.model.add(cls(**kwargs))
            self.refresh_table()
            self.view.clear_form()
        except Exception as e:
            self.view.show_error(str(e))

    def on_update_clicked(self) -> None:
        idx = self.view.get_selected_index()
        if idx is None:
            self.view.show_info("Select a device to update.")
            return
        try:
            dtype, kwargs = self.view.get_current_form_data()
            cls = DEVICE_TYPES[dtype]
            self.model.set_index(idx, cls(**kwargs))
            self.refresh_table()
        except Exception as e:
            self.view.show_error(str(e))

    def on_delete_clicked(self) -> None:
        idx = self.view.get_selected_index()
        if idx is None:
            return
        self.model.remove_index(idx)
        self.refresh_table(keep_selection=False)
        self.view.clear_form()

    def on_row_selected(self, idx: int) -> None:
        dev = self.model.get_index(idx)
        if dev is None:
            return
        self.view.fill_form_from_device(dev)

    def on_generate_30_each(self) -> None:
        cpus_laptop = ["i5-1240P", "i7-1260P", "Ryzen 5 7640U", "Ryzen 7 7840U"]
        cpus_pc = ["i3-12100F", "i5-13400F", "i7-12700", "Ryzen 5 5600", "Ryzen 7 5800X"]
        cpus_tab = ["Snap 6 Gen 1", "Snap 7 Gen 1", "Apple M1", "Apple M2"]
        gpus = ["Integrated", "RTX 3050", "RTX 3060", "RTX 4060"]
        cases = ["ATX", "mATX", "ITX"]

        for i in range(10):
            self.model.add(Laptop(
                name=f"Laptop {i+1}",
                cpu=random.choice(cpus_laptop),
                ram_gb=random.choice([8, 16, 32]),
                storage_gb=random.choice([256, 512, 1000, 2000]),
                price=round(random.uniform(499, 1999), 2),
                gpu=random.choice(gpus),
                screen_inch=random.choice([13.3, 14.0, 15.6, 16.0]),
                battery_wh=random.choice([45, 58, 70, 80])
            ))
        for i in range(10):
            self.model.add(PC(
                name=f"PC {i+1}",
                cpu=random.choice(cpus_pc),
                ram_gb=random.choice([8, 16, 32, 64]),
                storage_gb=random.choice([512, 1000, 2000, 4000]),
                price=round(random.uniform(399, 2499), 2),
                gpu=random.choice(gpus),
                psu_watt=random.choice([450, 550, 650, 750]),
                case_format=random.choice(cases)
            ))
        for i in range(10):
            self.model.add(Tablet(
                name=f"Tablet {i+1}",
                cpu=random.choice(cpus_tab),
                ram_gb=random.choice([4, 6, 8, 12]),
                storage_gb=random.choice([64, 128, 256, 512]),
                price=round(random.uniform(199, 1299), 2),
                screen_inch=random.choice([10.1, 10.5, 11.0, 12.9]),
                battery_wh=random.choice([25, 28, 32, 40])
            ))
        self.refresh_table()
