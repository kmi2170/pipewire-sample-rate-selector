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

    @staticmethod
    def format_latency(value: float) -> str:
        """
        Format a number with dynamic decimal places:
        - 2-digit integer part: 1 decimal place (e.g. 10.4)
        - 1-digit integer part: 2 decimal places (e.g. 0.83, 1.45)
        """
        if not isinstance(value, float):
            return "------"
        int_part = int(value)
        if int_part >= 10:
            return f"{value:.1f}"
        else:
            return f"{value:.2f}"
