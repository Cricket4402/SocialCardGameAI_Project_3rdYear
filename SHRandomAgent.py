import random
import SHPlayer

class RandomAgent(SHPlayer.Player):
    def __init__(self, id, name, party, role, state):
        super().__init__(id, name, party, role, state)

    def returnrandomplayer(self):
        currentplayers = self.state.players
        currentplayers.remove(self)

        r = random.randint(0, (len(currentplayers)-1))
        return currentplayers[r]
    
    def nominatechancellor(self):
        return self.returnrandomplayer()
    
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
        return self.returnrandomplayer()
    
    def choosenextpresident(self):
        return self.returnrandomplayer()
    
    def kill(self):
        return self.returnrandomplayer()
    
    def veto(self):
        r = random.randint(0,1)
        if r == 1:
            return "ACCEPT VETO"
        else:
            return "REJECT VETO"
