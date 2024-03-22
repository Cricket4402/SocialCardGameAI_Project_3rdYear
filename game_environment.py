import SHGame
import SHRandomAgent, SHSelfishAgent, SHSelfishPlusPlusAgent
import random
import time

n = 20000

libpol = 0
faspol = 0
hitelect = 0
killhit = 0

randomagentwins = [0, 0, 0]
selfishagentwins = [0, 0, 0]
splusagentwins = [0, 0, 0]

raloss = [0, 0, 0]
saloss = [0, 0, 0]
spaloss = [0, 0, 0]

def agentwinlosscounter(winvalue, players):
    
    # Filter by role
    # The reason is that a single bot may be Hitler
    # e.g. only 1 RandomAgent, which happens to be Hitler
    def libfilter(p):
        if p.role == "Liberal":
            return True
        return False
    
    def fascfilter(p):
        if p.role == "Fascist":
            return True
        return False
    
    def hitlerfilter(p):
        if p.role == "Hitler":
            return True
        return False
    
    def agents(p):
        return type(p)

    libplayers = list(filter(libfilter, players)) # Lib players
    fascplayers = list(filter(fascfilter, players)) # Fascist players
    hitlerplayers = list(filter(hitlerfilter, players)) # Hiter player

    libagents = list(map(agents, libplayers))
    fascagents = list(map(agents, fascplayers))
    hitleragents = list(map(agents, hitlerplayers))

    # Identify the winvalue
    # If Liberals win
    if winvalue == 1 or winvalue == 4:
        # Assign wins to Liberals
        if SHRandomAgent.RandomAgent in libagents:
            randomagentwins[0] += 1
        if SHSelfishAgent.SelfishAgent in libagents:
            selfishagentwins[0] += 1
        if SHSelfishPlusPlusAgent.SelfishPlusPlus in libagents:
            splusagentwins[0] += 1

        # Assign losses to Fascists/Hitler
        if SHRandomAgent.RandomAgent in fascagents:
            raloss[1] += 1
        if SHSelfishAgent.SelfishAgent in fascagents:
            saloss[1] += 1
        if SHSelfishPlusPlusAgent.SelfishPlusPlus in fascagents:
            spaloss[1] += 1

        if SHRandomAgent.RandomAgent in hitleragents:
            raloss[2] += 1
        if SHSelfishAgent.SelfishAgent in hitleragents:
            saloss[2] += 1
        if SHSelfishPlusPlusAgent.SelfishPlusPlus in hitleragents:
            spaloss[2] += 1
    elif winvalue == 2 or winvalue == 3:
        # Assign wins to Fascists/Hitler
        if SHRandomAgent.RandomAgent in fascagents:
            randomagentwins[1] += 1
        if SHSelfishAgent.SelfishAgent in fascagents:
            selfishagentwins[1] += 1
        if SHSelfishPlusPlusAgent.SelfishPlusPlus in fascagents:
            splusagentwins[1] += 1
        
        if SHRandomAgent.RandomAgent in hitleragents:
            randomagentwins[2] += 1
        if SHSelfishAgent.SelfishAgent in hitleragents:
            selfishagentwins[2] += 1
        if SHSelfishPlusPlusAgent.SelfishPlusPlus in hitleragents:
            splusagentwins[2] += 1

        # Assign losses to Liberals
        if SHRandomAgent.RandomAgent in libagents:
            raloss[0] += 1
        if SHSelfishAgent.SelfishAgent in libagents:
            saloss[0] += 1
        if SHSelfishPlusPlusAgent.SelfishPlusPlus in libagents:
            spaloss[0] += 1


def botmaker(name):
    r = random.randint(1,3)
    if r == 1:
        return SHRandomAgent.RandomAgent(i, name, "", "", "")
    elif r == 2:
        return SHSelfishAgent.SelfishAgent(i, name, "", "", "")
    elif r == 3:
        return SHSelfishPlusPlusAgent.SelfishPlusPlus(i, name, "", "", "")
    # elif r == 4:
    #     return SHQLearnAgent.QLearn(i, name, "", "", "")


start = time.time()
for i in range(0, n):
    game = SHGame.SHGame()

    # Ensure that there is at least 1 of each bot
    # bot0 = SHRandomAgent.RandomAgent(i, "RandomRoss", "", "", "")
    # bot1 = SHSelfishAgent.SelfishAgent(i, "SelfishSteve", "", "", "")
    # bot2 = SHSelfishPlusPlusAgent.SelfishPlusPlus(i, "SPlusSarah", "", "", "")
    # bot3 = SHQLearnAgent.QLearn(i, "QLearnQiyana", "", "", "")

    # game.state.players.append(bot0)
    # game.state.players.append(bot1)
    # game.state.players.append(bot1)

    for i in range(0, 10):
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
    
    allplayers = game.state.players + game.state.dead_players
    agentwinlosscounter(game.wincon(), allplayers)

    # for i in range(0, len(allplayers)):
    #     print(f"Player {i}: Class: {str(allplayers[i])} Role: {allplayers[i].role}")

end = time.time()

print(f"Time taken: {end - start}")

print(f"Liberal policy win: {libpol}")
print(f"Fascist policy win: {faspol}")
print(f"Hitler elected win: {hitelect}")
print(f"Killed Hitler win: {killhit}")
print(f"Total games played: {libpol + faspol + hitelect + killhit}")

print(f"Random agent wins: Liberal: {randomagentwins[0]} Fascist: {randomagentwins[1]} Hitler: {randomagentwins[2]}")
print(f"Selfish agent wins: Liberal: {selfishagentwins[0]} Fascist: {selfishagentwins[1]} Hitler: {selfishagentwins[2]}")
print(f"Selfish+ agent wins: Liberal: {splusagentwins[0]} Fascist: {splusagentwins[1]} Hitler: {splusagentwins[2]}")
print("------------------------------------------------------")
print(f"Random agent losses: Liberal: {raloss[0]} Fascist: {raloss[1]} Hitler: {raloss[2]}")
print(f"Selfish agent losses: Liberal: {saloss[0]} Fascist: {saloss[1]} Hitler: {saloss[2]}")
print(f"Selfish+ agent losses: Liberal: {spaloss[0]} Fascist: {spaloss[1]} Hitler: {spaloss[2]}")

print("======================================================")

print(f"""Random agent role winrates: 
      Liberal: {round(randomagentwins[0]/(randomagentwins[0]+raloss[0]), 3)} 
      Fascist: {round(randomagentwins[1]/(randomagentwins[1]+raloss[1]), 3)} 
      Hitler: {round(randomagentwins[2]/(randomagentwins[2]+raloss[2]), 3)}""")

print(f"""Selfish agent role winrates: 
      Liberal: {round(selfishagentwins[0]/(selfishagentwins[0]+saloss[0]), 3)} 
      Fascist: {round(selfishagentwins[1]/(selfishagentwins[1]+saloss[1]), 3)} 
      Hitler: {round(selfishagentwins[2]/(selfishagentwins[2]+saloss[2]), 3)}""")

print(f"""Selfish++ agent role winrates: 
      Liberal: {round(splusagentwins[0]/(splusagentwins[0]+spaloss[0]), 3)} 
      Fascist: {round(splusagentwins[1]/(splusagentwins[1]+spaloss[1]), 3)} 
      Hitler: {round(splusagentwins[2]/(splusagentwins[2]+spaloss[2]), 3)}""")

print("======================================================")

print(f"Random agent overall winrate: {round(((randomagentwins[0]+randomagentwins[1]+randomagentwins[2])/(randomagentwins[0]+randomagentwins[1]+randomagentwins[2]+raloss[0]+raloss[1]+raloss[2])),3)}")
print(f"Selfish agent overall winrate: {round(((selfishagentwins[0]+selfishagentwins[1]+selfishagentwins[2])/(selfishagentwins[0]+selfishagentwins[1]+selfishagentwins[2]+saloss[0]+saloss[1]+saloss[2])),3)}")
print(f"Selfish++ agent overall winrate: {round(((splusagentwins[0]+splusagentwins[1]+splusagentwins[2])/(splusagentwins[0]+splusagentwins[1]+splusagentwins[2]+spaloss[0]+spaloss[1]+spaloss[2])),3)}")

print(f"""Game ending scenarios
      Liberal Policy enacted: {round(libpol/n,3)}
      Fascist Policy enacted: {round(faspol/n,3)}
      Hitler elected as Chancellor: {round(hitelect/n,3)}
      Hitler is killed: {round(killhit/n,3)}""")