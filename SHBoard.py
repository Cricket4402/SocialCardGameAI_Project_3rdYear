import random
import SHPolicy
import SHRole

class GameBoard:
    def __init__(self) -> None:
        pass


policydeck = ([SHPolicy.Liberal()] * 6) + ([SHPolicy.Fascist()] * 11)
rolelist = [SHRole.Hitler()] + [SHRole.Fascist()] * 3 + [SHRole.Liberal()] * 6

for p in policydeck:
    print(p)
print(len(policydeck))

for r in rolelist:
    print(r)
print(len(rolelist))