from tkinter.ttk import Style
from typing import Tuple, List


class StyleConfig:
    """Constants for styling configuration"""

    # Colors
    BACKGROUND_BLACK = "black"
    BACKGROUND_DARK = "#202020"
    FOREGROUND_WHITE = "white"
    FOREGROUND_CYAN = "cyan"
    FOREGROUND_MAGENTA = "magenta"
    FOREGROUND_LIGHT_BLUE = "lightblue"
    FOREGROUND_PINK = "pink"

    # Fonts
    FONT_FAMILY = "Arial"

    # Label styles configuration
    LABEL_STYLES = [
        ("Title.TLabel", BACKGROUND_BLACK, FOREGROUND_WHITE, 11),
        ("Status.Value.TLabel", BACKGROUND_DARK, FOREGROUND_WHITE, 22),
        ("Status.Unit.TLabel", BACKGROUND_BLACK, FOREGROUND_WHITE, 10),
    ]

    # Button styles configuration
    BUTTON_STYLES = [
        ("Rate.TButton", 5, FOREGROUND_CYAN, 12, (2, 12)),
        ("Buffer.TButton", 5, FOREGROUND_MAGENTA, 12, (2, 12)),
        ("Control.TButton", 8, FOREGROUND_WHITE, 10, (0, 5)),
    ]

    # Button state mappings
    BUTTON_STATE_STYLES = [
        ("Rate.TButton", FOREGROUND_LIGHT_BLUE, FOREGROUND_CYAN),
        ("Buffer.TButton", FOREGROUND_PINK, FOREGROUND_MAGENTA),
    ]


class StyleManager:
    """Handles all TTK styling configuration"""

    def __init__(self, style: Style):
        self.style = style
        self.config = StyleConfig()

    def setup_all_styles(self) -> None:
        """Configure all application styles"""
        self._setup_frame_styles()
        self._setup_label_styles()
        self._setup_button_styles()
        self._setup_button_states()

    def _setup_frame_styles(self) -> None:
        """Configure frame styles"""
        self.style.configure("Main.TFrame", background=self.config.BACKGROUND_BLACK)

    def _setup_label_styles(self) -> None:
        """Configure label styles"""
        for style_name, bg, fg, font_size in self.config.LABEL_STYLES:
            self.style.configure(
                style_name,
                background=bg,
                foreground=fg,
                font=(self.config.FONT_FAMILY, font_size, "bold"),
            )

    def _setup_button_styles(self) -> None:
        """Configure button styles"""
        for style_name, width, fg, font_size, padding in self.config.BUTTON_STYLES:
            self.style.configure(
                style_name,
                width=width,
                background=self.config.BACKGROUND_DARK,
                foreground=fg,
                relief="flat",
                font=(self.config.FONT_FAMILY, font_size, "bold"),
                padding=padding,
            )

    def _setup_button_states(self) -> None:
        """Configure button state styles (hover, pressed, etc.)"""
        for style_name, active_color, pressed_color in self.config.BUTTON_STATE_STYLES:
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
