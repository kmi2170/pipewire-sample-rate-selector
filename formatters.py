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
