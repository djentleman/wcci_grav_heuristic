# hyperheuristic

class Hyperheuristic():
    def __init__(self, optimizers):
        self.optimizers = optimizers
        # initialize optimizers in same state
        self.globalPositions = optimizers[0].positions
        for optimizer in self.optimizers:
            optimizer.positions = self.globalPositions
