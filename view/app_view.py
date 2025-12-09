import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Tuple, Optional, List

from model import DEVICE_TYPES, BaseDevice

Row = Tuple[int, str, str, str, int, int, float, str]

class AppView(ctk.CTk):
    """
    View = pure UI. Knows how to draw widgets and collect/show data.
    Delegates all logic to Presenter via callbacks.
    """
    def __init__(self):
        super().__init__()
        self.title("Device Inventory — MVP (Dark)")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.geometry("1100x640")

        self.presenter = None  # set via set_presenter()
        self._selected_row_index: Optional[int] = None

        self._build_menu()
        self._build_ui()

    # ---------- MVP wiring ----------
    def set_presenter(self, presenter) -> None:
        self.presenter = presenter

    # ---------- Menu ----------
    def _build_menu(self):
        self.option_add('*tearOff', False)
        menubar = tk.Menu(self, bg="#1c1c1c", fg="white", activebackground="#333333", activeforeground="white")
        gen_menu = tk.Menu(menubar, bg="#1c1c1c", fg="white", activebackground="#333333", activeforeground="white")
        gen_menu.add_command(label="30 devices (10×each)    Ctrl+G", command=self._on_generate_30)
        menubar.add_cascade(label="Generate", menu=gen_menu)
        self.configure(menu=menubar)
        # shortcut
        self.bind_all("<Control-g>", lambda e: self._on_generate_30())

    # ---------- UI ----------
    def _build_ui(self):
        # Left
        left = ctk.CTkFrame(self, corner_radius=16)
        left.pack(side="left", fill="y", padx=12, pady=12)

        ctk.CTkLabel(left, text="Add / Edit Device", font=ctk.CTkFont(size=18, weight="bold")).pack(padx=12, pady=(12, 6))

        self.var_type = ctk.StringVar(value="Laptop")
        ctk.CTkLabel(left, text="Type").pack(anchor="w", padx=12)
        self.cb_type = ctk.CTkOptionMenu(
            left,
            values=list(DEVICE_TYPES.keys()),
            variable=self.var_type,
            command=self._on_type_changed,  # delegate to presenter
        )
        self.cb_type.pack(fill="x", padx=12, pady=(0, 8))
        self.var_type.trace_add("write", lambda *_: self._on_type_changed(self.var_type.get()))

        self.ent_name = self._labeled_entry(left, "Name")
        self.ent_cpu = self._labeled_entry(left, "CPU")
        self.ent_ram = self._labeled_entry(left, "RAM (GB)")
        self.ent_storage = self._labeled_entry(left, "Storage (GB)")
        self.ent_price = self._labeled_entry(left, "Price ($)")

        self.opt_container = ctk.CTkFrame(left)
        self.opt_container.pack(fill="x", padx=12, pady=(4, 8))
        self.optional_widgets: Dict[str, ctk.CTkEntry] = {}
        self.show_optional_fields_for_type(self.var_type.get())

        btns = ctk.CTkFrame(left)
        btns.pack(fill="x", padx=12, pady=8)

        ctk.CTkButton(btns, text="Add Device", command=self._on_add).pack(fill="x", padx=4, pady=4)
        ctk.CTkButton(btns, text="Update Selected", command=self._on_update).pack(fill="x", padx=4, pady=4)
        ctk.CTkButton(btns, text="Delete Selected", fg_color="#8B0000", hover_color="#a32626",
                      command=self._on_delete).pack(fill="x", padx=4, pady=4)
        ctk.CTkButton(btns, text="Add 30 Devices (10 × each)", command=self._on_generate_30).pack(fill="x", padx=4, pady=4)

        # Right
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

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    # ---------- View helpers ----------
    def _labeled_entry(self, parent, label):
        ctk.CTkLabel(parent, text=label).pack(anchor="w", padx=12)
        ent = ctk.CTkEntry(parent)
        ent.pack(fill="x", padx=12, pady=(0, 8))
        return ent

    def show_optional_fields_for_type(self, dev_type: str):
        for w in self.opt_container.winfo_children():
            w.destroy()
        self.optional_widgets.clear()

        def add(label_key: str, label_text: str):
            self.optional_widgets[label_key] = self._labeled_entry(self.opt_container, label_text)

        if dev_type == "Laptop":
            add("gpu", "GPU")
            add("screen_inch", "Screen (inch)")
            add("battery_wh", "Battery (Wh)")
        elif dev_type == "PC":
            add("gpu", "GPU")
            add("psu_watt", "PSU (Watt)")
            add("case_format", "Case Format")
        elif dev_type == "Tablet":
            add("screen_inch", "Screen (inch)")
            add("battery_wh", "Battery (Wh)")

    # data API for Presenter
    def get_current_form_data(self) -> Tuple[str, dict]:
        dtype = self.var_type.get()
        name = self.ent_name.get().strip()
        cpu = self.ent_cpu.get().strip()
        if not name or not cpu:
            raise ValueError("Name and CPU are required.")
        try:
            ram = int(self.ent_ram.get().strip())
            storage = int(self.ent_storage.get().strip())
            price = float(self.ent_price.get().strip())
        except Exception:
            raise ValueError("RAM, Storage must be integers; Price must be a number.")

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
        return dtype, kwargs

    def fill_form_from_device(self, dev: BaseDevice) -> None:
        dtype = getattr(dev, "category", "Laptop")
        if dtype not in DEVICE_TYPES:
            dtype = "Laptop"
        self.var_type.set(dtype)
        self.show_optional_fields_for_type(dtype)

        def set_entry(entry: ctk.CTkEntry, value: str):
            entry.delete(0, "end")
            entry.insert(0, value)

        set_entry(self.ent_name, dev.name)
        set_entry(self.ent_cpu, dev.cpu)
        set_entry(self.ent_ram, str(dev.ram_gb))
        set_entry(self.ent_storage, str(dev.storage_gb))
        set_entry(self.ent_price, str(dev.price))

        def maybe(key, value):
            if key in self.optional_widgets and value is not None:
                set_entry(self.optional_widgets[key], str(value))

        maybe("gpu", getattr(dev, "gpu", None))
        maybe("screen_inch", getattr(dev, "screen_inch", None))
        maybe("battery_wh", getattr(dev, "battery_wh", None))
        maybe("psu_watt", getattr(dev, "psu_watt", None))
        maybe("case_format", getattr(dev, "case_format", None))

    def clear_form(self):
        self.var_type.set("Laptop")
        self.show_optional_fields_for_type("Laptop")
        for ent in (self.ent_name, self.ent_cpu, self.ent_ram, self.ent_storage, self.ent_price):
            ent.delete(0, "end")
        for w in self.optional_widgets.values():
            w.delete(0, "end")

    def refresh_table(self, rows: List[Row], keep_selection: bool = True) -> None:
        prev = self._selected_row_index if keep_selection else None
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        for row in rows:
            self.tree.insert("", "end", values=row)
        if prev is not None:
            # try reselect by index value
            for iid in self.tree.get_children():
                if int(self.tree.item(iid, "values")[0]) == prev:
                    self.tree.selection_set(iid)
                    break

    def get_selected_index(self) -> Optional[int]:
        sel = self.tree.selection()
        if not sel:
            return None
        iid = sel[0]
        try:
            return int(self.tree.item(iid, "values")[0])
        except Exception:
            return None

    def show_error(self, msg: str) -> None:
        messagebox.showerror("Error", msg, parent=self)

    def show_info(self, msg: str) -> None:
        messagebox.showinfo("Info", msg, parent=self)

    # ---------- event plumbing to Presenter ----------
    def _on_type_changed(self, value: str):
        if self.presenter:
            self.presenter.on_type_changed(value)

    def _on_add(self):
        if self.presenter:
            self.presenter.on_add_clicked()

    def _on_update(self):
        if self.presenter:
            self.presenter.on_update_clicked()

    def _on_delete(self):
        if self.presenter:
            self.presenter.on_delete_clicked()

    def _on_generate_30(self):
        if self.presenter:
            self.presenter.on_generate_30_each()

    def _on_tree_select(self, _event=None):
        self._selected_row_index = self.get_selected_index()
        if self.presenter and self._selected_row_index is not None:
            self.presenter.on_row_selected(self._selected_row_index)
