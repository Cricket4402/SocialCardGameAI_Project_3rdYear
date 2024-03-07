import random
import SHPolicy
import SHRole

class GameBoard:
    def __init__(self, state):
        self.state = state
        self.num_liberals = 6
        self.num_fascists = 4
        self.rolelist = [SHRole.Hitler()] + ([SHRole.Fascist()] * 3) + ([SHRole.Liberal()] * 6)
        self.policydeck = ([SHPolicy.Liberal()] * 6) + ([SHPolicy.Fascist()] * 11)
        self.discardpile = []
        




