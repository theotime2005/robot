import time


class TimerExecution:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.result = ""

    def start_timer(self):
        self.start_time = time.perf_counter()

    def stop_timer(self):
        self.end_time = time.perf_counter()
        elapsed_time = self.end_time - self.start_time

        # Conversion en heures, minutes, secondes, millisecondes
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (seconds - int(seconds)) * 1000

        self.result=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
