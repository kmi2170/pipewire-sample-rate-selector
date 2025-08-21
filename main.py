from tkinter import *
from tkinter.ttk import *  # Override with ttk widgets
from typing import Literal, Optional, Tuple, Dict, Any
import subprocess

PipewireValueType = Literal["rate", "quantum"]
ButtonDict = Dict[int, Button]
ConfigDict = Dict[str, Any]


class PipewireConfig:
    def __init__(self):
        self.available_sample_rates = (44100, 48000, 88200, 96000, 176400, 192000)
        self.available_buffer_sizes = (32, 64, 128, 256, 512, 1024, 2048)


class PipewireController:
    def __init__(self, config: PipewireConfig):
        self.config = config

    def get_available_sample_rates(self) -> Tuple[int, ...]:
        return self.config.available_sample_rates

    def get_available_buffer_sizes(self) -> Tuple[int, ...]:
        return self.config.available_buffer_sizes

    def get_current_value(self, type: PipewireValueType) -> Optional[int]:
        return self._get_force_value(type) or self._get_value(type)

    def _get_force_value(self, type: PipewireValueType) -> Optional[int]:
        try:
            setting = subprocess.check_output(
                f"pw-metadata -n settings 0 clock.force-{type}", shell=True
            )
            value = setting.decode("UTF-8").split("value:'")[1].split("' type:")[0]
            return int(value)
        except (subprocess.CalledProcessError, IndexError, ValueError):
            return None

    def _get_value(self, type: PipewireValueType) -> Optional[int]:
        try:
            setting = subprocess.check_output(
                f"pw-metadata -n settings 0 clock.{type}", shell=True
            )
            value = setting.decode("UTF-8").split("value:'")[1].split("' type:")[0]
            return int(value)
        except (subprocess.CalledProcessError, IndexError, ValueError):
            return None

    def set_value(self, value: int, type: PipewireValueType) -> None:
        subprocess.run(
            f"pw-metadata -n settings 0 clock.force-{type} {value}", shell=True
        )
        print(f"Setting {type} to: {value}")


class PipewireGUI:
    def __init__(self, root: Tk, controller: PipewireController):
        self.root = root
        self.controller = controller

        # Store button information for selection tracking
        self._sample_rate_buttons: Dict[int, Button] = {}
        self._buffer_buttons: Dict[int, Button] = {}

        self._setup_window()
        self._setup_ttk_style()
        self._setup_config_for_ui()
        self._create_ui()

    def _setup_window(self) -> None:
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.title("Pipewire Sample Rate Selector")
        self.root.configure(bg="black", padx=10, pady=10)

    def _setup_ttk_style(self) -> None:
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
            width=8,
            background="#202020",
            foreground="white",
            font=("Arial", 10, "bold"),
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

    def _setup_config_for_ui(self) -> None:
        self._sample_rate_config = {
            "type": "rate",
            "title": "Sample Rate",
            "style": "Rate.TButton",
            "unit": "kHz",
            "format_function": self._format_sample_rate,
            "available_values": self.controller.get_available_sample_rates(),
        }
        self._buffer_size_config = {
            "type": "quantum",
            "title": "Buffer Size",
            "style": "Buffer.TButton",
            "unit": "samples",
            "format_function": None,
            "available_values": self.controller.get_available_buffer_sizes(),
        }

    def _create_ui(self) -> None:
        self._create_current_status_section()
        self._create_buttons_section(
            self._sample_rate_config, self._sample_rate_buttons
        )
        self._create_buttons_section(self._buffer_size_config, self._buffer_buttons)
        self._set_initial_button_selection()
        self._create_control_buttons()

    def _create_current_status_section(self) -> None:
        current_sample_rate = self.controller.get_current_value("rate")
        current_buffer_size = self.controller.get_current_value("quantum")

        current_status_frame = Frame(self.root, style="Main.TFrame")
        current_status_frame.pack(pady=10)

        current_status_frame.grid_columnconfigure(0, weight=1)  # Sample rate value
        current_status_frame.grid_columnconfigure(1, weight=0)  # "kHz" unit
        current_status_frame.grid_columnconfigure(2, weight=0)  # Buffer size value
        current_status_frame.grid_columnconfigure(3, weight=1)  # "samples" unit

        self.current_sample_rate_label = Label(
            current_status_frame,
            text=self._format_sample_rate(current_sample_rate),
            style="Status.Value.TLabel",
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
            text=self._format_buffer_size(current_buffer_size),
            style="Status.Value.TLabel",
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

    def _set_initial_button_selection(self) -> None:
        current_sample_rate = self.controller.get_current_value("rate")
        current_buffer_size = self.controller.get_current_value("quantum")

        self._update_button_selection(current_sample_rate, self._sample_rate_buttons)
        self._update_button_selection(current_buffer_size, self._buffer_buttons)

    def _create_buttons_section(self, config: ConfigDict, buttons: ButtonDict) -> None:
        Label(
            self.root,
            text=config["title"],
            style="Title.TLabel",
            anchor="center",
        ).pack(pady=(10, 0))

        self._create_buttons(config, buttons)

    def _create_buttons(self, config: ConfigDict, buttons: ButtonDict) -> None:
        button_frame = Frame(self.root, style="Main.TFrame")
        button_frame.pack(pady=10)

        # Create buttons in a horizontal layout
        for value in config["available_values"]:
            formatted_value = (
                config["format_function"](value) if config["format_function"] else value
            )
            button = Button(
                button_frame,
                text=formatted_value,
                command=lambda v=value: self.on_button_selected(
                    v, buttons, config["type"]
                ),
                style=config["style"],
            )
            button.pack(side="left", padx=5, pady=10)

            # Store button reference for later styling updates
            buttons[value] = button

    def _create_control_buttons(self) -> None:
        Button(
            self.root,
            text="Exit",
            command=self.root.quit,
            style="Control.TButton",
        ).pack(side="right", padx=10, pady=10)

    def on_button_selected(
        self, value: int, buttons: ButtonDict, type: PipewireValueType
    ) -> None:
        self.controller.set_value(value, type)
        self.update_status()
        self._update_button_selection(value, buttons)

    def _update_button_selection(
        self, selected_value: int, buttons: ButtonDict
    ) -> None:
        for value, button in buttons.items():
            if value == selected_value:
                button.state(["pressed"])
            else:
                if "pressed" in button.state():
                    button.state(["!pressed"])

    def update_status(self) -> None:
        current_rate = self.controller.get_current_value("rate")
        current_buffer = self.controller.get_current_value("quantum")
        formatted_rate = self._format_sample_rate(current_rate)
        formatted_buffer = self._format_buffer_size(current_buffer)

        self.current_sample_rate_label.config(text=f"{formatted_rate}")
        self.current_buffer_size_label.config(text=f"{formatted_buffer}")

    def _format_sample_rate(self, rate: int) -> str:
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
        return "--------"

    def _format_buffer_size(self, buffer_size: int) -> str:
        if isinstance(buffer_size, int):
            return str(buffer_size)
        return "------"

    def run(self):
        self.root.mainloop()


class PipewireSampleRateSelector:
    def __init__(self):
        root = Tk()
        config = PipewireConfig()
        controller = PipewireController(config)
        self.gui = PipewireGUI(root, controller)

    def run(self):
        self.gui.run()


if __name__ == "__main__":
    app = PipewireSampleRateSelector()
    app.run()
