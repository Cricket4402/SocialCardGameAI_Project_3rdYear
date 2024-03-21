import SHGame
import SHRandomAgent, SHSelfishAgent, SHSelfishPlusAgent
import time

num = 1000000

libpol = 0
faspol = 0
hitelect = 0
killhit = 0
uhhh = 0

counter = 0

start = time.time()
for i in range(0, num):
    game = SHGame.SHGame()
    for i in range(0, 10):
        name = "RandomBot" + str(i)
        # x = SHRandomAgent.RandomAgent(i, name, "", "", "")
        # x = SHSelfishAgent.SelfishAgent(i, name, "", "", "")
        x = SHSelfishPlusAgent.SelfishPlus(i, name, "", "", "")
        game.state.players.append(x)
    result = game.play()
    if result:
        counter += 1
        
    if game.wincon() == 1:
        libpol += 1
    elif game.wincon() == 2:
        faspol += 1
    elif game.wincon() == 3:
        hitelect += 1
    elif game.wincon() == 4:
        killhit += 1
end = time.time()
print(f"Time taken: {end - start}")

print(f"Liberal policy win: {libpol}")
print(f"Fascist policy win: {faspol}")
print(f"Hitler elected win: {hitelect}")
print(f"Killed Hitler win: {killhit}")
print(f"{libpol + faspol + hitelect + killhit}")

