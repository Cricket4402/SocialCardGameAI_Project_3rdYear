import unittest

import sys
sys.path.append(".")

import SHRandomAgent, SHSelfishAgent, SHSelfishPlusPlusAgent
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

    def test_vote(self):
        result = self.game.voting()
        ye = [True, False]
        self.assertIn(result, ye)

    def test_inspect(self):
        self.game.assignplayergamestates()
        self.game.assignplayerroles()
        self.game.informfascists()
        self.game.choosefirstpresident()

        self.game.inspect()
        tio = self.game.state.inspected_players[0][0]
        self.assertIn(tio, self.game.state.players)
        self.assertIsNot(tio, self.game.state.current_president)
    
    def test_choose(self):
        self.game.assignplayergamestates()
        self.game.assignplayerroles()
        self.game.informfascists()
        self.game.choosefirstpresident()

        self.game.choose()
        self.assertTrue(self.game.specialelection)
        self.assertIn(self.game.state.pre_president, self.game.state.players)
        self.assertNotEqual(self.game.state.pre_president, self.game.state.current_president)

    def test_kill(self):
        self.game.assignplayergamestates()
        self.game.assignplayerroles()
        self.game.informfascists()
        self.game.choosefirstpresident()

        self.game.kill()
        self.assertEqual(len(self.game.state.dead_players), 1)
        self.assertEqual(len(self.game.state.players), 9)
        self.assertEqual(len(self.game.state.players) + len(self.game.state.dead_players), 10)

    def test_veto(self):
        self.game.assignplayergamestates()
        self.game.assignplayerroles()
        self.game.informfascists()
        self.game.choosefirstpresident()

        self.game.state.current_chancellor = self.game.state.current_president.nominatechancellor()
        decision = self.game.veto(self.game.board.drawpolicy(3))
        if decision:
            self.assertTrue(decision)
        else:
            self.assertFalse(decision)
    
    def test_failed_vote(self):
        self.game.failedvote()
        self.assertEqual(len(self.game.board.policydeck), 17)
        self.assertEqual(self.game.state.failedvotes, 1)

        self.game.failedvote()
        self.assertEqual(len(self.game.board.policydeck), 17)
        self.assertEqual(self.game.state.failedvotes, 2)

        self.game.failedvote()
        self.assertEqual(len(self.game.board.policydeck), 16)
        self.assertEqual(self.game.state.failedvotes, 0)

    ### WIN CONDITION TESTS ###

    def test_hitler_chancellor_win(self):
        self.game.state.current_chancellor = self.game.hitler

        self.game.state.fasctracker = 2
        r1 = self.game.hitlerchancellorwincon()
        self.assertFalse(r1)

        self.game.state.fasctracker = 3
        r2 = self.game.hitlerchancellorwincon()
        self.assertTrue(r2)

        self.game.state.fasctracker = 4
        r3 = self.game.hitlerchancellorwincon()
        self.assertTrue(r3)

    def test_policy_win(self):
        self.game.state.libtracker = 4
        self.game.state.fasctracker = 5
        r1 = self.game.policywincon()
        self.assertFalse(r1)

        self.game.state.libtracker = 5
        self.game.state.fasctracker = 5
        r2 = self.game.policywincon()
        self.assertTrue(r2)
        
        self.game.state.libtracker = 4
        self.game.state.fasctracker = 6
        r3 = self.game.policywincon()
        self.assertTrue(r3)

    def test_hitler_killed_win(self):
        self.game.assignplayergamestates()
        self.game.assignplayerroles()
        self.game.informfascists()
        self.game.choosefirstpresident()

        r1 = self.game.hitlerkilledwincon()
        self.assertFalse(r1)

        self.game.state.dead_players.append(self.game.hitler)
        self.game.state.players.remove(self.game.hitler)

        self.assertIn(self.game.hitler, self.game.state.dead_players)
        self.assertNotIn(self.game.hitler, self.game.state.players)
        
        r2 = self.game.hitlerkilledwincon()
        self.assertTrue(r2)

    def test_turn_v1(self):
        self.game.assignplayergamestates()
        self.game.assignplayerroles()
        self.game.informfascists()
        self.game.choosefirstpresident()

        result = self.game.turn()
        self.assertFalse(result)

        if self.game.state.fasctracker == 1:
            self.assertEqual(len(self.game.state.inspected_players), 1)
            self.assertIn(self.game.state.inspected_players[0][0], self.game.state.players)

    def test_turn_policy_win(self):
        self.game.assignplayergamestates()
        self.game.assignplayerroles()
        self.game.informfascists()
        self.game.choosefirstpresident()

        self.game.state.libtracker = 4
        self.game.state.fasctracker = 5

        result = self.game.turn()
        if self.game.state.libtracker == 5 or self.game.state.fasctracker == 6:
            self.assertTrue(result)
        else:
            # If game doesn't end, veto happened, so failed vote is up 1
            self.assertFalse(result)
            self.assertEqual(self.game.state.failedvotes, 1)
    
    def test_turn_hitler_killed(self):
        self.game.assignplayergamestates()
        self.game.assignplayerroles()
        self.game.informfascists()

        self.game.state.dead_players.append(self.game.hitler)
        self.game.state.players.remove(self.game.hitler)

        self.game.choosefirstpresident()

        result = self.game.turn()

        # If vote doesn't fail, then it should result in game ending 
        if self.game.state.failedvotes != 0:
            self.assertFalse(result)
        else:
            self.assertTrue(result)

    def test_play_random(self):
        # Test to see if the game ends
        final = self.game.play()
        self.assertTrue(final)

    def test_play_selfish(self):
        g = SHGame.SHGame()
        for i in range(0, 10):
            name = "Selfish" + str(i)
            x = SHSelfishAgent.SelfishAgent(i, name, "", "", "")
            g.state.players.append(x)

        final = g.play()
        self.assertTrue(final)
    
    def test_play_cunning(self):
        g = SHGame.SHGame()
        for i in range(0, 10):
            name = "Cunning" + str(i)
            x = SHSelfishPlusPlusAgent.SelfishPlusPlus(i, name, "", "", "")
            g.state.players.append(x)

        final = g.play()
        self.assertTrue(final)


if __name__ == "__main__":
    unittest.main()