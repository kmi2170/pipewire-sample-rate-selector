from tkinter import *
from tkinter.ttk import *  # Override with ttk widgets


class PipewireConfig:
    def __init__(self):
        self.available_sample_rates = (44100, 48000, 88200, 96000, 176400, 192000)
        self.available_buffer_sizes = (32, 64, 128, 256, 512, 1024, 2048)

        # Overrides default values in pipewire config if defined
        self.default_sample_rate = None
        self.default_buffer_size = None


class PipewireController(PipewireConfig):
    def __init__(self):
        super().__init__()
        self.current_sample_rate = None
        self.current_buffer_size = None

    def get_available_sample_rates(self):
        return self.available_sample_rates

    def get_available_buffer_sizes(self):
        return self.available_buffer_sizes

    def get_current_sample_rate(self):
        """Get the currently set sample rate"""
        # TODO: Implement actual pipewire query
        return self.current_sample_rate or None

    def get_current_buffer_size(self):
        """Get the currently set buffer size"""
        # TODO: Implement actual pipewire query
        return self.current_buffer_size or None

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
        print("Refreshing Pipewire status...")
        pass


class PipewireGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Store button information for selection tracking
        self.rate_buttons = {}
        self.buffer_buttons = {}

        self.setup_window()
        self.setup_ttk_style()
        self.setup_config_for_ui()
        self.create_ui()

    def setup_window(self):
        self.root.geometry("800x600")
        self.root.resizable(False, False)

    def setup_ttk_style(self):
        self.style = Style()
        self.style.configure("Main.TFrame", background="black")
        self.style.configure(
            "Title.TLabel",
            background="black",
            foreground="white",
            font=("Arial", 12, "bold"),
        )
        self.style.configure(
            "Status.Value.TLabel",
            background="#202020",
            foreground="white",
            font=("Arial", 26, "bold"),
        )
        self.style.configure(
            "Status.Unit.TLabel",
            background="black",
            foreground="white",
            font=("Arial", 10, "bold"),
        )
        self.style.configure(
            "Rate.TButton",
            width=5,
            background="#202020",
            foreground="cyan",
            relief="flat",
            font=("Arial", 12, "bold"),
            padding=(5, 14),
        )
        self.style.configure(
            "Buffer.TButton",
            width=5,
            background="#202020",
            foreground="magenta",
            relief="flat",
            font=("Arial", 12, "bold"),
            padding=(5, 14),
        )
        self.style.configure(
            "Control.TButton",
            width=10,
            background="#202020",
            foreground="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            padding=(5, 10),
        )

        # Configure button states for Rate and Buffer buttons
        # active: when hovered
        # pressed: when clicked
        # selected: when selected
        self.style.map(
            "Rate.TButton",
            background=[
                ("active", "lightblue"),
                ("pressed", "cyan"),
                ("selected", "cyan"),
            ],
            foreground=[
                ("active", "black"),
                ("pressed", "black"),
                ("selected", "black"),
            ],
        )
        self.style.map(
            "Buffer.TButton",
            background=[
                ("active", "pink"),
                ("pressed", "magenta"),
                ("selected", "magenta"),
            ],
            foreground=[
                ("active", "black"),
                ("pressed", "black"),
                ("selected", "black"),
            ],
        )

    def setup_config_for_ui(self):
        self.sample_rate_config = {
            "title": "Sample Rate",
            "style": "Rate.TButton",
            "unit": "kHz",
            "format_function": self.format_sample_rate,
            "available_values": self.controller.get_available_sample_rates(),
            "on_click_function": self.on_sample_rate_selected,
        }
        self.buffer_size_config = {
            "title": "Buffer Size",
            "style": "Buffer.TButton",
            "unit": "samples",
            "format_function": None,
            "available_values": self.controller.get_available_buffer_sizes(),
            "on_click_function": self.on_buffer_size_selected,
        }

    def create_ui(self):
        self.main_frame = Frame(self.root, padding=10, style="Main.TFrame")
        self.main_frame.pack(fill="both", expand=True)

        self.create_current_status_section()
        self.create_buttons_section(self.sample_rate_config, self.rate_buttons)
        self.create_buttons_section(self.buffer_size_config, self.buffer_buttons)
        self.create_control_buttons()

    def create_current_status_section(self):
        current_rate = self.controller.get_current_sample_rate()
        current_buffer = self.controller.get_current_buffer_size()
        formatted_rate = self.format_sample_rate(current_rate)
        formatted_buffer = self.format_buffer_size(current_buffer)

        current_status_frame = Frame(self.main_frame, style="Main.TFrame")
        current_status_frame.pack(pady=20)

        current_status_frame.grid_columnconfigure(0, weight=1)  # Sample rate value
        current_status_frame.grid_columnconfigure(1, weight=0)  # "kHz" unit
        current_status_frame.grid_columnconfigure(2, weight=0)  # Buffer size value
        current_status_frame.grid_columnconfigure(3, weight=1)  # "samples" unit

        self.current_sample_rate_label = Label(
            current_status_frame,
            text=f"{formatted_rate}",
            style="Status.TLabel",
            anchor="e",
            width=5,
            padding=(15, 5, 15, 5),
        )
        self.current_sample_rate_label.grid(row=0, column=0, padx=0, pady=0, sticky="e")
        Label(
            current_status_frame,
            text="kHz",
            style="Status.Unit.TLabel",
            padding=(0, 0, 10, 0),
        ).grid(row=0, column=1, padx=5, pady=0, sticky="sw")

        self.current_buffer_size_label = Label(
            current_status_frame,
            text=f"{formatted_buffer}",
            style="Status.TLabel",
            width=4,
            padding=(15, 5, 15, 5),
            anchor="e",
        )
        self.current_buffer_size_label.grid(row=0, column=2, padx=0, pady=0, sticky="e")
        Label(
            current_status_frame,
            text="samples",
            style="Status.Unit.TLabel",
        ).grid(row=0, column=3, padx=5, pady=0, sticky="sw")

    def create_buttons_section(self, config, buttons):
        section_frame = Frame(self.main_frame, style="Main.TFrame")
        section_frame.pack(pady=20)
        Label(
            section_frame,
            text=config["title"],
            style="Title.TLabel",
            anchor="center",
        ).pack()

        self.create_buttons(config, buttons)

    def create_buttons(self, config, buttons):
        button_frame = Frame(self.main_frame, style="Main.TFrame")
        button_frame.pack(pady=20)

        # Create buttons in a horizontal layout
        for value in config["available_values"]:
            formatted_value = (
                config["format_function"](value) if config["format_function"] else value
            )
            button = Button(
                button_frame,
                text=formatted_value,
                command=lambda v=value: config["on_click_function"](v),
                style=config["style"],
            )
            button.pack(side="left", padx=5, pady=10)

            # Store button reference for later styling updates
            buttons[value] = button

    def create_control_buttons(self):
        control_frame = Frame(self.main_frame, style="Main.TFrame")
        control_frame.pack(side="bottom", fill="x", padx=10, pady=20)

        Button(
            control_frame,
            text="Update",
            command=self.update_status,
            style="Control.TButton",
        ).pack(side="left")
        Button(
            control_frame,
            text="Exit",
            command=self.root.quit,
            style="Control.TButton",
        ).pack(side="right")

    # def on_button_selected(self, value, buttons, config):
    #     success = self.controller.set_sample_rate(value)
    #     if success:
    #         self.update_button_selection(value, buttons)
    #         self.update_status()

    def on_sample_rate_selected(self, rate):
        success = self.controller.set_sample_rate(rate)
        if success:
            self.update_status()
            self.update_button_selection(rate, self.rate_buttons)

    def on_buffer_size_selected(self, buffer_size):
        success = self.controller.set_buffer_size(buffer_size)
        if success:
            self.update_status()
            self.update_button_selection(buffer_size, self.buffer_buttons)

    def update_button_selection(self, selected_value, buttons):
        for value, button in buttons.items():
            if value == selected_value:
                button.state(["pressed"])
            else:
                if "pressed" in button.state():
                    button.state(["!pressed"])

    def update_status(self):
        current_rate = self.controller.get_current_sample_rate()
        current_buffer = self.controller.get_current_buffer_size()
        formatted_rate = self.format_sample_rate(current_rate)
        formatted_buffer = self.format_buffer_size(current_buffer)

        self.current_sample_rate_label.config(text=f"{formatted_rate}")
        self.current_buffer_size_label.config(text=f"{formatted_buffer}")

    def format_sample_rate(self, rate):
        # Format sample rate for display (44100 -> 44.1, 192000 -> 192)
        if isinstance(rate, int):
            if rate >= 1000:
                formatted = rate / 1000
                # Remove unnecessary decimal places
                if formatted.is_integer():
                    return str(int(formatted))
                else:
                    return f"{formatted:.1f}"
            else:
                return str(rate)
        return "------"

    def format_buffer_size(self, buffer_size):
        if isinstance(buffer_size, int):
            return str(buffer_size)
        return "------"

    def run(self):
        self.root.mainloop()


class PipewireSampleRateSelector:
    def __init__(self):
        root = Tk()
        controller = PipewireController()
        self.gui = PipewireGUI(root, controller)

    def run(self):
        self.gui.run()


if __name__ == "__main__":
    app = PipewireSampleRateSelector()
    app.run()
