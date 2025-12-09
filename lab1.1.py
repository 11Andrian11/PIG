import random
import customtkinter as ctk

# -----------------------------
# Domain model (inheritance demo)
# -----------------------------
class Computer:
    def __init__(self, cpu: str, ram_gb: int, storage_gb: int):
        self.cpu = cpu
        self.ram_gb = int(ram_gb)
        self.storage_gb = int(storage_gb)

    # base parameters setter
    def set_parameters(self, cpu=None, ram_gb=None, storage_gb=None):
        if cpu:
            self.cpu = cpu
        if ram_gb is not None and str(ram_gb) != "":
            self.ram_gb = int(ram_gb)
        if storage_gb is not None and str(storage_gb) != "":
            self.storage_gb = int(storage_gb)

    def get_info(self) -> str:
        return f"CPU: {self.cpu}, RAM: {self.ram_gb}GB, Storage: {self.storage_gb}GB"


class GamingComputer(Computer):
    def __init__(self, cpu: str, ram_gb: int, storage_gb: int, gpu: str):
        super().__init__(cpu, ram_gb, storage_gb)
        self.gpu = gpu

    def set_parameters(self, gpu=None, **kwargs):
        super().set_parameters(**kwargs)
        if gpu:
            self.gpu = gpu

    def get_info(self) -> str:
        return f"[Gaming] {super().get_info()}, GPU: {self.gpu}"


class WorkstationComputer(Computer):
    def __init__(self, cpu: str, ram_gb: int, storage_gb: int, software: str):
        super().__init__(cpu, ram_gb, storage_gb)
        self.software = software

    def set_parameters(self, software=None, **kwargs):
        super().set_parameters(**kwargs)
        if software:
            self.software = software

    def get_info(self) -> str:
        return f"[Workstation] {super().get_info()}, Software: {self.software}"


class ServerComputer(Computer):
    def __init__(self, cpu: str, ram_gb: int, storage_gb: int, network_gbps: float):
        super().__init__(cpu, ram_gb, storage_gb)
        self.network_gbps = float(network_gbps)

    def set_parameters(self, network_gbps=None, **kwargs):
        super().set_parameters(**kwargs)
        if network_gbps is not None and str(network_gbps) != "":
            self.network_gbps = float(network_gbps)

    def get_info(self) -> str:
        return f"[Server] {super().get_info()}, Network: {self.network_gbps:g} Gbps"


# -----------------------------
# GUI application (CustomTkinter)
# -----------------------------
class ComputerManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter — Computer Manager")
        self.geometry("1080x640")

        # global appearance & theme
        ctk.set_appearance_mode("system")  # "light" | "dark" | "system"
        ctk.set_default_color_theme("dark-blue")  # "blue" | "dark-blue" | "green" or your JSON

        # data store
        self.objects: list[Computer] = []

        # grid layout: 0=sidebar, 1=growing content
        self.grid_columnconfigure(0, weight=0, minsize=340)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_list_panel()

    # ---------- UI building blocks ----------
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, corner_radius=12)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self.sidebar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.sidebar, text="Computer Editor", font=("Segoe UI", 20, "bold")).grid(
            row=0, column=0, pady=(12, 4)
        )
        ctk.CTkLabel(self.sidebar, text="Create / modify objects and refresh the list").grid(
            row=1, column=0, pady=(0, 16)
        )

        # type selector
        self.type_var = ctk.StringVar(value="Gaming")
        ctk.CTkLabel(self.sidebar, text="Type").grid(row=2, column=0, sticky="w", padx=8)
        self.type_menu = ctk.CTkOptionMenu(self.sidebar, variable=self.type_var,
                                           values=["Gaming", "Workstation", "Server"],
                                           command=self._on_type_change)
        self.type_menu.grid(row=3, column=0, sticky="ew", padx=8, pady=(0, 8))

        # base params
        self.cpu_var = ctk.StringVar(value="Intel i5-12400")
        self.ram_var = ctk.StringVar(value="16")
        self.storage_var = ctk.StringVar(value="512")

        self._labeled_entry(self.sidebar, "CPU", self.cpu_var, row=4)
        self._labeled_entry(self.sidebar, "RAM (GB)", self.ram_var, row=5)
        self._labeled_entry(self.sidebar, "Storage (GB)", self.storage_var, row=6)

        # subtype-specific fields container
        self.subtype_frame = ctk.CTkFrame(self.sidebar)
        self.subtype_frame.grid(row=7, column=0, sticky="ew", padx=8, pady=(4, 8))
        self.subtype_frame.grid_columnconfigure(0, weight=1)

        # three variant fields (only one visible at a time)
        self.gpu_var = ctk.StringVar(value="NVIDIA RTX 4070")
        self.software_var = ctk.StringVar(value="AutoCAD")
        self.net_var = ctk.StringVar(value="10")

        self.gpu_row = self._labeled_entry(self.subtype_frame, "GPU", self.gpu_var, row=0)
        self.software_row = self._labeled_entry(self.subtype_frame, "Software", self.software_var, row=0)
        self.net_row = self._labeled_entry(self.subtype_frame, "Network (Gbps)", self.net_var, row=0)
        self._show_only("Gaming")

        # action buttons
        self.add_btn = ctk.CTkButton(self.sidebar, text="Add Object", command=self._add_object)
        self.add_btn.grid(row=8, column=0, sticky="ew", padx=8, pady=(8, 4))

        # update section
        ctk.CTkLabel(self.sidebar, text="Update by index").grid(row=9, column=0, sticky="w", padx=8, pady=(8, 0))
        idx_frame = ctk.CTkFrame(self.sidebar)
        idx_frame.grid(row=10, column=0, sticky="ew", padx=8, pady=4)
        idx_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(idx_frame, text="#").grid(row=0, column=0, padx=(8, 6))
        self.index_var = ctk.StringVar(value="0")
        self.index_entry = ctk.CTkEntry(idx_frame, textvariable=self.index_var, width=60)
        self.index_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=6)
        self.update_btn = ctk.CTkButton(self.sidebar, text="Update Selected", command=self._update_selected)
        self.update_btn.grid(row=11, column=0, sticky="ew", padx=8, pady=4)

        # utilities
        util_frame = ctk.CTkFrame(self.sidebar)
        util_frame.grid(row=12, column=0, sticky="ew", padx=8, pady=(8, 8))
        util_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(util_frame, text="Populate 30 demo", command=self._populate_demo).grid(
            row=0, column=0, sticky="ew", padx=6, pady=6
        )
        ctk.CTkButton(util_frame, text="Clear all", fg_color="gray30", command=self._clear_all).grid(
            row=0, column=1, sticky="ew", padx=6, pady=6
        )

        # appearance controls
        ctk.CTkLabel(self.sidebar, text="Appearance").grid(row=13, column=0, sticky="w", padx=8)
        self.appearance_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["System", "Light", "Dark"],
            command=lambda m: ctk.set_appearance_mode(m.lower())
        )
        self.appearance_menu.set("System")
        self.appearance_menu.grid(row=14, column=0, sticky="ew", padx=8, pady=(0, 8))

        ctk.CTkLabel(self.sidebar, text="UI Scaling").grid(row=15, column=0, sticky="w", padx=8)
        self.scale_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=lambda s: ctk.set_widget_scaling(int(s.rstrip('%'))/100)
        )
        self.scale_menu.set("100%")
        self.scale_menu.grid(row=16, column=0, sticky="ew", padx=8, pady=(0, 12))

    def _build_list_panel(self):
        self.list_panel = ctk.CTkFrame(self, corner_radius=12)
        self.list_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)
        self.list_panel.grid_columnconfigure(0, weight=1)
        self.list_panel.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self.list_panel)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 6))
        header.grid_columnconfigure((0,1,2), weight=1)
        ctk.CTkLabel(header, text="Objects (0)", font=("Segoe UI", 18, "bold"), anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="Refresh", width=90, command=self._refresh_view).grid(row=0, column=2, sticky="e")

        # simple list using CTkTextbox
        self.textbox = ctk.CTkTextbox(self.list_panel, wrap="none")
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.textbox.configure(state="disabled")

    # ---------- helpers ----------
    def _labeled_entry(self, parent, label, var, row):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", padx=8, pady=4)
        frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(frame, text=label, width=110, anchor="w").grid(row=0, column=0, padx=(2, 6))
        entry = ctk.CTkEntry(frame, textvariable=var)
        entry.grid(row=0, column=1, sticky="ew")
        return frame

    def _show_only(self, which: str):
        # hide all first
        for f in (self.gpu_row, self.software_row, self.net_row):
            f.grid_remove()
        # then show the one we need
        if which == "Gaming":
            self.gpu_row.grid()
        elif which == "Workstation":
            self.software_row.grid()
        elif which == "Server":
            self.net_row.grid()

    def _on_type_change(self, choice: str):
        self._show_only(choice)

    # ---------- actions ----------
    def _add_object(self):
        try:
            cpu = self.cpu_var.get().strip()
            ram = int(self.ram_var.get())
            storage = int(self.storage_var.get())
            kind = self.type_var.get()

            if kind == "Gaming":
                obj = GamingComputer(cpu, ram, storage, self.gpu_var.get().strip())
            elif kind == "Workstation":
                obj = WorkstationComputer(cpu, ram, storage, self.software_var.get().strip())
            else:
                obj = ServerComputer(cpu, ram, storage, float(self.net_var.get()))

            self.objects.append(obj)
            print(f"Added -> {obj.get_info()}")  # also print to terminal
            self._refresh_view()
        except Exception as e:
            self._message(f"Failed to add object: {e}")

    def _update_selected(self):
        try:
            idx = int(self.index_var.get())
            if not (0 <= idx < len(self.objects)):
                raise IndexError("index out of range")

            obj = self.objects[idx]
            # update base params (empty means keep)
            self.objects[idx].set_parameters(
                cpu=self.cpu_var.get().strip() or None,
                ram_gb=self.ram_var.get().strip() or None,
                storage_gb=self.storage_var.get().strip() or None,
            )
            # update subtype if field not empty
            if isinstance(obj, GamingComputer):
                self.objects[idx].set_parameters(gpu=self.gpu_var.get().strip() or None)
            elif isinstance(obj, WorkstationComputer):
                self.objects[idx].set_parameters(software=self.software_var.get().strip() or None)
            elif isinstance(obj, ServerComputer):
                net_val = self.net_var.get().strip()
                self.objects[idx].set_parameters(network_gbps=float(net_val) if net_val else None)

            print(f"Updated #{idx} -> {self.objects[idx].get_info()}")
            self._refresh_view()
        except Exception as e:
            self._message(f"Failed to update: {e}")

    def _populate_demo(self):
        self.objects.clear()
        # 10 Gaming
        for i in range(10):
            self.objects.append(
                GamingComputer(
                    cpu=f"Intel i7-{9800 + i}",
                    ram_gb=random.choice([16, 32]),
                    storage_gb=random.choice([512, 1024]),
                    gpu=f"NVIDIA RTX {random.choice([3060, 3070, 3080, 4060, 4070])}"
                )
            )
        # 10 Workstation
        for i in range(10):
            self.objects.append(
                WorkstationComputer(
                    cpu=f"Ryzen 7 {5700 + i}",
                    ram_gb=random.choice([32, 64]),
                    storage_gb=random.choice([1024, 2048]),
                    software=random.choice(["MATLAB", "SolidWorks", "AutoCAD"])
                )
            )
        # 10 Server
        for i in range(10):
            self.objects.append(
                ServerComputer(
                    cpu=f"Xeon Silver {4200 + i}",
                    ram_gb=random.choice([64, 128, 256]),
                    storage_gb=random.choice([2048, 4096]),
                    network_gbps=random.choice([1, 10, 25, 40])
                )
            )
        print("Populated with 30 demo objects.")
        self._refresh_view()

    def _clear_all(self):
        self.objects.clear()
        self._refresh_view()

    def _refresh_view(self):
        # update header count
        header_label = self.list_panel.grid_slaves(row=0, column=0)[0].grid_slaves(row=0, column=0)[0]
        header_label.configure(text=f"Objects ({len(self.objects)})")

        # rebuild textbox
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        for i, obj in enumerate(self.objects):
            self.textbox.insert("end", f"{i:02d}. {obj.get_info()}\n")
        self.textbox.configure(state="disabled")

    def _message(self, text: str):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Message")
        dlg.geometry("360x120")
        ctk.CTkLabel(dlg, text=text, wraplength=320).pack(padx=16, pady=16)
        ctk.CTkButton(dlg, text="OK", command=dlg.destroy).pack(pady=(0, 12))


if __name__ == "__main__":
    app = ComputerManagerApp()
    app.mainloop()
