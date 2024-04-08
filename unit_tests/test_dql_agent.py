import unittest

import sys
sys.path.append(".")

import SHDQLAgent, SHRandomAgent, SHGameState
import random

class TestSHDQLAgent(unittest.TestCase):
    def setUp(self):
        self.gstate = SHGameState.GameState()

        ## Alice will be our main character for the tests ##
        self.alice = SHRandomAgent.RandomAgent(0, "Alice", "Liberal", "Liberal", self.gstate)
        self.bob = SHRandomAgent.RandomAgent(1, "Bob", "Fascist", "Fascist", self.gstate)
        self.charlie = SHRandomAgent.RandomAgent(2, "Charlie", "Liberal", "Liberal", self.gstate)
        self.david = SHRandomAgent.RandomAgent(3, "David", "Fascist", "Fascist", self.gstate)
        self.eve = SHRandomAgent.RandomAgent(4, "Eve", "Fascist", "Hitler", self.gstate)

        self.omega = SHDQLAgent.DQLAgent(5, "Omega", "Liberal", "Liberal", self.gstate)
        
        self.gstate.players.append(self.alice)
        self.gstate.players.append(self.bob)
        self.gstate.players.append(self.charlie)
        self.gstate.players.append(self.david)
        self.gstate.players.append(self.eve)
        self.gstate.players.append(self.omega)
    
    def test_nominate_chancellor(self):
        x = self.omega.nominatechancellor()
        self.assertIsNot(x, self.omega)
        self.assertIn(x, self.gstate.players)

    def test_choose_policy_discard_3_cards(self):
        pile = ["Liberal", "Fascist", "Fascist"]
        x = self.omega.choosepolicydiscard(pile)
        self.assertTrue(0 <= x <= 2)

    def test_vote(self):
        x = self.omega.vote()
        if x == "Ja":
            self.assertEqual(x, "Ja")
            self.assertNotEqual(x, "Nein")
        else:
            self.assertEqual(x, "Nein")
            self.assertNotEqual(x, "Ja")

    def test_veto(self):
        x = self.omega.veto([])
        if x == "ACCEPT VETO":
            self.assertEqual(x, "ACCEPT VETO")
            self.assertNotEqual(x, "REJECT VETO")
        else:
            self.assertEqual(x, "REJECT VETO")
            self.assertNotEqual(x, "ACCEPT VETO")

    def test_inspect(self):
        self.gstate.inspected_players.append((self.bob, self.bob.party))
        x = self.omega.inspectplayer()
        self.assertIn(x, self.gstate.players)
        self.assertIsNot(x, self.omega)
        self.assertIsNot(x, self.bob)
    
    def test_special_election(self):
        x = self.omega.choosenextpresident()
        self.assertIn(x, self.gstate.players)
        self.assertIsNot(x, self.omega)

    def test_kill(self):
        x = self.omega.kill()
        self.assertIn(x, self.gstate.players)
        self.assertIsNot(x, self.omega)