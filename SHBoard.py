import random

# Secret Hitler Board
# Policy Deck + Roles

class GameBoard:
    def __init__(self, state):
        self.state = state

        # Shuffles the roles - player in position i gets the role in position i
        self.rolelist = [("Fascist", "Hitler")] + ([("Fascist", "Fascist")] * 3) + ([("Liberal", "Liberal")] * 6)
        random.shuffle(self.rolelist)

        # Shuffle the policy deck
        self.policydeck = (["Liberal"] * 6) + (["Fascist"] * 11)
        random.shuffle(self.policydeck)

        self.discardpile = []
    
    def shufflediscardback(self):
        # Shuffle the discard pile back into the policy deck
        random.shuffle(self.discardpile)
        self.policydeck = self.policydeck + self.discardpile
        self.discardpile = []
    
    def drawpolicy(self):
        # If there are at least 3 policies or more, draw 3
        # Else shuffle discard pile back

        if len(self.policydeck) >= 3:
            draw = self.policydeck[:3]
            self.policydeck = self.policydeck[3:] # removes the top 3 policies
            return draw
        else: # shuffle discard pile back
            self.shufflediscardback()
            return self.drawpolicy() # This should never loop
    


        