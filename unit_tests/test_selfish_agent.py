import unittest

import sys
sys.path.append(".")

import SHSelfishAgent, SHGameState

class TestSHSelfishAgent(unittest.TestCase):
    def setUp(self):
        self.gstate = SHGameState.GameState()

        ## Alice will be our main character for the tests ##
        self.alice = SHSelfishAgent.SelfishAgent(0, "Alice", "Liberal", "Liberal", self.gstate)
        self.bob = SHSelfishAgent.SelfishAgent(1, "Bob", "Fascist", "Fascist", self.gstate)
        self.charlie = SHSelfishAgent.SelfishAgent(2, "Charlie", "Liberal", "Liberal", self.gstate)
        self.david = SHSelfishAgent.SelfishAgent(3, "David", "Fascist", "Fascist", self.gstate)
        self.eve = SHSelfishAgent.SelfishAgent(4, "Eve", "Fascist", "Hitler", self.gstate)
        
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
        self.assertIn(x, self.gstate.players)
    
    def test_return_random_player_not_self(self):
        # The random player chosen is not themselves
        x = self.alice.returnrandomplayer()
        self.assertIsNot(x, self.alice)

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
    
    def test_choose_policy_as_liberal(self):
        # Use Alice here
        # First Fascist policy at index 1, so x should return 1
        pile = ["Liberal", "Fascist", "Fascist"]
        x = self.alice.choosepolicydiscard(pile)
        self.assertEqual(x, 1)

        pile2 = ["Liberal", "Liberal", "Fascist"]
        x = self.alice.choosepolicydiscard(pile2)
        self.assertEqual(x, 2)

        pile3 = ["Fascist", "Fascist", "Fascist"]
        x = self.alice.choosepolicydiscard(pile3)
        self.assertEqual(x, 0)

        pile4 = ["Liberal", "Liberal", "Liberal"]
        x = self.alice.choosepolicydiscard(pile4)
        self.assertEqual(x, 0)

        pile5 = ["Liberal", "Liberal"]
        x = self.alice.choosepolicydiscard(pile5)
        self.assertEqual(x, 0)

        pile6 = ["Liberal", "Fascist"]
        x = self.alice.choosepolicydiscard(pile6)
        self.assertEqual(x, 1)

        pile7 = ["Fascist", "Fascist"]
        x = self.alice.choosepolicydiscard(pile7)
        self.assertEqual(x, 0)

    def test_choose_policy_as_fascist(self):
        # First Fascist policy at index 1, so x should return 1
        pile = ["Liberal", "Fascist", "Fascist"]
        x = self.bob.choosepolicydiscard(pile)
        self.assertEqual(x, 0)

        pile2 = ["Fascist", "Fascist", "Liberal"]
        x = self.bob.choosepolicydiscard(pile2)
        self.assertEqual(x, 2)

        pile3 = ["Fascist", "Fascist", "Fascist"]
        x = self.bob.choosepolicydiscard(pile3)
        self.assertEqual(x, 0)

        pile4 = ["Liberal", "Liberal", "Liberal"]
        x = self.bob.choosepolicydiscard(pile4)
        self.assertEqual(x, 0)

        pile5 = ["Liberal", "Liberal"]
        x = self.bob.choosepolicydiscard(pile5)
        self.assertEqual(x, 0)

        pile6 = ["Liberal", "Fascist"]
        x = self.bob.choosepolicydiscard(pile6)
        self.assertEqual(x, 0)

        pile7 = ["Fascist", "Fascist"]
        x = self.bob.choosepolicydiscard(pile7)
        self.assertEqual(x, 0)

if __name__ == "__main__":
    unittest.main()