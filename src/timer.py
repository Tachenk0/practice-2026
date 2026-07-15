import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.running = False
    def start(self) -> None:
        if not self.running:
            self.start_time = time.time()
            self.end_time = None
            self.running = True
    def stop(self) -> None:
        if self.running:
            self.end_time = time.time()
            self.running = False
    def reset(self) -> None:
        self.start_time = None
        self.end_time = None
        self.running = False
    def get_elapsed(self) -> int:
        if self.start_time is None:
            return 0
        if self.running:
            return int(time.time() - self.start_time)
        return int(self.end_time - self.start_time)