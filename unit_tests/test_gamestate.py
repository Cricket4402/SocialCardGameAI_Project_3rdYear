import unittest

import sys
sys.path.append(".")

import SHGameState

class TestSHGameState(unittest.TestCase):
    def test_default_gamestate_values(self):
        x = SHGameState.GameState()
        self.assertEqual(x.libtracker, 0)
        self.assertEqual(x.fasctracker, 0)
        self.assertEqual(x.failedvotes, 0)

        self.assertIsNone(x.current_president)
        self.assertIsNone(x.ex_president)
        self.assertIsNone(x.chosen_president)
        self.assertIsNone(x.current_chancellor)
        self.assertIsNone(x.ex_chancellor)

        self.assertEqual(len(x.votes), 0)
        self.assertEqual(len(x.players), 0)

        self.assertFalse(x.veto)

if __name__ == "__main__":
    unittest.main()