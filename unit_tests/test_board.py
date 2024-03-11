import unittest

import sys
sys.path.append(".")

import SHBoard, SHGameState

class TestSHBoard(unittest.TestCase):
    
    def setUp(self):
        # Use this for most of the tests
        self.board = SHBoard.GameBoard(SHGameState.GameState())

    # TODO ADD MORE TESTS LOL
    def test_board_policy_deck_size(self):
        self.assertEqual(len(self.board.policydeck), 17)
    
    def test_board_role_list_size(self):
        self.assertEqual(len(self.board.rolelist), 10)
    
    #def test_draw_policy_

if __name__ == "__main__":
    unittest.main()