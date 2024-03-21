import SHGame
import SHRandomAgent, SHSelfishAgent, SHSelfishPlusAgent
import random
import time

n = 20000

libpol = 0
faspol = 0
hitelect = 0
killhit = 0

randomagentwins = [0,0,0]
selfishagentwins = [0,0,0]
splusagentwins = [0,0,0]

def botmaker(name):
    r = random.randint(1,3)
    if r == 1:
        return SHRandomAgent.RandomAgent(i, name, "", "", "")
    elif r == 2:
        return SHSelfishAgent.SelfishAgent(i, name, "", "", "")
    elif r == 3:
        return SHSelfishPlusAgent.SelfishPlus(i, name, "", "", "")
    # elif r == 4:
    #     return SHQLearnAgent.QLearn(i, name, "", "", "")

# TODO MAKE FUNCTIONS TO COUNT WINS FOR EACH ROLE       

    

start = time.time()
for i in range(0, n):
    game = SHGame.SHGame()

    # Ensure that there is at least 1 of each bot
    bot0 = SHRandomAgent.RandomAgent(i, "RandomRoss", "", "", "")
    bot1 = SHSelfishAgent.SelfishAgent(i, "SelfishSteve", "", "", "")
    bot2 = SHSelfishPlusAgent.SelfishPlus(i, "SPlusSarah", "", "", "")
    # bot3 = SHQLearnAgent.QLearn(i, "QLearnQiyana", "", "", "")

    game.state.players.append(bot0)
    game.state.players.append(bot1)
    game.state.players.append(bot1)

    for i in range(0, 7):
        x = botmaker("Bot" + str(i))
        game.state.players.append(x)
    
    random.shuffle(game.state.players)

    result = game.play()

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

