from typing import Optional, Union


class ValueFormatters:
    """Utility class for formatting display values"""

    # Constants for formatting
    SAMPLE_RATE_PLACEHOLDER = "--------"
    BUFFER_SIZE_PLACEHOLDER = "------"
    KILOHERTZ_THRESHOLD = 1000

    @staticmethod
    def format_sample_rate(rate: Optional[int]) -> str:
        """
        Format sample rate for display

        Args:
            rate: Sample rate in Hz or None

        Returns:
            Formatted string (e.g., "44.1", "48", "--------")
        """
        if not isinstance(rate, int):
            return ValueFormatters.SAMPLE_RATE_PLACEHOLDER

        if rate < ValueFormatters.KILOHERTZ_THRESHOLD:
            return str(rate)

        formatted = rate / ValueFormatters.KILOHERTZ_THRESHOLD
        return str(int(formatted)) if formatted.is_integer() else f"{formatted:.1f}"

    @staticmethod
    def format_buffer_size(buffer_size: Optional[int]) -> str:
        """
        Format buffer size for display

        Args:
            buffer_size: Buffer size in samples or None

        Returns:
            Formatted string (e.g., "512", "------")
        """
        return (
            str(buffer_size)
            if isinstance(buffer_size, int)
            else ValueFormatters.BUFFER_SIZE_PLACEHOLDER
        )

    @staticmethod
    def format_button_value(
        value: int, format_function: Optional[callable] = None
    ) -> Union[str, int]:
        """
        Format a value for button display

        Args:
            value: The raw value
            format_function: Optional formatting function

        Returns:
            Formatted value for display
        """
        return format_function(value) if format_function else value


class DisplayConstants:
    """Constants for UI display"""

    # Status label widths
    SAMPLE_RATE_LABEL_WIDTH = 5
    BUFFER_SIZE_LABEL_WIDTH = 4

    # Units
    SAMPLE_RATE_UNIT = "kHz"
    BUFFER_SIZE_UNIT = "samples"

    # Padding configurations
    STATUS_LABEL_PADDING = (10, 2, 10, 2)
    UNIT_LABEL_PADDING_LEFT = (0, 0, 10, 0)
    UNIT_LABEL_PADDING_RIGHT = (0, 0, 0, 0)
