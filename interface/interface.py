import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from typing import List, Type, Optional
import random

from computers import DEVICE_TYPES
from base_class import BaseDevice

class InventoryModel:
    def __init__(self):
        self.items: List[BaseDevice] = []

    def add(self, dev: BaseDevice):
        self.items.append(dev)

    def remove_index(self, idx: int):
        if 0 <= idx < len(self.items):
            self.items.pop(idx)

    def set_index(self, idx: int, dev: BaseDevice):
        if 0 <= idx < len(self.items):
            self.items[idx] = dev

    def get_index(self, idx: int) -> Optional[BaseDevice]:
        if 0 <= idx < len(self.items):
            return self.items[idx]
        return None

    def as_rows(self):
        for i, d in enumerate(self.items):
            dd = d.to_dict()
            extra = ""
            for k in ("gpu", "screen_inch", "battery_wh", "psu_watt", "case_format"):
                if k in dd:
                    extra = dd[k]
                    break
            yield (
                i,
                dd.get("category", ""),
                dd.get("name", ""),
                dd.get("cpu", ""),
                dd.get("ram_gb", 0),
                dd.get("storage_gb", 0),
                dd.get("price", 0.0),
                extra,
            )

class App(ctk.CTk):
    def __init__(self, model: InventoryModel):
        super().__init__()
        self.title("Device Inventory — Dark Theme")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.geometry("1100x640")

        self.model = model
        self._selected_row_index: Optional[int] = None

        self._build_menu()
        self._build_ui()
        self.bind_all("<Control-g>", lambda e: self._add_30_per_type())

    # ---------- Menu ----------
    def _build_menu(self):
        self.option_add('*tearOff', False)
        menubar = tk.Menu(self, bg="#1c1c1c", fg="white", activebackground="#333333", activeforeground="white")
        gen_menu = tk.Menu(menubar, bg="#1c1c1c", fg="white", activebackground="#333333", activeforeground="white")
        gen_menu.add_command(label="30 devices (10×each)    Ctrl+G", command=self._add_30_per_type)
        menubar.add_cascade(label="Generate", menu=gen_menu)
        self.configure(menu=menubar)

    # ---------- UI ----------
    def _build_ui(self):
        # Left panel
        left = ctk.CTkFrame(self, corner_radius=16)
        left.pack(side="left", fill="y", padx=12, pady=12)

        title = ctk.CTkLabel(left, text="Add / Edit Device", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(padx=12, pady=(12, 6))

        self.var_type = ctk.StringVar(value="Laptop")
        ctk.CTkLabel(left, text="Type").pack(anchor="w", padx=12)

        self.cb_type = ctk.CTkOptionMenu(
            left,
            values=list(DEVICE_TYPES.keys()),
            variable=self.var_type,
            command=self._on_type_changed,  # <-- IMPORTANT
        )
        self.cb_type.pack(fill="x", padx=12, pady=(0, 8))

        # safety net: if the OptionMenu fails to fire command on your platform, trace will.
        self.var_type.trace_add("write", lambda *args: self._on_type_changed(self.var_type.get()))

        self.ent_name = self._labeled_entry(left, "Name")
        self.ent_cpu = self._labeled_entry(left, "CPU")
        self.ent_ram = self._labeled_entry(left, "RAM (GB)")
        self.ent_storage = self._labeled_entry(left, "Storage (GB)")
        self.ent_price = self._labeled_entry(left, "Price ($)")

        self.opt_container = ctk.CTkFrame(left)
        self.opt_container.pack(fill="x", padx=12, pady=(4, 8))
        self.optional_widgets = {}

        # initial optional fields build
        self._refresh_optional_fields(self.var_type.get())

        btns = ctk.CTkFrame(left)
        btns.pack(fill="x", padx=12, pady=8)

        add_btn = ctk.CTkButton(btns, text="Add Device", command=self._add_device)
        add_btn.pack(fill="x", padx=4, pady=4)

        update_btn = ctk.CTkButton(btns, text="Update Selected", command=self._update_selected)
        update_btn.pack(fill="x", padx=4, pady=4)

        del_btn = ctk.CTkButton(btns, text="Delete Selected", fg_color="#8B0000", hover_color="#a32626", command=self._delete_selected)
        del_btn.pack(fill="x", padx=4, pady=4)

        gen30_btn = ctk.CTkButton(btns, text="Add 30 Devices (10 × each)", command=self._add_30_per_type)
        gen30_btn.pack(fill="x", padx=4, pady=4)

        # Right panel
        right = ctk.CTkFrame(self, corner_radius=16)
        right.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(right, text="Inventory", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=12, pady=(12, 6))

        cols = ("#", "Type", "Name", "CPU", "RAM", "Storage", "Price", "Extra")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1c1c1c",
                        foreground="white",
                        fieldbackground="#1c1c1c",
                        rowheight=25,
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))
        style.map("Treeview", background=[("selected", "#444444")])

        self.tree = ttk.Treeview(right, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c)
        self.tree.column("#", width=50, anchor="center")
        self.tree.column("Type", width=90, anchor="center")
        self.tree.column("Name", width=170, anchor="center")
        self.tree.column("CPU", width=140, anchor="center")
        self.tree.column("RAM", width=70, anchor="center")
        self.tree.column("Storage", width=90, anchor="center")
        self.tree.column("Price", width=90, anchor="center")
        self.tree.column("Extra", width=160, anchor="center")

        vsb = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=(0, 12))
        vsb.pack(side="left", fill="y", padx=(0, 12), pady=(0, 12))

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        self._refresh_table()

    def _on_type_changed(self, value: str):
        """Called whenever the option menu changes OR var trace fires."""
        # ensure var reflects menu (some Tk variants can de-sync)
        if self.var_type.get() != value:
            self.var_type.set(value)
        self._refresh_optional_fields(value)

    def _labeled_entry(self, parent, label):
        ctk.CTkLabel(parent, text=label).pack(anchor="w", padx=12)
        ent = ctk.CTkEntry(parent)
        ent.pack(fill="x", padx=12, pady=(0, 8))
        return ent

    def _clear_opt(self):
        for w in self.opt_container.winfo_children():
            w.destroy()
        self.optional_widgets.clear()

    def _refresh_optional_fields(self, dev_type: str):
        self._clear_opt()
        if dev_type == "Laptop":
            self.optional_widgets["gpu"] = self._labeled_entry(self.opt_container, "GPU")
            self.optional_widgets["screen_inch"] = self._labeled_entry(self.opt_container, "Screen (inch)")
            self.optional_widgets["battery_wh"] = self._labeled_entry(self.opt_container, "Battery (Wh)")
        elif dev_type == "PC":
            self.optional_widgets["gpu"] = self._labeled_entry(self.opt_container, "GPU")
            self.optional_widgets["psu_watt"] = self._labeled_entry(self.opt_container, "PSU (Watt)")
            self.optional_widgets["case_format"] = self._labeled_entry(self.opt_container, "Case Format")
        elif dev_type == "Tablet":
            self.optional_widgets["screen_inch"] = self._labeled_entry(self.opt_container, "Screen (inch)")
            self.optional_widgets["battery_wh"] = self._labeled_entry(self.opt_container, "Battery (Wh)")

    # ---------- Actions ----------
    def _add_device(self):
        try:
            cls: Type[BaseDevice] = DEVICE_TYPES[self.var_type.get()]
            kwargs = self._collect_form_to_kwargs()
            self.model.add(cls(**kwargs))
            self._refresh_table()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Invalid input", str(e), parent=self)

    def _update_selected(self):
        if self._selected_row_index is None:
            messagebox.showinfo("No selection", "Select a device to update.", parent=self)
            return
        try:
            cls: Type[BaseDevice] = DEVICE_TYPES[self.var_type.get()]
            kwargs = self._collect_form_to_kwargs()
            self.model.set_index(self._selected_row_index, cls(**kwargs))
            self._refresh_table()
        except Exception as e:
            messagebox.showerror("Invalid input", str(e), parent=self)

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        idx = int(self.tree.item(iid, "values")[0])
        self.model.remove_index(idx)
        self._selected_row_index = None
        self._refresh_table()
        self._clear_form()

    def _on_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        idx = int(self.tree.item(iid, "values")[0])
        dev = self.model.get_index(idx)
        if dev is None:
            return
        self._selected_row_index = idx
        self._clear_form(keep_type=False)
        self._fill_form_from_device(dev)

    # --- Helpers for form ---
    def _fill_form_from_device(self, dev: BaseDevice):
        dtype = getattr(dev, "category", "Laptop")
        if dtype not in DEVICE_TYPES:
            dtype = "Laptop"
        self.var_type.set(dtype)
        self._refresh_optional_fields(dtype)

        self._set_entry(self.ent_name, dev.name)
        self._set_entry(self.ent_cpu, dev.cpu)
        self._set_entry(self.ent_ram, str(dev.ram_gb))
        self._set_entry(self.ent_storage, str(dev.storage_gb))
        self._set_entry(self.ent_price, str(dev.price))

        def maybe_set(key, value):
            if key in self.optional_widgets and value is not None:
                self._set_entry(self.optional_widgets[key], str(value))

        maybe_set("gpu", getattr(dev, "gpu", None))
        maybe_set("screen_inch", getattr(dev, "screen_inch", None))
        maybe_set("battery_wh", getattr(dev, "battery_wh", None))
        maybe_set("psu_watt", getattr(dev, "psu_watt", None))
        maybe_set("case_format", getattr(dev, "case_format", None))

    def _set_entry(self, widget: ctk.CTkEntry, value: str):
        widget.delete(0, "end")
        widget.insert(0, value)

    def _collect_form_to_kwargs(self):
        name = self.ent_name.get().strip()
        cpu = self.ent_cpu.get().strip()
        if not name or not cpu:
            raise ValueError("Name and CPU are required.")
        ram = int(self.ent_ram.get().strip())
        storage = int(self.ent_storage.get().strip())
        price = float(self.ent_price.get().strip())
        kwargs = {"name": name, "cpu": cpu, "ram_gb": ram, "storage_gb": storage, "price": price}
        for key, widget in self.optional_widgets.items():
            val = widget.get().strip()
            if val == "":
                continue
            if key in ("screen_inch",):
                kwargs[key] = float(val)
            elif key in ("battery_wh", "psu_watt"):
                kwargs[key] = int(val)
            else:
                kwargs[key] = val
        return kwargs

    def _add_30_per_type(self):
        from computers import Laptop, PC, Tablet
        cpus_laptop = ["i5-1240P", "i7-1260P", "Ryzen 5 7640U", "Ryzen 7 7840U"]
        cpus_pc = ["i3-12100F", "i5-13400F", "i7-12700", "Ryzen 5 5600", "Ryzen 7 5800X"]
        cpus_tab = ["Snap 6 Gen 1", "Snap 7 Gen 1", "Apple M1", "Apple M2"]
        gpus = ["Integrated", "RTX 3050", "RTX 3060", "RTX 4060"]
        cases = ["ATX", "mATX", "ITX"]

        for i in range(10):
            self.model.add(
                Laptop(
                    name=f"Laptop {i+1}",
                    cpu=random.choice(cpus_laptop),
                    ram_gb=random.choice([8, 16, 32]),
                    storage_gb=random.choice([256, 512, 1000, 2000]),
                    price=round(random.uniform(499, 1999), 2),
                    gpu=random.choice(gpus),
                    screen_inch=random.choice([13.3, 14.0, 15.6, 16.0]),
                    battery_wh=random.choice([45, 58, 70, 80])
                )
            )
        for i in range(10):
            self.model.add(
                PC(
                    name=f"PC {i+1}",
                    cpu=random.choice(cpus_pc),
                    ram_gb=random.choice([8, 16, 32, 64]),
                    storage_gb=random.choice([512, 1000, 2000, 4000]),
                    price=round(random.uniform(399, 2499), 2),
                    gpu=random.choice(gpus),
                    psu_watt=random.choice([450, 550, 650, 750]),
                    case_format=random.choice(cases)
                )
            )
        for i in range(10):
            self.model.add(
                Tablet(
                    name=f"Tablet {i+1}",
                    cpu=random.choice(cpus_tab),
                    ram_gb=random.choice([4, 6, 8, 12]),
                    storage_gb=random.choice([64, 128, 256, 512]),
                    price=round(random.uniform(199, 1299), 2),
                    screen_inch=random.choice([10.1, 10.5, 11.0, 12.9]),
                    battery_wh=random.choice([25, 28, 32, 40])
                )
            )
        self._refresh_table()

    def _refresh_table(self):
        prev = self._selected_row_index
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.model.as_rows():
            self.tree.insert("", "end", values=row)
        if prev is not None and 0 <= prev < len(self.model.items):
            for iid in self.tree.get_children():
                if int(self.tree.item(iid, "values")[0]) == prev:
                    self.tree.selection_set(iid)
                    break

    def _clear_form(self, keep_type=True):
        if not keep_type:
            self.var_type.set("Laptop")
            self._refresh_optional_fields("Laptop")
        for ent in (self.ent_name, self.ent_cpu, self.ent_ram, self.ent_storage, self.ent_price):
            ent.delete(0, "end")
        for w in self.optional_widgets.values():
            w.delete(0, "end")
