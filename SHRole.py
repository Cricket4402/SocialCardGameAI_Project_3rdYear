class Role:
    def __init__(self, membership, role):
        self.membership = membership
        self.role = role
    def __str__(self):
        return f"{self.membership} -> {self.role}"

class Liberal(Role):
    def __init__(self):
        super().__init__("Liberal", "Liberal")

class Fascist(Role):
    def __init__(self):
        super().__init__("Fascist", "Fascist")

class Hitler(Role):
    def __init__(self):
        super().__init__("Fascist", "Hitler")