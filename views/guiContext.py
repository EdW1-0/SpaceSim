class GUIContext:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model

    def run(self):
        raise NotImplementedError