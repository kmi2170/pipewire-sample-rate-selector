class Utility:
    @staticmethod
    def latency_in_ms(sample_rate: int, quantum: int) -> float:
        return quantum / sample_rate * 1000
