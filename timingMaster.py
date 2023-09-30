class TimingMaster:
    def __init__(self, timestamp=0):
        self.timestamp = timestamp
        self.running = False
        self.stepping = False
        self.increment = 1

    def start(self):
        self.running = True
        self.stepping = False

    def step(self):
        self.running = True
        self.stepping = True

    def stop(self):
        self.running = False
        self.stepping = False

    def tick(self):
        if self.running:
            self.timestamp += self.increment
        if self.stepping:
            self.running = False
            self.stepping = False
