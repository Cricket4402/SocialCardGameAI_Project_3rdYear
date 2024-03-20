import SHBoard, SHGameState
import SHRandomAgent, SHSelfishAgent, SHCunningAgent

import random

class SHGame:
    # Set agentmix to True for random mix of agents
    def __init__(self, agentmix = False, outputconsole = False, outputlogs = False):
        self.state = SHGameState.GameState()
        self.board = SHBoard.GameBoard(self.state)
        self.hitler = None # Just to make it easier to check Hitler related stuff

        self.specialelection = False # True if special election action used

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
    
    def voting(self):
        # Return True if vote passes
        # Return False if vote fails
        yes = 0
        no = 0

        for p in self.state.players:
            temp = p.vote()
            if temp == "Ja":
                yes = yes + 1
            else:
                no = no + 1
        
        if yes > no:
            return True
        else:
            return False
    
    def inspect(self):
        inspected = self.state.current_president.inspectplayer()
        self.state.inspected_players.append((inspected, inspected.party))

    def choose(self):
        self.specialelection = True

        chosen = self.state.current_president.choosenextpresident()
        self.state.pre_president = self.state.current_president
        self.state.current_president = chosen

    def kill(self):
        dead = self.state.current_president.kill()
        self.state.dead_players.append(dead)
        self.state.players.remove(dead)

    def veto(self, policies):
        chancellor_response = self.state.current_chancellor.veto(policies)
        president_response = self.state.current_president.veto(policies)
        if chancellor_response == president_response:
            return True
        return False
    
    def failedvote(self):
        self.state.failedvotes += 1
        if self.state.failedvotes == 3:
            self.state.failedvotes == 0
            
            # Enact policy on the top of the deck
            self.board.enactpolicy(self.board.drawpolicy(1))
    
    def turn(self):
        if self.specialelection == False:
            # Select next player to be president
            # Skip this if Special Election is used
            self.setnextpresident()
        elif self.specialelection == True:
            self.state.current_president = self.state.pre_president
        
        self.specialelection = False

        # President nominates Chancellor
        self.state.nominated_chancellor = self.state.current_president.nominatechancellor()

        # Players vote if they want current president + chancellor
        result = self.voting()

        # If vote fails do this
        if result == False:
            self.failedvote()
        
        # Else, vote passes
        else:
            self.state.current_chancellor = self.state.nominated_chancellor
            # If Hitler is elected with 3+ Fascist policies, end game
            # Return value 3
            if self.state.current_chancellor == self.hitler:
                return 3

            # Else enact policy
            # (Here we can check if policy win is possible)
            # Return value 1 for Liberal policy win
            # Return value 2 for Fascist policy win
            # Draw 3 policies
            drawnpolicies = self.board.drawpolicy(3)
            # Current president chooses 1 to discard
            pdiscardchoice = self.state.current_president.choosepolicydiscard(drawnpolicies)
            # Remaining policies left (2 in the hand)
            remainingpolicies = self.board.discardpolicy(drawnpolicies, pdiscardchoice)

            # If 5 Fascist policies enacted, enable veto
            if self.state.fasctracker == 5:
                veto_status = self.veto(remainingpolicies)
                if veto_status:
                    # If veto passes
                    self.failedvote()
                    # End turn early
                    return -1

            # Current chancellor chooses 1 to discard
            cdiscardchoice = self.state.current_chancellor.choosepolicydiscard(remainingpolicies)
            # The final policy remaining after 2 have been discarded
            finalpolicy = self.board.discardpolicy(remainingpolicies, cdiscardchoice)
            # Enact the policy
            self.board.enactpolicy(finalpolicy[0])

            if self.state.libtracker == 5:
                return 1
            elif self.state.fasctracker == 6:
                return 2
        
        
            # Perform executive action if applicable
            if self.board.fascistactions[self.state.fasctracker - 1] is not None:
                execaction = self.board.fascistactions[self.state.fasctracker - 1]
                print("Performing executive action: " + execaction)
                # TODO IMPLEMENT EXEC ACTIONS
                if execaction == "inspect":
                    self.inspect()
                elif execaction == "choose":
                    self.choose()
                    # End this turn early to begin a new one
                    return -1
                elif execaction == "kill":
                    self.kill()


            # Check if Hitler is dead (post exec action)
            # Return value 4
            if self.hitler in self.state.dead_players:
                return 4
            
            
            # Otherwise, set current Chancellor and President to ex
            self.state.ex_chancellor = self.state.current_chancellor
            self.state.ex_president = self.state.current_president

            self.state.nominated_chancellor = None
            self.state.current_chancellor = None

            return -1

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
        
