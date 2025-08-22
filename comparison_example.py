# COMPARISON: Before vs After Refactoring

# =============================================================================
# BEFORE: Original PipewireGUI class (simplified excerpt)
# =============================================================================


class OriginalPipewireGUI:
    def __init__(self, root, controller, ui_config):
        self.root = root
        self.controller = controller
        self.ui_config = ui_config

        # Does EVERYTHING in __init__
        self._setup_window()
        self._setup_ttk_style()  # 50+ lines of styling code!
        self._setup_config_for_ui()
        self._create_ui_elements()

    def _setup_ttk_style(self):
        """This method is 50+ lines long and handles ALL styling"""
        self.style = Style()
        self.style.configure("Main.TFrame", background="black")

        # Lots of hardcoded styling configuration...
        for style_name, bg, fg, font_size in [
            ("Title.TLabel", "black", "white", 11),
            ("Status.Value.TLabel", "#202020", "white", 22),
            # ... more configurations
        ]:
            self.style.configure(
                style_name,
                background=bg,
                foreground=fg,
                font=("Arial", font_size, "bold"),
            )
        # ... 40 more lines of styling code

    def _format_sample_rate(self, rate):
        """Formatting mixed with GUI logic"""
        if not isinstance(rate, int):
            return "--------"
        if rate < 1000:
            return str(rate)
        formatted = rate / 1000
        return str(int(formatted)) if formatted.is_integer() else f"{formatted:.1f}"

    # ... 200+ more lines mixing GUI, styling, and formatting logic


# =============================================================================
# AFTER: Refactored with utility classes
# =============================================================================

from style_manager_example import StyleManager
from formatters_example import ValueFormatters


class RefactoredPipewireGUI:
    def __init__(self, root, controller, ui_config):
        self.root = root
        self.controller = controller
        self.ui_config = ui_config

        # Delegate responsibilities to specialized classes
        self.style_manager = StyleManager(Style())
        self.formatters = ValueFormatters()

        self._initialize_gui()

    def _initialize_gui(self):
        """Much cleaner initialization"""
        self._setup_window()
        self.style_manager.setup_all_styles()  # One line!
        self._create_ui_elements()

    def _setup_window(self):
        """Focused only on window configuration"""
        self.root.geometry(self.ui_config.window_geometry)
        self.root.resizable(False, False)
        self.root.title(self.ui_config.window_title)
        self.root.configure(bg="black", padx=10, pady=10)

    def update_status(self, type):
        """Clean update logic using formatters"""
        current_value = self.controller.get_current_value(type)

        if type == "rate":
            formatted = self.formatters.format_sample_rate(current_value)
            self.current_sample_rate_label.config(text=formatted)
        elif type == "quantum":
            formatted = self.formatters.format_buffer_size(current_value)
            self.current_buffer_size_label.config(text=formatted)


# =============================================================================
# BENEFITS OF REFACTORING:
# =============================================================================

"""
1. SINGLE RESPONSIBILITY PRINCIPLE:
   - StyleManager: Only handles styling
   - ValueFormatters: Only handles formatting
   - PipewireGUI: Only handles GUI orchestration

2. READABILITY:
   - Main GUI class went from 300+ lines to ~100 lines
   - Each method has a clear, focused purpose
   - No more mixing of concerns

3. TESTABILITY:
   - Can test formatting without creating GUI
   - Can test styling independently
   - Each utility class can be unit tested

4. MAINTAINABILITY:
   - Want to change colors? Only touch StyleManager
   - Want to change formatting? Only touch ValueFormatters
   - Want to add new UI elements? Focus on PipewireGUI

5. REUSABILITY:
   - StyleManager could be used in other Tkinter apps
   - ValueFormatters could be used in CLI versions
   - Each utility is self-contained

6. CONFIGURATION:
   - All styling constants are centralized
   - Easy to create themes by changing StyleConfig
   - No more hunting through code for hardcoded values
"""
