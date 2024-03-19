import SHBoard, SHGameState
import SHRandomAgent, SHSelfishAgent, SHCunningAgent

import random

class SHGame:
    # Set agentmix to True for random mix of agents
    def __init__(self, agentmix = False, outputconsole = False, outputlogs = False):
        self.state = SHGameState.GameState()
        self.board = SHBoard.GameBoard(self.state)
        self.hitler = None # Just to make it easier to check Hitler related stuff
    
    def assignplayergamestates(self):
        for p in self.state.players:
            p.state = self.state

    def assignplayerroles(self):
        rolearr = self.board.rolelist
        players = self.state.players
        for i in range(0, len(players)): # 10 players, goes up to index 9
            players[i].party = rolearr[i][0]
            players[i].role = rolearr[i][1]
            if players[i].role == "Hitler":
                self.hitler = players[i]

    def informfascists(self):
        # Inform Fascists who Hitler is
        playerarr = self.state.players
        for player in playerarr:
            if player.party == "Fascist":
                player.thehitlerplayer = self.hitler
        
    def choosefirstpresident(self):
        # Choose the first president to begin the game
        r = random.randint(0, 9)
        self.state.current_president = self.state.players[r]

    ##########################################
    #            TURN BASED STUFF            #
    ##########################################

    def setnextpresident(self):
        curpres = self.state.current_president
        i = self.state.players.index(curpres)
        return self.state.players[(i+1)%10]
    

    def turn(self):
            # Select next player to be president
            self.setnextpresident()

            # President nominates Chancellor

            # Players vote if they want current president + chancellor

            # If vote fails do this

            
            # Else, vote passes
            
            # If Hitler is elected with 3+ Fascist policies, end game
            # Return value 3

            # Else enact policy
            # (Here we can check if policy win is possible)
            # Return value 1 for Liberal policy win
            # Return value 2 for Fascist policy win

            # Perform executive action if applicable

            # Check if Hitler is dead (post exec action)
            # Return value 4

    ###########################################
    #         END OF TURN BASED STUFF         #
    ###########################################

    def play(self):
        self.assignplayergamestates()
        self.assignplayerroles()
        self.informfascists()
        self.choosefirstpresident()

        game_over = -1

        while game_over == -1:
            game_over = self.turn()
        
        return game_over
    

    def wincon(self, result):
        if result == 1:
            print("Liberals won by enacting 5 Liberal policies")
        elif result == 2:
            print("Fascists won by enacting 6 Fascists policies")
        elif result == 3:
            print("Fascists won by electing Hitler")
        elif result == 4:
            print("Liberals won by killing Hitler")
        else:
            print("How did you get here?")
        
