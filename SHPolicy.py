###################################
#              TILES              #
###################################
# Base class for the Liberal/Fascist tiles
class Tile:
    def __init__(self, party):
        self.party = party
    def __str__(self):
        return f"{self.party}"

class Liberal(Tile):
    def __init__(self):
        super().__init__("Liberal")

class Fascist(Tile):
    def __init__(self):
        super().__init__("Fascist")

    




