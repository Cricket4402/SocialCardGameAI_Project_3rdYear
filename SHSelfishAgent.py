import SHRandomAgent

class SelfishAgent(SHRandomAgent.RandomAgent):
    # Same as random agent except when discarding policies
    def __init__(self, id, name, party, role, state):
        super().__init__(id, name, party, role, state)
    
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
    