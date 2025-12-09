# view/plot_view.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Optional, List, Any


class PlotView:
    """A class to handle Matplotlib plot creation and embedding in Tkinter."""
    
    def __init__(self, parent=None, figsize=(8, 6), dpi=100):
        '''
        Initialize the PlotView.
        
        Args:
            parent: Parent Tkinter widget (optional)
            figsize: Tuple of (width, height) in inches
            dpi: Dots per inch for the figure
        '''
        self.parent = parent
        self.figsize = figsize
        self.dpi = dpi
        self.fig: Optional[Figure] = None
        self.ax: Optional[Axes] = None
        self.canvas = None
    
    def create_figure(self):
        '''Create a new matplotlib figure.'''
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        return self.fig, self.ax
    
    def embed_in_tkinter(self, parent):
        """
        Embed the matplotlib figure in a Tkinter window.
        
        Args:
            parent: Tkinter parent widget
            
        Returns:
            The canvas widget containing the figure
        """
        if self.fig is None:
            raise ValueError("Figure not created. Call create_figure() first.")
        
        try:
            self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
            self.canvas.draw()
            
            # Handle window close event to clean up matplotlib
            def on_closing():
                try:
                    if self.canvas:
                        self.canvas.get_tk_widget().destroy()
                    if self.fig:
                        import matplotlib.pyplot as plt
                        plt.close(self.fig)
                except:
                    pass
                parent.destroy()
            
            parent.protocol("WM_DELETE_WINDOW", on_closing)
            return self.canvas.get_tk_widget()
        except Exception as e:
            raise ValueError(f"Failed to embed plot: {e}")
    
    def plot_line(self, x, y, label=None, color=None, linestyle='-', linewidth=2):
        """
        Plot a line on the current axes.
        
        Args:
            x: X-axis data
            y: Y-axis data
            label: Legend label
            color: Line color
            linestyle: Line style ('-', '--', '-.', ':')
            linewidth: Width of the line
        """
        if self.ax is None:
            self.create_figure()
        
        assert self.ax is not None
        self.ax.plot(x, y, label=label, color=color, linestyle=linestyle, linewidth=linewidth)
    def plot_scatter(self, x, y, label=None, color=None, size=50, marker='o'):
        """
        Plot scatter points on the current axes.
        
        Args:
            x: X-axis data
            y: Y-axis data
            label: Legend label
            color: Point color
            size: Point size
            marker: Marker style
        """
        if self.ax is None:
            self.create_figure()
        
        assert self.ax is not None
        self.ax.scatter(x, y, label=label, color=color, s=size, marker=marker)
    def plot_bar(self, x, y, label=None, color=None, width=0.8):
        """
        Plot a bar chart on the current axes.
        
        Args:
            x: X-axis data (categories)
            y: Y-axis data (values)
            label: Legend label
            color: Bar color
            width: Bar width
        """
        if self.ax is None:
            self.create_figure()
        
        assert self.ax is not None
        self.ax.bar(x, y, label=label, color=color, width=width)
        if self.ax is None:
            self.create_figure()
        
        assert self.ax is not None
        self.ax.bar(x, y, label=label, color=color, width=width)
    
    def set_title(self, title, fontsize=14):
        """Set the plot title."""
        if self.ax is None:
            self.create_figure()
        assert self.ax is not None
        self.ax.set_title(title, fontsize=fontsize)
    
    def set_labels(self, xlabel=None, ylabel=None, fontsize=12):
        """Set axis labels."""
        if self.ax is None:
            self.create_figure()
        assert self.ax is not None
        if xlabel:
            self.ax.set_xlabel(xlabel, fontsize=fontsize)
        if ylabel:
            self.ax.set_ylabel(ylabel, fontsize=fontsize)
    
    def set_grid(self, visible=True, alpha=0.3):
        """Enable or disable grid."""
        if self.ax is None:
            self.create_figure()
        assert self.ax is not None
        self.ax.grid(visible=visible, alpha=alpha)
    
    def add_legend(self, loc='best'):
        """Add legend to the plot."""
        if self.ax is None:
            self.create_figure()
        assert self.ax is not None
        self.ax.legend(loc=loc)
    
    def clear(self):
        """Clear the current plot."""
        if self.fig is not None:
            self.fig.clear()
            self.ax = None
    
    def show(self):
        """Display the plot in a standalone window."""
        if self.fig is None:
            raise ValueError("Figure not created. Call create_figure() first.")
        plt.show()
    
    def refresh_canvas(self):
        """Refresh the embedded canvas."""
        if self.canvas is not None:
            self.canvas.draw()
    
    def plot_device_prices(self, devices):
        """
        Plot device prices as a bar chart.
        
        Args:
            devices: List of Device objects with name and price attributes
        """
        if not devices:
            raise ValueError("No devices to plot")
        
        if self.ax is None:
            self.create_figure()
        
        assert self.ax is not None and self.fig is not None
        names = [device.name for device in devices]
        prices = [device.price for device in devices]
        
        self.ax.clear()
        self.ax.bar(names, prices, color='steelblue', edgecolor='navy', alpha=0.7)
        self.ax.set_xlabel('Device Name', fontsize=11)
        self.ax.set_ylabel('Price (€)', fontsize=11)
        self.ax.set_title('Device Prices', fontsize=13, fontweight='bold')
        self.ax.grid(axis='y', alpha=0.3)
        
        # Rotate x-axis labels for better readability
        self.fig.autofmt_xdate(rotation=45, ha='right')
    
    def plot_videocard_count(self, devices):
        """
        Plot count of devices by video card type.
        
        Args:
            devices: List of Device objects with videocard_type attribute
        """
        if not devices:
            raise ValueError("No devices to plot")
        
        if self.ax is None:
            self.create_figure()
        
        assert self.ax is not None and self.fig is not None
        # Count devices by video card type
        videocard_counts = {}
        for device in devices:
            card_type = device.videocard_type
            videocard_counts[card_type] = videocard_counts.get(card_type, 0) + 1
        
        self.ax.clear()
        self.ax.bar(list(videocard_counts.keys()), list(videocard_counts.values()), color='coral', edgecolor='darkred', alpha=0.7)
        self.ax.set_xlabel('Video Card Type', fontsize=11)
        self.ax.set_ylabel('Count', fontsize=11)
        self.ax.set_title('Devices by Video Card Type', fontsize=13, fontweight='bold')
        self.ax.grid(axis='y', alpha=0.3)
        
        self.fig.autofmt_xdate(rotation=45, ha='right')
    
    def plot_category_comparison(self, devices):
        """
        Plot count of devices by category (laptop, tablet, pc, etc).
        
        Args:
            devices: List of Device objects with category attribute
        """
        if not devices:
            raise ValueError("No devices to plot")
        
        if self.ax is None:
            self.create_figure()
        
        assert self.ax is not None and self.fig is not None
        # Count devices by category
        category_counts = {}
        for device in devices:
            category = device.category
            category_counts[category] = category_counts.get(category, 0) + 1
        
        self.ax.clear()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        self.ax.bar(list(category_counts.keys()), list(category_counts.values()), color=colors[:len(category_counts)], edgecolor='black', alpha=0.7)
        self.ax.set_xlabel('Category', fontsize=11)
        self.ax.set_ylabel('Count', fontsize=11)
        self.ax.set_title('Devices by Category', fontsize=13, fontweight='bold')
        self.ax.grid(axis='y', alpha=0.3)
        
        self.fig.autofmt_xdate(rotation=45, ha='right')
