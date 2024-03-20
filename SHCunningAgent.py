import random
import SHPlayer
import copy
# import SHGameState

class CunningAgent(SHPlayer.Player):
    def __init__(self, id, name, party, role, state):
        super().__init__(id, name, party, role, state)

        # A cunning agent will remember if certain players act sus
        # Holds playerobject
        self.suspiciousplayers = []

    def returnrandomplayer(self):
        currentplayers = copy.copy(self.state.players)
        currentplayers.remove(self)


        r = random.randint(0, (len(currentplayers)-1))
        return currentplayers[r]
    
    def nominatechancellor(self):

        def voterandomchancellor():
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
        
        # If secret role is Fascist, vote Hitler as Chancellor
        if self.role == "Fascist":
            if(self.state.ex_president == self.thehitlerplayer) or (self.state.ex_chancellor == self.thehitlerplayer):
                # If Hitler was president or chancellor last round, can't choose them, choose random instead
                return voterandomchancellor()
            return self.thehitlerplayer
        
        # If Hitler, vote randomly (you don't know the other Fascists)
        if self.role == "Hitler":
            return voterandomchancellor()
        # Liberals will not nominate suspicious players
        if self.role == "Liberal":
            currentplayers = copy.copy(self.state.players)
            currentplayers.remove(self)

            for sus in self.suspiciousplayers:
                currentplayers.remove(sus)

            # Ex president can't be nominated
            if (self.state.ex_president != None) and (self.state.ex_president in currentplayers): 
                currentplayers.remove(self.state.ex_president)
            
            # Ex chancellor can't be nominated
            if (self.state.ex_chancellor != None) and (self.state.ex_chancellor in currentplayers): 
                currentplayers.remove(self.state.ex_chancellor)
            
            if len(currentplayers) == 0: 
                # If all players are sus, then choose randomly
                return voterandomchancellor()
            
            # Will randomly choose a player that is not suspicious
            r = random.randint(0, (len(currentplayers)-1))
            return currentplayers[r]
            

    def choosepolicydiscard(self, policies):
        cparty = self.party
        if cparty == "Liberal":
            # Discard first Fascist policy found
            if "Fascist" not in policies:
                # The only time Fascist is not in policies is if all 3 policies are Liberal
                # Discard the first policy (doesn't matter which one we pick here)
                return 0
            return policies.index("Fascist")
        else:
            # Discard first Liberal policy found, as Fascist
            if "Liberal" not in policies:
                # The only time Liberal is not in policies is if all 3 policies are Fascist
                return 0
            return policies.index("Liberal")

    def vote(self):
        # Liberals will not vote for sus players
        if self.role == "Liberal":
            for p in self.suspiciousplayers:
                if p == self.state.nominated_chancellor:
                    return "Nein"
            return "Ja"
        # Fascists will vote against Liberal players
        if self.role == "Fascist":
            if self.state.nominated_chancellor.party == "Liberal":
                return "Nein"
            return "Ja"

        # Hitler doesn't know the other Fascists, so just vote randomly
        if self.role == "Hitler":
            r = random.randint(0,1)
            if r == 1:
                return "Ja"
            else:
                return "Nein"
        

    def inspectplayer(self):
        def randomplayerinspect():
            t = copy.copy(self.state.players)
            t.remove(self)
            for insp in self.state.inspected_players:
                # Can't inspect players already inspected
                t.remove(insp[0])
            r = random.randint(0, (len(t) - 1))
            return t[r]

        # Liberals will prefer to inspect suspicious players
        if self.party == "Liberal":
            if len(self.suspiciousplayers) != 0: # If there is at least 1 sus player
                sussies = copy.copy(self.suspiciousplayers)

                def mappy(tup):
                    return tup[0]
                
                newm = list(map(mappy, self.state.inspected_players))
                for ip in newm:
                    if ip in sussies:
                        sussies.remove(ip)
                return sussies[0]
            
            # Just pick randomly if cannot pick a sus player
            return randomplayerinspect()
        if self.party == "Fascist":
            return randomplayerinspect()

    def choosenextpresident(self):
        # Liberals will not nominate suspicious players
        if self.role == "Liberal":
            nominees = copy.copy(self.state.players)
            nominees.remove(self)

            for sus in self.suspiciousplayers:
                nominees.remove(sus)

            if len(nominees) == 0:
                return self.returnrandomplayer()
            
            r = random.randint(0, (len(nominees)-1))
            return nominees[r]

        # Fascists only choose other Fascists
        if self.role == "Fascist":
            nominees = copy.copy(self.state.players)
            nominees.remove(self)
            
            def filterlib(player):
                if player.party == "Liberal":
                    return False
                return True
            
            fascists = list(filter(filterlib, nominees))
            r = random.randint(0, (len(fascists)-1))
            return fascists[r]
        
        # Hitler doesn't know other Fascists, so just randomly choose
        if self.role == "Hitler":
            return self.returnrandomplayer()

    def kill(self):
        # Kill sus players
        if self.role == "Liberal":
            if len(self.suspiciousplayers) != 0:
                r = random.randint(0, (len(self.suspiciousplayers)-1))
                return self.suspiciousplayers[r]
            else:
                return self.returnrandomplayer()

        # Kill Liberal players
        if self.role == "Fascist":
            nominees = copy.copy(self.state.players)
            nominees.remove(self)
            
            def filterlibtrue(player):
                if player.party == "Liberal":
                    return True
                return False
            
            libs = list(filter(filterlibtrue, nominees))
            r = random.randint(0, (len(libs)-1))
            return libs[r]

        if self.role == "Hitler":
            # Kill randomly (don't know identity of Fascists)
            return self.returnrandomplayer()

    def veto(self, policies):
        # The veto votes of both president and chancellor must agree
        # Opposite parties will never agree to veto
        # The same parties will agree to veto
        if self.party == "Liberal":
            # Liberals will not veto unless there are no Liberal tiles
            if "Liberal" not in policies:
                # No Liberal tiles -> veto
                return "ACCEPT VETO"
            else:
                # Liberal tiles exist -> no veto
                return "REJECT VETO"
        if self.party == "Fascist":
            if "Fascist" not in policies:
                # No Fascist tiles -> veto
                return "ACCEPT VETO"
            else:
                # Fascist tiles exist -> no veto
                return "REJECT VETO"

# if __name__ == "__main__":
#     gstate = SHGameState.GameState()
#     g = CunningAgent(6, "George", "Fascist", "Fascist", gstate)
#     a = CunningAgent(6, "Alice", "Liberal", "Liberal", gstate)
#     gstate.players.append(g)
#     gstate.players.append(a)
#     gstate.nominated_chancellor = a
#     g.inspectplayer()
#     g.inspectplayer()