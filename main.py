from tkinter import *
from tkinter.ttk import *  # Override with ttk widgets


class PipewireController:
    """Application logic for Pipewire sample rate management"""

    def __init__(self):
        self.current_sample_rate = None
        self.current_buffer_size = None
        self.available_rates = ["44100", "48000", "88200", "96000", "176400", "192000"]
        self.available_buffer_sizes = ["32", "64", "128", "256", "512", "1024", "2048"]
        self.devices = []

    def get_available_sample_rates(self):
        """Get list of available sample rates"""
        return self.available_rates

    def get_available_buffer_sizes(self):
        """Get list of available buffer sizes"""
        return self.available_buffer_sizes

    def get_current_sample_rate(self):
        """Get the currently set sample rate"""
        # TODO: Implement actual pipewire query
        return self.current_sample_rate or "Not set"

    def get_current_buffer_size(self):
        """Get the currently set buffer size"""
        # TODO: Implement actual pipewire query
        return self.current_buffer_size or "Not set"

    def set_sample_rate(self, rate):
        """Set the sample rate for pipewire"""
        # TODO: Implement actual pipewire command
        print(f"Setting sample rate to: {rate} Hz")
        self.current_sample_rate = rate
        return True  # Return success/failure status

    def set_buffer_size(self, buffer_size):
        """Set the buffer size for pipewire"""
        # TODO: Implement actual pipewire command
        print(f"Setting buffer size to: {buffer_size} samples")
        self.current_buffer_size = buffer_size
        return True  # Return success/failure status

    def refresh_status(self):
        """Refresh the list of available audio devices"""
        # TODO: Implement actual pipewire device discovery
        print("Refreshing Pipewire status...")
        pass

    # def get_devices(self):
    #     """Get the list of available audio devices"""
    #     return self.devices


class PipewireGUI:
    """GUI for Pipewire sample rate selector"""

    def __init__(self, controller):
        self.controller = controller
        self.root = Tk()
        self.setup_window()
        self.setup_style()
        self.create_widgets()

    def setup_window(self):
        """Configure the main window properties"""
        # self.root.title("Pipewire Sample Rate Selector")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

    def setup_style(self):
        """Configure ttk styles"""
        self.style = Style()
        self.style.configure("Custom.TFrame", background="black")
        self.style.configure("Title.TLabel", background="black", foreground="white")
        self.style.configure(
            "Rate.TButton",
            width=5,
            background="#202020",
            foreground="cyan",
            relief="flat",
            padding=(6, 14),
        )
        self.style.configure(
            "Buffer.TButton",
            width=5,
            background="#202020",
            foreground="magenta",
            relief="flat",
            padding=(6, 14),
        )

        # Configure button states for Rate buttons
        self.style.map(
            "Rate.TButton",
            background=[
                ("active", "lightblue"),  # When hovered
                ("pressed", "cyan"),  # When clicked/selected
                ("selected", "cyan"),
            ],  # When selected
            foreground=[
                ("active", "black"),  # When hovered
                ("pressed", "black"),  # When clicked/selected
                ("selected", "black"),
            ],
        )  # When selected

        # Configure button states for Buffer buttons
        self.style.map(
            "Buffer.TButton",
            background=[
                ("active", "pink"),  # When hovered
                ("pressed", "magenta"),  # When clicked/selected
                ("selected", "magenta"),
            ],  # When selected
            foreground=[
                ("active", "black"),  # When hovered
                ("pressed", "black"),  # When clicked/selected
                ("selected", "black"),
            ],
        )  # When selected
        self.style.configure(
            "Status.TLabel", background="black", foreground="lightgray"
        )

    def create_widgets(self):
        """Create and layout the main widgets"""
        self.main_frame = Frame(self.root, padding=10, style="Custom.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        self.create_ui_elements()

    def format_sample_rate(self, rate):
        """Format sample rate for display (44100 -> 44.1, 192000 -> 192)"""
        if isinstance(rate, str) and rate.isdigit():
            rate_num = int(rate)
            if rate_num >= 1000:
                formatted = rate_num / 1000
                # Remove unnecessary decimal places
                if formatted.is_integer():
                    return str(int(formatted))
                else:
                    return f"{formatted:.1f}"
            else:
                return rate
        return rate

    def create_ui_elements(self):
        """Create the UI elements for the application"""
        # Title
        # self.title_label = Label(
        #     self.main_frame,
        #     text="Pipewire Sample Rate Selector",
        #     font=("Arial", 16, "bold"),
        #     style="Title.TLabel",
        # )
        # self.title_label.pack(pady=20)

        # Current status
        current_rate = self.controller.get_current_sample_rate()
        formatted_rate = (
            self.format_sample_rate(current_rate)
            if current_rate != "Not set"
            else current_rate
        )

        current_status_frame = Frame(self.main_frame, style="Custom.TFrame")
        current_status_frame.pack(pady=20)

        self.current_sample_rate_label = Label(
            current_status_frame,
            text=f"Current: {formatted_rate}{'kHz' if current_rate != 'Not set' else ''}",
            font=("Arial", 12),
            style="Status.TLabel",
        )
        self.current_sample_rate_label.pack(pady=10)
        self.current_buffer_size_label = Label(
            current_status_frame,
            text=f"Buffer: {formatted_rate}{''if current_rate != 'Not set' else ''}",
            font=("Arial", 12),
            style="Status.TLabel",
        )
        self.current_buffer_size_label.pack(pady=10)

        # Sample rate buttons
        self.create_sample_rate_section()

        # Buffer size buttons
        self.create_buffer_size()

        # Control buttons
        self.create_control_buttons()

    def create_sample_rate_section(self):
        """Create the sample rate selection with buttons"""
        # Section frame
        rate_frame = Frame(self.main_frame, style="Custom.TFrame")
        rate_frame.pack(pady=20, fill="x")

        # Section label
        Label(
            rate_frame,
            text="Sample Rate [kHz]",
            font=("Arial", 12, "bold"),
            style="Title.TLabel",
        ).pack(pady=(0, 10))

        # Button frame for sample rates
        button_frame = Frame(rate_frame, style="Custom.TFrame")
        button_frame.pack(fill="x", padx=20)

        # Store button information for selection tracking
        self.rate_buttons = {}
        self.selected_rate = None

        # Create buttons for each sample rate
        self.create_sample_rate_buttons(button_frame)

    def create_sample_rate_buttons(self, parent_frame):
        """Create buttons for each sample rate"""
        rates = self.controller.get_available_sample_rates()

        # Create buttons in a horizontal layout
        for i, rate in enumerate(rates):
            formatted_rate = self.format_sample_rate(rate)

            # Create button with formatted rate text
            button = Button(
                parent_frame,
                # text=f"{formatted_rate} kHz",
                text=f"{formatted_rate}",
                command=lambda r=rate: self.on_sample_rate_selected(r),
                style="Rate.TButton",
            )
            button.pack(side="left", padx=5, pady=10)

            # Store button reference for later styling updates
            self.rate_buttons[rate] = button

    def create_buffer_size(self):
        """Create the buffer size selection with buttons"""
        # Section frame
        buffer_frame = Frame(self.main_frame, style="Custom.TFrame")
        buffer_frame.pack(pady=20, fill="x")

        # Section label
        Label(
            buffer_frame,
            text="Buffer Size",
            font=("Arial", 12, "bold"),
            style="Title.TLabel",
        ).pack(pady=(0, 10))

        # Button frame for buffer sizes
        button_frame = Frame(buffer_frame, style="Custom.TFrame")
        button_frame.pack(fill="x", padx=20)

        # Store button information for selection tracking
        self.buffer_buttons = {}
        self.selected_buffer_size = None

        # Create buttons for each buffer size
        self.create_buffer_size_buttons(button_frame)

    def create_buffer_size_buttons(self, parent_frame):
        """Create buttons for each buffer size"""
        buffer_sizes = self.controller.get_available_buffer_sizes()

        # Create buttons in a horizontal layout
        for i, buffer_size in enumerate(buffer_sizes):
            # Create button with buffer size text
            button = Button(
                parent_frame,
                text=f"{buffer_size}",
                command=lambda b=buffer_size: self.on_buffer_size_selected(b),
                style="Buffer.TButton",
            )
            button.pack(side="left", padx=5, pady=10)

            # Store button reference for later styling updates
            self.buffer_buttons[buffer_size] = button

    def create_control_buttons(self):
        """Create control buttons (refresh, apply, etc.)"""
        control_frame = Frame(self.main_frame, style="Custom.TFrame")
        control_frame.pack(side="bottom", fill="x", pady=20)

        # Refresh button
        Button(control_frame, text="Refresh", command=self.on_refresh_clicked).pack(
            side="left"
        )

        # Exit button
        Button(control_frame, text="Exit", command=self.root.quit).pack(side="right")

    def on_sample_rate_selected(self, rate):
        """Handle sample rate selection"""
        success = self.controller.set_sample_rate(rate)
        if success:
            self.update_status()
            self.update_button_selection(rate)

    def on_buffer_size_selected(self, buffer_size):
        """Handle buffer size selection"""
        success = self.controller.set_buffer_size(buffer_size)
        if success:
            self.update_status()
            self.update_buffer_button_selection(buffer_size)

    def on_refresh_clicked(self):
        """Handle refresh button click"""
        self.controller.refresh_status()
        self.update_status()

    def update_button_selection(self, selected_rate):
        """Update visual feedback for selected button"""
        # Reset all buttons to default appearance and highlight selected one
        for rate, button in self.rate_buttons.items():
            if rate == selected_rate:
                # Highlight selected button
                button.state(["pressed"])
            else:
                # Reset unselected buttons
                button.state(["!pressed"])

        self.selected_rate = selected_rate

    def update_buffer_button_selection(self, selected_buffer_size):
        """Update visual feedback for selected buffer button"""
        # Reset all buttons to default appearance and highlight selected one
        for buffer_size, button in self.buffer_buttons.items():
            print(
                f"Buffer size: {buffer_size}, selected_buffer_size: {selected_buffer_size}"
            )
            if buffer_size == selected_buffer_size:
                # Highlight selected button
                button.state(["pressed"])
            else:
                # Reset unselected buttons
                button.state(["!pressed"])

        self.selected_buffer_size = selected_buffer_size

    def update_status(self):
        """Update the status labels with current sample rate and buffer size"""
        current_rate = self.controller.get_current_sample_rate()
        current_buffer = self.controller.get_current_buffer_size()
        formatted_rate = (
            self.format_sample_rate(current_rate)
            if current_rate != "Not set"
            else current_rate
        )
        rate_unit = "kHz" if current_rate != "Not set" else ""

        # Update sample rate label
        self.current_sample_rate_label.config(
            text=f"Current: {formatted_rate}{rate_unit}"
        )

        # Update buffer size label
        self.current_buffer_size_label.config(
            text=(
                f"Buffer: {current_buffer} samples"
                if current_buffer != "Not set"
                else "Buffer: Not set"
            )
        )

    def run(self):
        """Start the application"""
        self.root.mainloop()


class PipewireSampleRateSelector:
    """Main application class that coordinates GUI and Controller"""

    def __init__(self):
        self.controller = PipewireController()
        self.gui = PipewireGUI(self.controller)

    def run(self):
        """Start the application"""
        self.gui.run()


if __name__ == "__main__":
    app = PipewireSampleRateSelector()
    app.run()
