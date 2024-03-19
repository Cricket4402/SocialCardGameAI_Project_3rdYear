import SHGame
import SHRandomAgent

game = SHGame.SHGame()
for i in range(0, 10):
    name = "RandomBot" + str(i)
    x = SHRandomAgent.RandomAgent(i, name, "", "", "")
    game.state.players.append(x)

game.assignplayerroles()
print(game.hitler)