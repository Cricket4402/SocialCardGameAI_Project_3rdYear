import unittest

import sys
sys.path.append(".")

import SHRandomAgent, SHSelfishAgent, SHCunningAgent
import SHGame

class TestSHGame(unittest.TestCase):
    def setUp(self):
        self.game = SHGame.SHGame()
        for i in range(0, 10):
            name = "RandomBot" + str(i)
            x = SHRandomAgent.RandomAgent(i, name, "", "", "")
            self.game.state.players.append(x)

    def test_player_gamestates_assigned(self):
        self.game.assignplayergamestates()
        for p in self.game.state.players:
            # The gamestate objects held by each player should be the same
            # as the one held by the game object
            self.assertEqual(p.state, self.game.state)

    def test_player_parties_and_roles_assigned(self):
        self.game.assignplayerroles()
        player0 = self.game.state.players[0]
        self.assertIsNot(player0.party, "")
        self.assertIsNot(player0.role, "")

        validparty = ["Liberal", "Fascist"]
        validrole = ["Liberal", "Fascist", "Hitler"]

        self.assertIn(player0.party, validparty)
        for p in self.game.state.players:
            self.assertIn(p.party, validparty)
            self.assertIn(p.role, validrole)
    
    def test_inform_fascists(self):
        self.game.assignplayerroles()
        self.game.informfascists()
        for p in self.game.state.players:
            if p.party == "Fascist":
                self.assertIs(p.thehitlerplayer, self.game.hitler)
                self.assertEqual(p.thehitlerplayer, self.game.hitler)
                self.assertIsNot(p.thehitlerplayer, None)
            else:
                self.assertIs(p.thehitlerplayer, None)
                self.assertIsNot(p.thehitlerplayer, self.game.hitler)

    def test_choose_first_president(self):
        self.game.choosefirstpresident()
        x = self.game.state.current_president
        self.assertIn(x, self.game.state.players)

    def test_set_next_president(self):
        self.game.choosefirstpresident()
        cur = self.game.state.current_president
        curi = self.game.state.players.index(cur)
        self.assertEqual(cur, self.game.state.players[curi])

        newpres = self.game.setnextpresident()
        newi = self.game.state.players.index(newpres)
        self.assertEqual(newi, (curi +1)%10)
        self.assertEqual(newpres, self.game.state.players[newi])


if __name__ == "__main__":
    unittest.main()