class GUIContext:
    def __init__(self, screen, model, manager):
        self.screen = screen
        self.model = model
        self.manager = manager

    def run(self):
        raise NotImplementedError