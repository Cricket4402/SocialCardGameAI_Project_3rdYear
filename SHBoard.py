import random

# Secret Hitler Board
# Policy Deck + Roles

class GameBoard:
    def __init__(self):

        self.libtracker = 0 # 5 needed to win as Liberals
        self.fasctracker = 0 # 6 needed to win as Fascists, 3 to allow Hitler wincon
        self.failedvotes = 0 # 3 needed for Election Tracker case - read rules for details

        # Fascist actions
        self.fascistactions = ["inspect", "inspect", "choose", "kill", "kill", None]

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
        self.policydeck += self.discardpile
        self.discardpile = []
    
    def drawpolicy(self, n):
        # If there are at least 3 policies or more, draw 3
        # Else shuffle discard pile back

        if len(self.policydeck) >= n:
            draw = self.policydeck[:n]
            self.policydeck = self.policydeck[n:] # removes the top 3 policies
            return draw
        else: # shuffle discard pile back
            self.shufflediscardback()
            draw2 = self.policydeck[:n]
            self.policydeck = self.policydeck[n:] # removes the top 3 policies
            return draw2
    
    def discardpolicy(self, policies, choice):
        try:
            self.discardpile.append(policies[choice])
            policies.pop(choice)
            return policies
        except:
            print("Invalid choice!")
            return False

    def enactpolicy(self, policy):
        # If no executive action can be used, return False
        # Else return True
        if policy == "Liberal":
            self.libtracker += 1
        else:
            self.fasctracker += 1
