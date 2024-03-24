class GameState:
    def __init__(self):

        # Election related variables
        self.current_president = None
        self.ex_president = None
        self.pre_president = None # When Special Election used, holds the last president
        self.after_pre_president = None # The president player who should come after pre_pres

        self.nominated_chancellor = None
        self.current_chancellor = None
        self.ex_chancellor = None

        # Policy related
        self.chancellor_discarded = None # The policy that chancellor discarded
        self.president_discarded = None # The policy that president discarded
        

        # Player related
        self.players = []
        self.dead_players = []

        # Elective action powers
        self.inspected_players = [] # (playerobject, party)

