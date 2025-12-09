# view/app_view.py
import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageChops
import os
from view.plot_view import PlotView

def round_corners(image, radius=10, bg_tolerance=30):
    """Make solid background transparent (if present) and add rounded corners.

    - Detects background color from the top-left pixel and makes pixels
      within `bg_tolerance` transparent (useful for JPG icons with a flat bg).
    - Applies a rounded rectangle alpha mask of `radius` pixels.

    Returns a PIL RGBA image with proper transparency.
    """
    image = image.convert("RGBA")

    # Build a background mask by color-keying the top-left pixel
    bg_color = image.getpixel((0, 0))[:3]
    pixels = list(image.getdata())
    bg_mask_data = []
    for px in pixels:
        r, g, b, a = px
        if (abs(r - bg_color[0]) <= bg_tolerance
                and abs(g - bg_color[1]) <= bg_tolerance
                and abs(b - bg_color[2]) <= bg_tolerance):
            # treat as background -> transparent
            bg_mask_data.append(0)
        else:
            # keep original alpha
            bg_mask_data.append(a)

    bg_mask = Image.new("L", image.size)
    bg_mask.putdata(bg_mask_data)

    # Rounded mask
    round_mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(round_mask)
    draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)

    # Combine masks: keep pixels that are both not-background and inside rounded rect
    combined_mask = ImageChops.multiply(bg_mask, round_mask)

    # Apply final alpha
    image.putalpha(combined_mask)
    return image

class AppView(ctk.CTk):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter
        self.plot_view = PlotView(figsize=(8, 5), dpi=100)

        self.title("Device Inventory")
        self.geometry("800x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Load images for buttons with rounded corners
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        edit_pil_img = round_corners(Image.open(os.path.join(base_path, "images", "edit.jpg")), radius=8)
        delete_pil_img = round_corners(Image.open(os.path.join(base_path, "images", "delete.jpg")), radius=8)
        self.edit_img = CTkImage(edit_pil_img, size=(40, 40))
        self.delete_img = CTkImage(delete_pil_img, size=(40, 40))

        # Scrollable area
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Button frame for Add and Plot buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)
        
        # Add button
        self.add_btn = ctk.CTkButton(button_frame, text="Add Devices", command=self.open_add_popup)
        self.add_btn.pack(side="left", padx=5)
        
        # Show Plot button
        self.plot_btn = ctk.CTkButton(button_frame, text="Show Plot", command=self.show_price_plot)
        self.plot_btn.pack(side="left", padx=5)
        
        # Generate Random Devices button
        self.random_btn = ctk.CTkButton(button_frame, text="Generate Random", command=self.generate_random_devices)
        self.random_btn.pack(side="left", padx=5)

    def refresh_frames(self, devices):
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

        for dev in devices:
            frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#333333", corner_radius=10)
            frame.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(frame, text=dev.short(), anchor="w").pack(
                side="left", padx=10, pady=5, expand=True, fill="x"
            )

            # Right-side vertical button column: Edit above Delete
            btns_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btns_frame.pack(side="right", padx=10, pady=5)

            ctk.CTkButton(
                btns_frame,
                image=self.edit_img,
                text="",
                fg_color="#1E90FF",
                hover_color="#3EA0FF",
                width=40,
                height=40,
                command=lambda d=dev: self.open_edit_popup(d)
            ).pack(pady=(0,6))

            ctk.CTkButton(
                btns_frame,
                image=self.delete_img,
                text="",
                fg_color="#8B0000",
                hover_color="#A32626",
                width=40,
                height=40,
                command=lambda d=dev: self.presenter.delete_device(d)
            ).pack()

    def show_error(self, message):
        messagebox.showerror("Error", message)
    
    def generate_random_devices(self):
        """Generate random devices with a popup asking for count."""
        popup = ctk.CTkToplevel(self)
        popup.title("Generate Random Devices")
        popup.geometry("300x150")
        popup.resizable(False, False)
        
        ctk.CTkLabel(popup, text="Number of devices to generate:", font=("Arial", 12)).pack(pady=10)
        
        count_entry = ctk.CTkEntry(popup, placeholder_text="5")
        count_entry.pack(pady=5, padx=10, fill="x")
        count_entry.insert(0, "5")
        
        def generate():
            try:
                count = int(count_entry.get())
                if count <= 0:
                    messagebox.showerror("Invalid Input", "Please enter a positive number")
                    return
                self.presenter.generate_random_devices(count)
                popup.destroy()
                messagebox.showinfo("Success", f"Generated {count} random devices!")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number")
        
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ctk.CTkButton(button_frame, text="Generate", command=generate).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=5)
    
    def show_price_plot(self):
        """Display a menu to choose which plot to show."""
        if not self.presenter.devices:
            messagebox.showwarning("No Data", "No devices to plot. Add some devices first.")
            return
        
        # Create menu window
        menu_window = ctk.CTkToplevel(self)
        menu_window.title("Choose Plot Type")
        menu_window.geometry("400x300")
        menu_window.resizable(False, False)
        
        # Title label
        ctk.CTkLabel(menu_window, text="Select a Plot Type", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Button frame
        button_frame = ctk.CTkFrame(menu_window, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Plot buttons
        ctk.CTkButton(
            button_frame,
            text="Device Prices",
            command=lambda: self._show_plot(menu_window, self.plot_view.plot_device_prices, self.presenter.devices)
        ).pack(pady=10, fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="Video Card Type Count",
            command=lambda: self._show_plot(menu_window, self.plot_view.plot_videocard_count, self.presenter.devices)
        ).pack(pady=10, fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="Category Comparison",
            command=lambda: self._show_plot(menu_window, self.plot_view.plot_category_comparison, self.presenter.devices)
        ).pack(pady=10, fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="Close",
            fg_color="#555555",
            command=menu_window.destroy
        ).pack(pady=10, fill="x")
    
    def _show_plot(self, menu_window, plot_func, devices):
        """Helper method to display a plot in a new window."""
        try:
            menu_window.destroy()
            
            # Create new window for plot
            plot_window = ctk.CTkToplevel(self)
            plot_window.title("Device Plot")
            plot_window.geometry("900x600")
            plot_window.resizable(True, True)
            
            # Create and plot data
            plot_func(devices)
            
            # Embed plot in window
            plot_widget = self.plot_view.embed_in_tkinter(plot_window)
            plot_widget.pack(fill="both", expand=True, padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror("Plot Error", f"Failed to display plot: {e}")

    def open_add_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Device")
        popup.geometry("400x450")

        # create labeled entry fields
        ctk.CTkLabel(popup, text="Name:").pack(pady=(10,0))
        name_entry = ctk.CTkEntry(popup)
        name_entry.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(popup, text="Model:").pack(pady=(5,0))
        model_entry = ctk.CTkEntry(popup)
        model_entry.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(popup, text="Category:").pack(pady=(5,0))
        category_entry = ctk.CTkEntry(popup)
        category_entry.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(popup, text="Video Card Type:").pack(pady=(5,0))
        videocart_entry = ctk.CTkEntry(popup)
        videocart_entry.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(popup, text="Price (€):").pack(pady=(5,0))
        price_entry = ctk.CTkEntry(popup)
        price_entry.pack(pady=5, fill="x", padx=10)

        # submit button
        def submit():
            kwargs = {}
            try:
                kwargs["name"] = name_entry.get().strip()
                kwargs["model"] = model_entry.get().strip()
                kwargs["category"] = category_entry.get().strip()
                kwargs["videocard_type"] = videocart_entry.get().strip()
                kwargs["price"] = price_entry.get().strip()

                for k, v in kwargs.items():
                    if not v:
                        raise ValueError(f"{k} cannot be empty")

                # validate price is numeric
                try:
                    float(kwargs["price"])
                except ValueError:
                    raise ValueError("price must be a number")

            except Exception as e:
                messagebox.showerror("Error", str(e))
                return

            # forward to presenter
            self.presenter.add_device(kwargs)
            popup.destroy()

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Add", command=submit).pack(side="left", padx=8)
        ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=8)

    def open_edit_popup(self, device):
        popup = ctk.CTkToplevel(self)
        popup.title("Edit Device")
        popup.geometry("400x450")

        # create labeled entry fields prefilled with device values
        ctk.CTkLabel(popup, text="Name:").pack(pady=(10,0))
        name_entry = ctk.CTkEntry(popup)
        name_entry.insert(0, getattr(device, "name", ""))
        name_entry.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(popup, text="Model:").pack(pady=(5,0))
        model_entry = ctk.CTkEntry(popup)
        model_entry.insert(0, getattr(device, "model", ""))
        model_entry.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(popup, text="Category:").pack(pady=(5,0))
        category_entry = ctk.CTkEntry(popup)
        category_entry.insert(0, getattr(device, "category", ""))
        category_entry.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(popup, text="Video Card Type:").pack(pady=(5,0))
        videocart_entry = ctk.CTkEntry(popup)
        videocart_entry.insert(0, getattr(device, "videocard_type", ""))
        videocart_entry.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(popup, text="Price (€):").pack(pady=(5,0))
        price_entry = ctk.CTkEntry(popup)
        price_entry.insert(0, str(getattr(device, "price", "")))
        price_entry.pack(pady=5, fill="x", padx=10)

        def submit_edit():
            kwargs = {}
            try:
                kwargs["name"] = name_entry.get().strip()
                kwargs["model"] = model_entry.get().strip()
                kwargs["category"] = category_entry.get().strip()
                kwargs["videocard_type"] = videocart_entry.get().strip()
                kwargs["price"] = price_entry.get().strip()

                for k, v in kwargs.items():
                    if not v:
                        raise ValueError(f"{k} cannot be empty")

                try:
                    float(kwargs["price"])
                except ValueError:
                    raise ValueError("price must be a number")

            except Exception as e:
                messagebox.showerror("Error", str(e))
                return

            self.presenter.edit_device(device, kwargs)
            popup.destroy()

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(btn_frame, text="Save", command=submit_edit).pack(side="left", padx=8)
        ctk.CTkButton(btn_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=8)
