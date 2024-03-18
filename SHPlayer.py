class Player: # Abstract class
    def __init__(self, id, name, party, role, state):
        self.id = id
        self.name = name

        self.party = party # Party membership
        self.role = role # Secret role

        self.state = state # Uses Gamestate()

        self.dead = False # True if killed by exec action

        # With 10 players, Fascists know Hitler, but Hitler doesn't know Fascists
        # This will have a value if player is a Fascist
        self.thehitlerplayer = None 

    def isfascist(self):
        return self.party == "Fascist"
    
    def isHitler(self):
        return self.role == "Hitler"
    
    ## Must implement all below functions ##
    def nominatechancellor(self):
        # Choose who you want to be chancellor.
        # Perform this action when you are president.
        raise NotImplementedError("Player cannot nominate Chancellor")

    def choosepolicydiscard(self, policies):
        # Choose a policy to discard
        # When 2 policies are discarded, the remaining one is enacted
        raise NotImplementedError("Player cannot discard policy")

    def vote(self):
        # Vote for the chosen chancellor
        # Ja for yes, Nein for no
        raise NotImplementedError("Player cannot vote")

    def inspectplayer(self):
        # Executive action for inspecting a player's party membership
        raise NotImplementedError("Player cannot inspect another player")
    
    def choosenextpresident(self):
        # Executive action for choosing next president
        raise NotImplementedError("Player cannot choose another president")
    
    def kill(self):
        # Executive action for killing
        raise NotImplementedError("Player cannot kill")
    
    def veto(self, policies):
        # Veto action
        # policies arg only used in CunningAgent and QAgent
        raise NotImplementedError("Player cannot veto")

    