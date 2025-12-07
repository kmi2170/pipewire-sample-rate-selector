from tkinter import *
from tkinter.ttk import *  # Override with ttk widgets
from typing import Literal, Optional, Dict, Any
import subprocess

from colors import COLORS
from styles import setup_ttk_styles
from formatters import Formatters
from utility import Utility

PipewireValueType = Literal["rate", "quantum"]
ButtonDict = Dict[int, Button]
ConfigDict = Dict[str, Any]


# Pipewire configuration constants
AVAILABLE_SAMPLE_RATES = (44100, 48000, 88200, 96000, 176400, 192000, 384000)
AVAILABLE_BUFFER_SIZES = (32, 64, 128, 256, 512, 1024, 2048, 4096)


# UI configuration constants
WINDOW_TITLE = "Pipewire Sample Rate Selector"
SAMPLE_RATE_CONFIG = {
    "type": "rate",
    "title": "Sample Rate",
    "unit": "kHz",
}
QUANTUM_CONFIG = {
    "type": "quantum",
    "title": "Quantum",
    "unit": "frames",
}
LATENCY_CONFIG = {
    "type": "latency",
    "title": "Latency",
    "unit": "ms",
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
        self._sync_status_and_button_selection()

    def _setup_window(self) -> None:
        self.root.resizable(True, True)
        self.root.title(WINDOW_TITLE)
        self.root.configure(bg=COLORS["bg_primary"], padx=5, pady=5)

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
            **QUANTUM_CONFIG,
            "style": "Buffer.TButton",
            "format_function": Formatters.format_buffer_size,
            "available_values": AVAILABLE_BUFFER_SIZES,
        }
        self._latency_config = {
            **LATENCY_CONFIG,
            "style": "Latency.TButton",
            "format_function": Formatters.format_latency,
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
        self._create_control_buttons()

    def _create_current_status_section(self) -> None:
        frame = Frame(self.root, style="Main.TFrame")
        frame.pack(pady=(10, 10))
        for i, weight in enumerate([1, 0, 0, 0, 0, 1]):
            frame.grid_columnconfigure(i, weight=weight)
        for i, weight in enumerate([0, 1]):
            frame.grid_rowconfigure(i, weight=weight)

        self._create_status_title_label(frame, SAMPLE_RATE_CONFIG["title"], 0, 0)
        self._current_sample_rate_label = self._create_status_value_label(
            frame, Formatters.format_sample_rate(None), 1, 0, width=5
        )
        self._create_unit_label(frame, SAMPLE_RATE_CONFIG["unit"], 1, 1)

        self._create_status_title_label(frame, QUANTUM_CONFIG["title"], 0, 2)
        self._current_buffer_size_label = self._create_status_value_label(
            frame, Formatters.format_buffer_size(None), 1, 2, width=4
        )
        self._create_unit_label(frame, QUANTUM_CONFIG["unit"], 1, 3)

        self._create_status_title_label(frame, LATENCY_CONFIG["title"], 0, 4)
        self._current_latency_label = self._create_status_value_label(
            frame, Formatters.format_latency(None), 1, 4, width=4
        )
        self._create_unit_label(frame, LATENCY_CONFIG["unit"], 1, 5)

    def _create_status_title_label(
        self, parent: Frame, text: str, row: int, column: int
    ) -> None:
        Label(parent, text=text, style="Status.Title.TLabel").grid(
            row=row, column=column, padx=0, pady=0
        )

    def _create_status_value_label(
        self, parent: Frame, text: str, row: int, column: int, width: int
    ) -> Label:
        label = Label(
            parent,
            text=text,
            style="Status.Value.TLabel",
            anchor="e",
            width=width,
            padding=(10, 2, 10, 2),
        )
        label.grid(row=row, column=column, padx=0, pady=0, sticky="e")
        return label

    def _create_unit_label(
        self, parent: Frame, text: str, row: int, column: int
    ) -> None:
        Label(
            parent,
            text=text,
            style="Status.Unit.TLabel",
        ).grid(row=row, column=column, padx=(2, 8), pady=0, sticky="sw")

    def _create_buttons_section(self, config: ConfigDict, buttons: ButtonDict) -> None:
        Label(
            self.root, text=config["title"], style="Title.TLabel", anchor="center"
        ).pack(pady=(5, 0))
        self._create_buttons(config, buttons)

    def _create_buttons(self, config: ConfigDict, buttons: ButtonDict) -> None:
        button_frame = Frame(self.root, style="Main.TFrame")
        button_frame.pack()
        # Create buttons in a horizontal layout
        for value in config["available_values"]:
            button = Button(
                button_frame,
                text=config["format_function"](value),
                command=lambda v=value: self._on_button_selected(v, config["type"]),
                style=config["style"],
            )
            button.pack(side="left", padx=5, pady=10)
            buttons[value] = button

    def _create_control_buttons(self) -> None:
        button_frame = Frame(self.root, style="Main.TFrame")
        button_frame.pack(padx=10, fill="x")
        Button(
            button_frame,
            text="Sync",
            style="Control.TButton",
            command=self._sync_status_and_button_selection,
        ).pack(side="left", pady=(10, 0))
        Button(
            button_frame,
            text="Exit",
            style="Control.TButton",
            command=self.root.quit,
        ).pack(side="right", pady=(10, 0))

    def _sync_status_and_button_selection(self) -> None:
        self._update_sample_rate_status_and_button_selection()
        self._update_buffer_size_status_and_button_selection()
        self._update_latency_status()

    def _on_button_selected(
        self,
        value: int,
        type: PipewireValueType,
    ) -> None:
        self.controller.set_value(value, type)
        if type == "rate":
            self._update_sample_rate_status_and_button_selection()
        elif type == "quantum":
            self._update_buffer_size_status_and_button_selection()
        self._update_latency_status()

    def _update_sample_rate_status_and_button_selection(
        self,
    ) -> None:
        current_value = self.controller.get_current_value("rate")
        self._current_sample_rate_label.config(
            text=Formatters.format_sample_rate(current_value)
        )
        self._update_button_selection(current_value, self._sample_rate_buttons)

    def _update_buffer_size_status_and_button_selection(
        self,
    ) -> None:
        current_value = self.controller.get_current_value("quantum")
        self._current_buffer_size_label.config(
            text=Formatters.format_buffer_size(current_value)
        )
        self._update_button_selection(current_value, self._buffer_buttons)

    def _update_latency_status(self) -> None:
        current_value = Utility.latency_in_ms(
            self.controller.get_current_value("rate"),
            self.controller.get_current_value("quantum"),
        )
        self._current_latency_label.config(
            text=Formatters.format_latency(current_value)
        )

    def _update_button_selection(
        self, selected_value: int, buttons: ButtonDict
    ) -> None:
        for value, button in buttons.items():
            if value == selected_value:
                button.state(["pressed"])
            else:
                if "pressed" in button.state():
                    button.state(["!pressed"])

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
