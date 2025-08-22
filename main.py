from tkinter import *
from tkinter.ttk import *  # Override with ttk widgets
from typing import Literal, Optional, Tuple, Dict, Any
import subprocess

from colors import COLORS
from styles import setup_ttk_styles
from formatters import Formatters

PipewireValueType = Literal["rate", "quantum"]
ButtonDict = Dict[int, Button]
ConfigDict = Dict[str, Any]


# Pipewire configuration constants
AVAILABLE_SAMPLE_RATES = (44100, 48000, 88200, 96000, 176400, 192000)
AVAILABLE_BUFFER_SIZES = (32, 64, 128, 256, 512, 1024, 2048)


# UI configuration constants
WINDOW_GEOMETRY = "480x280"
WINDOW_TITLE = "Pipewire Sample Rate Selector"
SAMPLE_RATE_CONFIG = {
    "type": "rate",
    "title": "Sample Rate",
    "unit": "kHz",
}
BUFFER_SIZE_CONFIG = {
    "type": "quantum",
    "title": "Buffer Size",
    "unit": "samples",
}


class PipewireController:
    def get_current_value(self, type: PipewireValueType) -> Optional[int]:
        return self._get_force_value(type) or self._get_value(type)

    def _get_force_value(self, type: PipewireValueType) -> Optional[int]:
        cmd = f"pw-metadata -n settings 0 clock.force-{type}"
        return self._get_value_from_metadata(cmd)

    def _get_value(self, type: PipewireValueType) -> Optional[int]:
        cmd = f"pw-metadata -n settings 0 clock.{type}"
        return self._get_value_from_metadata(cmd)

    def _get_value_from_metadata(self, cmd: str) -> Optional[int]:
        try:
            output = subprocess.check_output(cmd, shell=True)
            value = output.decode("UTF-8").split("value:'")[1].split("' type:")[0]
            return int(value)
        except (subprocess.CalledProcessError, IndexError, ValueError):
            return None

    def set_value(self, value: int, type: PipewireValueType) -> None:
        cmd = f"pw-metadata -n settings 0 clock.force-{type} {value}"
        try:
            subprocess.run(cmd, shell=True)
            print(f"Setting {type} to: {value}")
        except subprocess.CalledProcessError:
            print(f"Failed to set {type} to: {value}")


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
        self._create_ui_elements()

    def _setup_window(self) -> None:
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.resizable(False, False)
        self.root.title(WINDOW_TITLE)
        self.root.configure(bg=COLORS["bg_primary"], padx=10, pady=10)

    def _setup_ttk_style(self) -> None:
        self.style = Style()
        setup_ttk_styles(self.style)

    def _setup_config_for_ui(self) -> None:
        self._sample_rate_config = {
            **SAMPLE_RATE_CONFIG,
            "style": "Rate.TButton",
            "format_function": Formatters.format_sample_rate,
            "available_values": AVAILABLE_SAMPLE_RATES,
        }
        self._buffer_size_config = {
            **BUFFER_SIZE_CONFIG,
            "style": "Buffer.TButton",
            "format_function": Formatters.format_buffer_size,
            "available_values": AVAILABLE_BUFFER_SIZES,
        }

    def _create_ui_elements(self) -> None:
        self._create_current_status_section()
        self._create_buttons_section(
            self._sample_rate_config,
            self._sample_rate_buttons,
        )
        self._create_buttons_section(
            self._buffer_size_config,
            self._buffer_buttons,
        )

        self._set_initial_button_selection()

    def _create_current_status_section(self) -> None:
        frame = Frame(self.root, style="Main.TFrame")
        frame.pack(pady=(10, 10))
        # Configure grid columns
        for i, weight in enumerate([1, 0, 0, 1]):
            frame.grid_columnconfigure(i, weight=weight)

        current_sample_rate_text = Formatters.format_sample_rate(
            self.controller.get_current_value("rate")
        )
        current_buffer_size_text = Formatters.format_buffer_size(
            self.controller.get_current_value("quantum")
        )
        self.current_sample_rate_label = self._create_status_label(
            frame, current_sample_rate_text, 0, width=5
        )
        self._create_unit_label(frame, SAMPLE_RATE_CONFIG["unit"], 1)
        self.current_buffer_size_label = self._create_status_label(
            frame, current_buffer_size_text, 2, width=4
        )
        self._create_unit_label(frame, BUFFER_SIZE_CONFIG["unit"], 3)

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
        self._update_button_selection(
            current_sample_rate,
            self._sample_rate_buttons,
        )
        self._update_button_selection(
            current_buffer_size,
            self._buffer_buttons,
        )

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
            button = Button(
                button_frame,
                text=config["format_function"](value),
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


class PipewireSampleRateSelector:
    def __init__(self):
        root = Tk()
        controller = PipewireController()
        self.gui = PipewireGUI(root, controller)

    def run(self):
        self.gui.run()


def main():
    app = PipewireSampleRateSelector()
    app.run()


if __name__ == "__main__":
    main()
