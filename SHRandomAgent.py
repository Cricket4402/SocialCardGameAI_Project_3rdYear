import random
import SHPlayer
import copy

class RandomAgent(SHPlayer.Player):
    def __init__(self, id, name, party, role, state):
        super().__init__(id, name, party, role, state)
    
    def __str__(self):
        return "RandomAgent"

    def returnrandomplayer(self):
        currentplayers = copy.copy(self.state.players)
        currentplayers.remove(self)
        return currentplayers
    
    def nominatechancellor(self):

        # def shownames(player):
        #     return player.name
        
        # x = list(map(shownames, copy.copy(self.state.players)))
        # print(x)

        currentplayers = copy.copy(self.state.players)
        currentplayers.remove(self)

        # Ex president can't be nominated
        if (self.state.ex_president != None) and (self.state.ex_president in currentplayers): 
            currentplayers.remove(self.state.ex_president)
        
        # Ex chancellor can't be nominated
        if (self.state.ex_chancellor != None) and (self.state.ex_chancellor in currentplayers): 
            currentplayers.remove(self.state.ex_chancellor)

        r = random.randint(0, (len(currentplayers)-1))
        return currentplayers[r]
    
    def choosepolicydiscard(self, policies):
        r = random.randint(0, (len(policies)-1))
        return r
    
    def vote(self):
        r = random.randint(0,1)
        if r == 1:
            return "Ja"
        else:
            return "Nein"
    
    def inspectplayer(self):
        temp = self.returnrandomplayer()
        for insp in self.state.inspected_players:
            # Can't inspect players already inspected
            temp.remove(insp[0])
        r = random.randint(0, (len(temp) - 1))
        return temp[r]
    
    def choosenextpresident(self):
        temp = self.returnrandomplayer()
        r = random.randint(0, (len(temp) - 1))
        return temp[r]
    
    def kill(self):
        temp = self.returnrandomplayer()
        r = random.randint(0, (len(temp) - 1))
        return temp[r]
    
    def veto(self, policies):
        r = random.randint(0,1)
        if r == 1:
            return "ACCEPT VETO"
        else:
            return "REJECT VETO"
