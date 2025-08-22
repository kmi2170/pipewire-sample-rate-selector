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


class UIConfig:
    def __init__(self):
        self.window_geometry = "480x280"
        self.window_title = "Pipewire Sample Rate Selector"
        self.sample_rate_config = {
            "type": "rate",
            "title": "Sample Rate",
            "style": "Rate.TButton",
            "unit": "kHz",
        }
        self.buffer_size_config = {
            "type": "quantum",
            "title": "Buffer Size",
            "style": "Buffer.TButton",
            "unit": "samples",
        }


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
    def __init__(self, root: Tk, controller: PipewireController, ui_config: UIConfig):
        self.root = root
        self.controller = controller
        self.ui_config = ui_config

        # Store button information for selection tracking
        self._sample_rate_buttons: Dict[int, Button] = {}
        self._buffer_buttons: Dict[int, Button] = {}

        self._setup_window()
        self._setup_ttk_style()
        self._setup_config_for_ui()
        self._create_ui_elements()

    def _setup_window(self) -> None:
        self.root.geometry(self.ui_config.window_geometry)
        self.root.resizable(False, False)
        self.root.title(self.ui_config.window_title)
        self.root.configure(bg="black", padx=10, pady=10)

    def _setup_ttk_style(self) -> None:
        self.style = Style()
        self.style.configure("Main.TFrame", background="black")
        for style_name, bg, fg, font_size in [
            ("Title.TLabel", "black", "white", 11),
            ("Status.Value.TLabel", "#202020", "white", 22),
            ("Status.Unit.TLabel", "black", "white", 10),
        ]:
            self.style.configure(
                style_name,
                background=bg,
                foreground=fg,
                font=("Arial", font_size, "bold"),
            )
        for style_name, width, fg, font_size, padding in [
            ("Rate.TButton", 5, "cyan", 12, (2, 12)),
            ("Buffer.TButton", 5, "magenta", 12, (2, 12)),
            ("Control.TButton", 8, "white", 10, (0, 5)),
        ]:
            self.style.configure(
                style_name,
                width=width,
                background="#202020",
                foreground=fg,
                relief="flat",
                font=("Arial", font_size, "bold"),
                padding=padding,
            )

        # Configure button states for Rate and Buffer buttons
        for style_name, active_color, pressed_color in [
            ("Rate.TButton", "lightblue", "cyan"),
            ("Buffer.TButton", "pink", "magenta"),
        ]:
            self.style.map(
                style_name,
                background=[
                    ("active", active_color),
                    ("pressed", pressed_color),
                    ("selected", pressed_color),
                ],
                foreground=[
                    ("active", "black"),
                    ("pressed", "black"),
                    ("selected", "black"),
                ],
            )

    def _setup_config_for_ui(self) -> None:
        self._sample_rate_config = {
            **self.ui_config.sample_rate_config,
            "format_function": Formatters.format_sample_rate,
            "available_values": self.controller.get_available_sample_rates(),
        }
        self._buffer_size_config = {
            **self.ui_config.buffer_size_config,
            "format_function": Formatters.format_buffer_size,
            "available_values": self.controller.get_available_buffer_sizes(),
        }

    def _create_ui_elements(self) -> None:
        self._create_current_status_section()
        self._create_buttons_section(
            self._sample_rate_config, self._sample_rate_buttons
        )
        self._create_buttons_section(self._buffer_size_config, self._buffer_buttons)

        self._set_initial_button_selection()

    def _create_current_status_section(self) -> None:
        frame = Frame(self.root, style="Main.TFrame")
        frame.pack(pady=(10, 10))

        # Configure grid columns
        for i, weight in enumerate([1, 0, 0, 1]):
            frame.grid_columnconfigure(i, weight=weight)

        current_rate = self.controller.get_current_value("rate")
        current_buffer = self.controller.get_current_value("quantum")

        self.current_sample_rate_label = self._create_status_label(
            frame, Formatters.format_sample_rate(current_rate), 0, width=5
        )
        self._create_unit_label(frame, "kHz", 1)

        self.current_buffer_size_label = self._create_status_label(
            frame, Formatters.format_buffer_size(current_buffer), 2, width=4
        )
        self._create_unit_label(frame, "samples", 3)

    def _create_status_label(
        self, parent: Frame, text: str, column: int, width: int
    ) -> Label:
        label = Label(
            parent,
            text=text,
            style="Status.Value.TLabel",
            anchor="e",
            width=width,
            padding=(10, 2, 10, 2),
        )
        label.grid(row=0, column=column, padx=0, pady=0, sticky="e")
        return label

    def _create_unit_label(self, parent: Frame, text: str, column: int) -> None:
        padding = (0, 0, 10, 0) if column == 1 else (0, 0, 0, 0)
        Label(parent, text=text, style="Status.Unit.TLabel", padding=padding).grid(
            row=0, column=column, padx=5, pady=0, sticky="sw"
        )

    def _set_initial_button_selection(self) -> None:
        current_sample_rate = self.controller.get_current_value("rate")
        current_buffer_size = self.controller.get_current_value("quantum")

        self._update_button_selection(current_sample_rate, self._sample_rate_buttons)
        self._update_button_selection(current_buffer_size, self._buffer_buttons)

    def _create_buttons_section(self, config: ConfigDict, buttons: ButtonDict) -> None:
        Label(
            self.root, text=config["title"], style="Title.TLabel", anchor="center"
        ).pack(pady=(10, 0))

        self._create_buttons(config, buttons)

    def _create_buttons(self, config: ConfigDict, buttons: ButtonDict) -> None:
        button_frame = Frame(self.root, style="Main.TFrame")
        button_frame.pack()

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

            buttons[value] = button

    def on_button_selected(
        self,
        value: int,
        buttons: ButtonDict,
        type: PipewireValueType,
    ) -> None:
        self.controller.set_value(value, type)
        self.update_status(type)
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

    def update_status(self, type: PipewireValueType) -> None:
        current_value = self.controller.get_current_value(type)
        if type == "rate":
            self.current_sample_rate_label.config(
                text=Formatters.format_sample_rate(current_value)
            )
        elif type == "quantum":
            self.current_buffer_size_label.config(
                text=Formatters.format_buffer_size(current_value)
            )

    def run(self):
        self.root.mainloop()


class Formatters:
    @staticmethod
    def format_sample_rate(rate: int | None) -> str:
        if not isinstance(rate, int):
            return "--------"
        if rate < 1000:
            return str(rate)
        formatted = rate / 1000
        return str(int(formatted)) if formatted.is_integer() else f"{formatted:.1f}"

    @staticmethod
    def format_buffer_size(buffer_size: int | None) -> str:
        return str(buffer_size) if isinstance(buffer_size, int) else "------"


class PipewireSampleRateSelector:
    def __init__(self):
        root = Tk()
        config = PipewireConfig()
        ui_config = UIConfig()
        controller = PipewireController(config)

        self.gui = PipewireGUI(root, controller, ui_config)

    def run(self):
        self.gui.run()


if __name__ == "__main__":
    app = PipewireSampleRateSelector()
    app.run()
