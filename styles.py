from tkinter.ttk import Style
from colors import COLORS


def setup_ttk_styles(style: Style) -> None:
    """Configure all ttk styles for the application"""

    # Configure main frame style
    style.configure("Main.TFrame", background=COLORS["bg_primary"])

    # Configure label styles
    for style_name, bg, fg, font_size in [
        ("Title.TLabel", COLORS["bg_primary"], COLORS["font_primary"], 11),
        ("Status.Value.TLabel", COLORS["bg_secondary"], COLORS["font_primary"], 22),
        ("Status.Unit.TLabel", COLORS["bg_primary"], COLORS["font_primary"], 10),
        ("Status.Title.TLabel", COLORS["bg_primary"], COLORS["font_primary"], 8),
    ]:
        style.configure(
            style_name,
            background=bg,
            foreground=fg,
            font=("Arial", font_size, "bold"),
        )

    # Configure button styles
    for style_name, width, fg, font_size, padding in [
        ("Rate.TButton", 5, COLORS["rate_font"]["unselected"], 12, (2, 12)),
        ("Buffer.TButton", 5, COLORS["buffer_font"]["unselected"], 12, (2, 12)),
        ("Control.TButton", 8, COLORS["control_font"]["unselected"], 10, (4, 4)),
    ]:
        style.configure(
            style_name,
            width=width,
            background=COLORS["bg_secondary"],
            foreground=fg,
            relief="flat",
            font=("Arial", font_size, "bold"),
            padding=padding,
        )

    # Configure button states for Rate and Buffer buttons
    for (
        style_name,
        active_color,
        pressed_color,
        selected_color,
        font_active_color,
        font_pressed_color,
        font_selected_color,
    ) in [
        (
            "Rate.TButton",
            COLORS["rate_button"]["active"],
            COLORS["rate_button"]["pressed"],
            COLORS["rate_button"]["selected"],
            COLORS["rate_font"]["active"],
            COLORS["rate_font"]["pressed"],
            COLORS["rate_font"]["selected"],
        ),
        (
            "Buffer.TButton",
            COLORS["buffer_button"]["active"],
            COLORS["buffer_button"]["pressed"],
            COLORS["buffer_button"]["selected"],
            COLORS["buffer_font"]["active"],
            COLORS["buffer_font"]["pressed"],
            COLORS["buffer_font"]["selected"],
        ),
        (
            "Control.TButton",
            COLORS["control_button"]["active"],
            COLORS["control_button"]["pressed"],
            COLORS["control_button"]["selected"],
            COLORS["control_font"]["active"],
            COLORS["control_font"]["pressed"],
            COLORS["control_font"]["selected"],
        ),
    ]:
        style.map(
            style_name,
            background=[
                ("active", active_color),
                ("pressed", pressed_color),
                ("selected", selected_color),
            ],
            foreground=[
                ("active", font_active_color),
                ("pressed", font_pressed_color),
                ("selected", font_selected_color),
            ],
        )
