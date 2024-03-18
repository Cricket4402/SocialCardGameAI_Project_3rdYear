class GameState:
    def __init__(self):
        self.libtracker = 0 # 5 needed to win as Liberals
        self.fasctracker = 0 # 6 needed to win as Fascists, 3 to allow Hitler wincon
        self.failedvotes = 0 # 3 needed for Election Tracker case - read rules for details

        # Election related variables
        self.current_president = None
        self.ex_president = None
        self.chosen_president = None # Executive action choose next president
        
        self.nominated_chancellor = None
        self.current_chancellor = None
        self.ex_chancellor = None

        # Policy related
        self.chancellor_discarded = None # The policy that chancellor discarded
        self.president_discarded = None # The policy that president discarded
        

        # Player related
        self.votes = [] 
        self.players = []

        # Elective action powers
        self.inspected_players = [] # (playerobject, party)

        # Veto power
        self.veto = False # True after 5 Fascist policies enacted

