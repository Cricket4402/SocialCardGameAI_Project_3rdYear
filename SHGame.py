import SHBoard, SHGameState

import random

class SHGame:
    # Set agentmix to True for random mix of agents
    def __init__(self, outputconsole = False, outputlogs = False):
        self.outputconsole = outputconsole
        self.outputlogs = outputlogs

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
        r = random.randint(0, len(self.state.players)-1)
        self.state.current_president = self.state.players[r]

    ##########################################
    #            TURN BASED STUFF            #
    ##########################################

    def setnextpresident(self):
        curpres = self.state.current_president
        if curpres not in self.state.players:
            # If the current president is dead for whatever reason
            # This is only possible if the president kills themself
            # Which is not allowed in a normal game
            # This is only for test_turn_hitler_killed
            # Choose a random player instead
            i = random.randint(0, len(self.state.players)-1)
        else:
            i = self.state.players.index(curpres)
        return self.state.players[(i+1)%len(self.state.players)]
    
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
    
    ### START OF EXEC POWERS ###

    def inspect(self):
        inspected = self.state.current_president.inspectplayer()
        self.state.inspected_players.append((inspected, inspected.party))

    def choose(self):
        self.specialelection = True

        chosen = self.state.current_president.choosenextpresident()
        self.state.pre_president = self.state.current_president

        # In case the old president gets killed
        i = self.state.players.index(self.state.pre_president)
        self.state.after_pre_president = self.state.players[(i+1)%len(self.state.players)]

        self.state.current_president = chosen

    def kill(self):
        dead = self.state.current_president.kill()

        # Debug
        if self.outputconsole:
            presname = self.state.current_president.name
            print(f"President {presname} has killed {dead.name}")

        self.state.dead_players.append(dead)
        self.state.players.remove(dead)

    ### END OF EXEC POWERS ###

    def veto(self, policies):
        chancellor_response = self.state.current_chancellor.veto(policies)
        president_response = self.state.current_president.veto(policies)
        if chancellor_response == president_response:
            return True
        return False
    
    def failedvote(self):

        # Debug
        if self.outputconsole:
            print("Vote failed!")

        self.state.failedvotes = self.state.failedvotes + 1
        if self.state.failedvotes == 3:
            
            # Debug
            if self.outputconsole:
                print("3 votes failed! Chaos ensues, enact top policy")

            self.state.failedvotes = 0
            
            # Enact policy on the top of the deck
            self.board.enactpolicy(self.board.drawpolicy(1)[0])

        
    # GAME-ENDING CONDITIONS
    def hitlerchancellorwincon(self):
        # If Hitler is elected with 3+ Fascist policies, end game
        if (self.state.current_chancellor == self.hitler) and (self.state.fasctracker >= 3):
            return True
        return False

    def policywincon(self):
        if (self.state.libtracker == 5) or (self.state.fasctracker == 6):
            return True
        return False

    def hitlerkilledwincon(self):
        if self.hitler in self.state.dead_players:
            return True
        return False

    
    def turn(self):

        # Debug
        if self.outputconsole:
            print("Fascist policies: " + str(self.state.fasctracker) + " Liberal policies: " + str(self.state.libtracker))
            print("Deck: " + str(len(self.board.policydeck)) + " Discard: " + str(len(self.board.discardpile)))

        if self.specialelection == False:
            # Select next player to be president
            # Skip this if Special Election is used
            if self.state.pre_president is not None:
                # If there exists a president in pre_president (pre special election)
                # Set current president to be the previous one before the special election
                if self.state.pre_president not in self.state.players:
                    # If old president gets killed
                    self.state.current_president = self.state.after_pre_president
                else:
                    self.state.current_president = self.state.pre_president
                
                self.state.after_pre_president = None
                self.state.pre_president = None
                self.setnextpresident()
            else:
                self.setnextpresident()

        elif self.specialelection == True:
            self.specialelection = False
        
        # Debug
        if self.outputconsole:
            print(f"President this round: {self.state.current_president.name}")
        

        # President nominates Chancellor
        self.state.nominated_chancellor = self.state.current_president.nominatechancellor()

        # Players vote if they want current president + chancellor
        result = self.voting()

        # If vote fails do this
        if result == False:
            self.failedvote()
            return self.policywincon()
        
        # Else, vote passes
        else:
            self.state.current_chancellor = self.state.nominated_chancellor
            # Check Hitler as Chancellor wincon
            if self.hitlerchancellorwincon():
                return True

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
                    # Send remaining into discard pile
                    self.board.discardpile.extend(remainingpolicies)
                    self.failedvote()
                    # Game ends if enacted policies == gg
                    # Otherwise, ends turn early
                    return self.policywincon()

            # Current chancellor chooses 1 to discard
            cdiscardchoice = self.state.current_chancellor.choosepolicydiscard(remainingpolicies)
            # The final policy remaining after 2 have been discarded
            finalpolicy = self.board.discardpolicy(remainingpolicies, cdiscardchoice)
            # Enact the policy
            self.board.enactpolicy(finalpolicy[0])
            
            # If a policy is enacted, reset election tracker
            self.state.failedvotes = 0

            # Check policy wincon
            if self.policywincon():
                return True
        
        
            # Perform executive action if applicable
            
            if finalpolicy[0] == "Fascist":
                if self.board.fascistactions[self.state.fasctracker - 1] is not None:
                    execaction = self.board.fascistactions[self.state.fasctracker - 1]
                    
                    # Debug
                    if self.outputconsole:
                        print("Performing executive action: " + execaction)
                    
                    # TODO IMPLEMENT EXEC ACTIONS
                    if execaction == "inspect":
                        self.inspect()
                    elif execaction == "choose":
                        self.choose()
                        # End this turn early to begin a new one
                        return False
                    elif execaction == "kill":
                        self.kill()


            # Check if Hitler is dead (post exec action)
            if self.hitlerkilledwincon():
                return True
             
            # Otherwise, set current Chancellor and President to ex
            self.state.ex_chancellor = self.state.current_chancellor
            self.state.ex_president = self.state.current_president

            self.state.nominated_chancellor = None
            self.state.current_chancellor = None

            return False

    ###########################################
    #         END OF TURN BASED STUFF         #
    ###########################################

    def play(self):
        self.assignplayergamestates()
        self.assignplayerroles()
        self.informfascists()
        self.choosefirstpresident()

        game_over = False

        while game_over == False:
            game_over = self.turn()
        
        # Debug
        if self.outputconsole:
            print("===============")
            print("Game has ended!")
            print("===============")
        return game_over
    
    def wincon(self):
        if self.state.libtracker == 5:
            # Liberal policy win
            return 1
        elif self.state.fasctracker == 6:
            # Fascist policy win
            return 2
        elif self.hitlerchancellorwincon():
            # Hitler elected Chancellor win
            return 3
        elif self.hitlerkilledwincon():
            # Liberals kill Hitler win
            return 4
        else:
            return "Error"

        
