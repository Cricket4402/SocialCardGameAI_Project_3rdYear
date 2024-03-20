import unittest

import sys
sys.path.append(".")

import SHRandomAgent, SHGameState
import random

class TestSHRandomAgent(unittest.TestCase):
    def setUp(self):
        self.gstate = SHGameState.GameState()

        ## Alice will be our main character for the tests ##
        self.alice = SHRandomAgent.RandomAgent(0, "Alice", "Liberal", "Liberal", self.gstate)
        self.bob = SHRandomAgent.RandomAgent(1, "Bob", "Fascist", "Fascist", self.gstate)
        self.charlie = SHRandomAgent.RandomAgent(2, "Charlie", "Liberal", "Liberal", self.gstate)
        self.david = SHRandomAgent.RandomAgent(3, "David", "Fascist", "Fascist", self.gstate)
        self.eve = SHRandomAgent.RandomAgent(4, "Eve", "Fascist", "Hitler", self.gstate)
        
        self.gstate.players.append(self.alice)
        self.gstate.players.append(self.bob)
        self.gstate.players.append(self.charlie)
        self.gstate.players.append(self.david)
        self.gstate.players.append(self.eve)
    
    def test_return_random_player(self):
        # The random player chosen is a valid player

        # Covers the following functions
        # - nominatechancellor
        # - inspectplayer
        # - choosenextpresident
        # - kill

        x = self.alice.returnrandomplayer()
        r = random.randint(0, (len(x) - 1))
        self.assertIn(x[r], self.gstate.players)
    
    def test_return_random_player_not_self(self):
        # The random player chosen is not themselves
        x = self.alice.returnrandomplayer()
        self.assertIsNot(x, self.alice)

    def test_nominate_chancellor(self):
        self.gstate.ex_chancellor = self.bob
        self.gstate.ex_president = self.charlie

        x = self.alice.nominatechancellor()
        self.assertIn(x, self.gstate.players)
        self.assertIsNot(x, self.alice)

        self.assertIsNot(x, self.bob)
        self.assertIsNot(x, self.charlie)

    def test_choose_policy_discard_3_cards(self):
        pile = ["Liberal", "Fascist", "Fascist"]
        x = self.alice.choosepolicydiscard(pile)
        self.assertTrue(0 <= x <= 2)

    def test_choose_policy_discard_2_cards(self):
        pile = ["Liberal", "Fascist"]
        x = self.alice.choosepolicydiscard(pile)
        self.assertTrue(0 <= x <= 1)

    def test_vote(self):
        x = self.alice.vote()
        if x == "Ja":
            self.assertEqual(x, "Ja")
            self.assertNotEqual(x, "Nein")
        else:
            self.assertEqual(x, "Nein")
            self.assertNotEqual(x, "Ja")

    def test_veto(self):
        x = self.alice.veto([])
        if x == "ACCEPT VETO":
            self.assertEqual(x, "ACCEPT VETO")
            self.assertNotEqual(x, "REJECT VETO")
        else:
            self.assertEqual(x, "REJECT VETO")
            self.assertNotEqual(x, "ACCEPT VETO")
    
    def test_inspect(self):
        self.gstate.inspected_players.append((self.bob, self.bob.party))
        x = self.alice.inspectplayer()
        self.assertIn(x, self.gstate.players)
        self.assertIsNot(x, self.alice)
        self.assertIsNot(x, self.bob)



if __name__ == "__main__":
    unittest.main()