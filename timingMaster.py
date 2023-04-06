class TimingMaster:
    def __init__(self, timestamp = 0):
        self.timestamp = timestamp
        self.running = False
        self.increment = 1000

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def tick(self):
        if self.running:
            self.timestamp += self.increment