import offsets
class Cheat():
    def __init__(self):
        self.running = False
        self.offsets = offsets.Offsets().get_offsets()

    def get_name(self):
        pass

    def start(self):
        self.running=True

    def stop(self):
        self.running = False

    def get_status(self):
        return self.running