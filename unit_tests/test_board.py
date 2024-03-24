import unittest

import sys
sys.path.append(".")

import SHBoard, SHGameState
import copy

class TestSHBoard(unittest.TestCase):
    
    def setUp(self):
        # Use this for most of the tests
        self.board = SHBoard.GameBoard(SHGameState.GameState())


    def test_board_policy_deck_size(self):
        self.assertEqual(len(self.board.policydeck), 17)
    
    def test_board_role_list_size(self):
        self.assertEqual(len(self.board.rolelist), 10)


    #### SHUFFLE DISCARD PILE TESTS ####
    def test_shuffle_empty_pile(self):
        x = SHBoard.GameBoard(SHGameState.GameState())
        x.shufflediscardback()
        self.assertEqual(len(x.discardpile), 0)
        self.assertEqual(len(x.policydeck), 17)
    
    def test_shuffle_arbitrary_pile(self):
        x = SHBoard.GameBoard(SHGameState.GameState())
        x.discardpile = ["X", "Y", "Z"] # Placeholder tokens
        self.assertEqual(len(x.discardpile), 3)
        self.assertEqual(len(x.policydeck), 17)
        x.shufflediscardback()
        self.assertEqual(len(x.discardpile), 0)
        self.assertEqual(len(x.policydeck), 20)
    

    #### DRAW/DISCARD POLICY TESTS ####
    def test_draw_policy_check_size(self):
        # Check the size of the policydeck does indeed change
        x = SHBoard.GameBoard(SHGameState.GameState())
        x.drawpolicy(3)
        self.assertEqual(len(x.policydeck), 14)
    
    def test_draw_policy_check_size_2(self):
        # Check the size of the policydeck does indeed change
        # Performed until only 2 policies are left
        x = SHBoard.GameBoard(SHGameState.GameState())

        for i in range(1,6): # 3 x 5 = 15, so 17 - 15 = 2 policies left
            x.drawpolicy(3)

        self.assertEqual(len(x.policydeck), 2)
    
    def test_discard_policy_isolated(self):
        x = SHBoard.GameBoard(SHGameState.GameState())
        temp = x.discardpolicy(["X", "Y", "Z"], 0) # Discard index 0

        self.assertEqual(len(x.discardpile), 1)
        self.assertEqual(x.discardpile[0], "X")
        self.assertEqual(len(temp), 2)

        temp2 = x.discardpolicy(temp, 1)

        self.assertEqual(len(x.discardpile), 2)
        self.assertEqual(x.discardpile[0], "X")
        self.assertEqual(x.discardpile[1], "Z")

        self.assertEqual(len(temp2), 1)
        self.assertEqual(temp2[0], "Y")

    def test_discard_policy_fail(self):
        x = SHBoard.GameBoard(SHGameState.GameState())
        # False
        temp = x.discardpolicy(["X", "Y", "Z"], 5) 
        self.assertFalse(temp)

        temp2 = x.discardpolicy(["X", "Y", "Z"], -5) 
        self.assertFalse(temp2)

        temp3 = x.discardpolicy(["X", "Y", "Z"], 3) 
        self.assertFalse(temp3)

        # Not False
        temp4 = x.discardpolicy(["X", "Y", "Z"], 0) 
        self.assertNotEqual(temp4, False)
        
        temp5 = x.discardpolicy(["X", "Y", "Z"], 1) 
        self.assertNotEqual(temp5, False)

        temp6 = x.discardpolicy(["X", "Y", "Z"], 2) 
        self.assertNotEqual(temp6, False)

    #### ENACT POLICY TESTS ####
    def test_draw_discard_discard_enact(self):
        x = SHBoard.GameBoard(SHGameState.GameState())

        # Draw 3
        drawn1 = copy.deepcopy(x.policydeck[:3])
        hand1 = x.drawpolicy(3)
        self.assertEqual(drawn1, hand1)
        self.assertEqual(len(x.policydeck), 14)
        self.assertEqual(len(x.discardpile), 0)

        # Discard 1, check remaining is the same
        oldhand1 = copy.deepcopy(hand1)
        self.assertEqual(len(oldhand1), 3)

        hand2 = x.discardpolicy(hand1, 0)
        self.assertEqual(len(hand2), 2)
        self.assertEqual(len(x.policydeck), 14)
        self.assertEqual(len(x.discardpile), 1)

        oldhand1.pop(0)
        self.assertEqual(len(oldhand1), 2)

        self.assertEqual(hand2, oldhand1)
        self.assertEqual(len(x.policydeck), 14)
        
        # Discard 1, only 1 left
        oldhand2 = copy.deepcopy(hand2)
        hand3 = x.discardpolicy(hand2, 0)
        oldhand2.pop(0)
        self.assertEqual(hand3, oldhand2)
        
        lib = 0
        fasc = 0
        
        x.enactpolicy(hand3[0])

        if hand3[0] == "Liberal":
            lib += 1
            self.assertEqual(x.libtracker, lib)
            self.assertEqual(x.fasctracker, fasc)
        else:
            fasc += 1
            self.assertEqual(x.libtracker, lib)
            self.assertEqual(x.fasctracker, fasc)
        
        self.assertEqual((len(x.policydeck) + len(x.discardpile)), 16)

    def test_full_deck_cycled(self):
        x = SHBoard.GameBoard(SHGameState.GameState())
        lib = 0
        fasc = 0
        for i in range(1, 7):
            a = x.drawpolicy(3)
            b = x.discardpolicy(a, 0)
            c = x.discardpolicy(b, 0)

            x.enactpolicy(c[0])

            if c[0] == "Liberal":
                lib += 1
            else:
                fasc += 1
        
        self.assertEqual(lib, x.libtracker)
        self.assertEqual(fasc, x.fasctracker)
        self.assertEqual(x.fasctracker + x.libtracker, 6)
        self.assertEqual((len(x.policydeck) + len(x.discardpile)), 11)
        self.assertEqual(len(x.policydeck), 9)
        self.assertEqual(len(x.discardpile), 2)


if __name__ == "__main__":
    unittest.main()