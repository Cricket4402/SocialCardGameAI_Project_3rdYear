import unittest

import sys
sys.path.append(".")

import SHCunningAgent, SHGameState

class TestSHCunningAgent(unittest.TestCase):
    def setUp(self):
        self.gstate = SHGameState.GameState()

        self.a = SHCunningAgent.CunningAgent(0, "Alice", "Liberal", "Liberal", self.gstate)
        self.b = SHCunningAgent.CunningAgent(1, "Bob", "Liberal", "Liberal", self.gstate)
        self.c = SHCunningAgent.CunningAgent(2, "Charlie", "Liberal", "Liberal", self.gstate)
        self.d = SHCunningAgent.CunningAgent(3, "Dave", "Liberal", "Liberal", self.gstate)
        self.e = SHCunningAgent.CunningAgent(4, "Eve", "Liberal", "Liberal", self.gstate)
        self.f = SHCunningAgent.CunningAgent(5, "Fred", "Liberal", "Liberal", self.gstate)

        self.g = SHCunningAgent.CunningAgent(6, "George", "Fascist", "Fascist", self.gstate)
        self.h = SHCunningAgent.CunningAgent(7, "Harry", "Fascist", "Fascist", self.gstate)
        self.i = SHCunningAgent.CunningAgent(8, "Irene", "Fascist", "Fascist", self.gstate)

        self.j = SHCunningAgent.CunningAgent(9, "Jack", "Fascist", "Hitler", self.gstate)

        self.gstate.players.append(self.a)
        self.gstate.players.append(self.b)
        self.gstate.players.append(self.c)
        self.gstate.players.append(self.d)
        self.gstate.players.append(self.e)
        self.gstate.players.append(self.f)
        self.gstate.players.append(self.g)
        self.gstate.players.append(self.h)
        self.gstate.players.append(self.i)
        self.gstate.players.append(self.j)

        self.g.thehitlerplayer = self.j
        self.h.thehitlerplayer = self.j
        self.i.thehitlerplayer = self.j
    
    def test_nominate_chancellor_as_fascist(self):
        # All Fascists should vote j (Hitler) as Chancellor
        gvote = self.g.nominatechancellor()
        self.assertEqual(gvote, self.j)

        hvote = self.h.nominatechancellor()
        self.assertEqual(hvote, self.j)

        ivote = self.i.nominatechancellor()
        self.assertEqual(ivote, self.j)
    
    def test_nominate_chancellor_as_hitler(self):
        jvote = self.j.nominatechancellor()
        self.assertIn(jvote, self.gstate.players)
        self.assertIsNot(jvote, self.j)
    
    def test_nominate_chancellor_as_liberal_no_sus(self):
        avote = self.a.nominatechancellor()
        self.assertIn(avote, self.gstate.players)
        self.assertIsNot(avote, self.a)

    def test_nominate_chancellor_as_liberal_sus_players_sus(self):
        self.a.suspiciousplayers.append(self.g)
        self.a.suspiciousplayers.append(self.h)
        self.a.suspiciousplayers.append(self.i)
        self.assertEqual(len(self.a.suspiciousplayers), 3)
        avote = self.a.nominatechancellor()
        self.assertIn(avote, self.gstate.players)
        self.assertIsNot(avote, self.a)
        # The sussies
        self.assertIsNot(avote, self.g)
        self.assertIsNot(avote, self.h)
        self.assertIsNot(avote, self.i)

    def test_nominate_chancellor_as_liberal_sus_players_with_ex(self):
        self.gstate.ex_chancellor = self.b
        self.gstate.ex_president = self.c

        self.a.suspiciousplayers.append(self.g)
        self.a.suspiciousplayers.append(self.h)
        self.a.suspiciousplayers.append(self.i)
        self.assertEqual(len(self.a.suspiciousplayers), 3)
        avote = self.a.nominatechancellor()
        self.assertIn(avote, self.gstate.players)
        self.assertIsNot(avote, self.a)

        self.assertIsNot(avote, self.g)
        self.assertIsNot(avote, self.h)
        self.assertIsNot(avote, self.i)

        self.assertIsNot(avote, self.b)
        self.assertIsNot(avote, self.c)
    
    def test_nominate_chancellor_as_liberal_all_sus(self):
        self.gstate.ex_chancellor = self.b
        self.gstate.ex_president = self.c


        self.a.suspiciousplayers.append(self.d)
        self.a.suspiciousplayers.append(self.e)
        self.a.suspiciousplayers.append(self.f)
        self.a.suspiciousplayers.append(self.g)
        self.a.suspiciousplayers.append(self.h)
        self.a.suspiciousplayers.append(self.i)
        self.a.suspiciousplayers.append(self.j)

        self.assertEqual(len(self.a.suspiciousplayers), 7)
        avote = self.a.nominatechancellor()
        self.assertIn(avote, self.gstate.players)
        self.assertIsNot(avote, self.a)

        self.assertIsNot(avote, self.b)
        self.assertIsNot(avote, self.c)

    def test_choose_policy_discard_as_fascist(self):
        pile = ["Liberal", "Fascist", "Fascist"]
        x = self.g.choosepolicydiscard(pile)
        self.assertEqual(x, 0)

        pile2 = ["Fascist", "Fascist", "Liberal"]
        x = self.g.choosepolicydiscard(pile2)
        self.assertEqual(x, 2)

        pile3 = ["Fascist", "Fascist", "Fascist"]
        x = self.g.choosepolicydiscard(pile3)
        self.assertEqual(x, 0)

        pile4 = ["Liberal", "Liberal", "Liberal"]
        x = self.g.choosepolicydiscard(pile4)
        self.assertEqual(x, 0)

        pile5 = ["Liberal", "Liberal"]
        x = self.g.choosepolicydiscard(pile5)
        self.assertEqual(x, 0)

        pile6 = ["Liberal", "Fascist"]
        x = self.g.choosepolicydiscard(pile6)
        self.assertEqual(x, 0)

        pile7 = ["Fascist", "Fascist"]
        x = self.g.choosepolicydiscard(pile7)
        self.assertEqual(x, 0)

    def test_choose_policy_discard_as_liberal(self):
        # Use Alice here
        # First Fascist policy at index 1, so x should return 1
        pile = ["Liberal", "Fascist", "Fascist"]
        x = self.a.choosepolicydiscard(pile)
        self.assertEqual(x, 1)

        pile2 = ["Liberal", "Liberal", "Fascist"]
        x = self.a.choosepolicydiscard(pile2)
        self.assertEqual(x, 2)

        pile3 = ["Fascist", "Fascist", "Fascist"]
        x = self.a.choosepolicydiscard(pile3)
        self.assertEqual(x, 0)

        pile4 = ["Liberal", "Liberal", "Liberal"]
        x = self.a.choosepolicydiscard(pile4)
        self.assertEqual(x, 0)

        pile5 = ["Liberal", "Liberal"]
        x = self.a.choosepolicydiscard(pile5)
        self.assertEqual(x, 0)

        pile6 = ["Liberal", "Fascist"]
        x = self.a.choosepolicydiscard(pile6)
        self.assertEqual(x, 1)

        pile7 = ["Fascist", "Fascist"]
        x = self.a.choosepolicydiscard(pile7)
        self.assertEqual(x, 0)

    def test_vote_as_fascist(self):
        self.gstate.nominated_chancellor = self.i # Fascist
        v1 = self.g.vote()
        self.assertEqual(v1, "Ja")

        self.gstate.nominated_chancellor = self.a # Liberal
        v2 = self.g.vote()
        self.assertEqual(v2, "Nein")

        self.gstate.nominated_chancellor = self.j # Hitler
        v3 = self.g.vote()
        self.assertEqual(v3, "Ja")
    
    def test_vote_as_liberal(self):
        self.gstate.nominated_chancellor = self.i # Not sus
        v1 = self.a.vote()
        self.assertEqual(v1, "Ja")

        self.a.suspiciousplayers.append(self.g)
        self.gstate.nominated_chancellor = self.g # Sus
        v2 = self.a.vote()
        self.assertEqual(v2, "Nein")
    
    def test_vote_as_hitler(self):
        x = self.j.vote()
        if x == "Ja":
            self.assertEqual(x, "Ja")
            self.assertNotEqual(x, "Nein")
        else:
            self.assertEqual(x, "Nein")
            self.assertNotEqual(x, "Ja")

    def test_inspect_player_as_fascist(self):
        self.gstate.inspected_players.append((self.a, self.a.party))
        self.gstate.inspected_players.append((self.b, self.b.party))
        x = self.g.inspectplayer()
        self.assertIn(x, self.gstate.players)
        self.assertIsNot(x, self.g)
        self.assertIsNot(x, self.a)
        self.assertIsNot(x, self.b)
    
    def test_inspect_player_as_liberal(self):
        self.gstate.inspected_players.append((self.h, self.h.party))
        self.gstate.inspected_players.append((self.i, self.i.party))
        # Inspect player - no suspicions
        i1 = self.a.inspectplayer()
        self.assertIn(i1, self.gstate.players)
        self.assertIsNot(i1, self.a)
        self.assertIsNot(i1, self.h)
        self.assertIsNot(i1, self.i)

        # Inspect player - 1 sus
        self.a.suspiciousplayers.append(self.b)
        self.assertEqual(self.a.suspiciousplayers[0], self.b)
        self.assertEqual(len(self.a.suspiciousplayers), 1)
        i2 = self.a.inspectplayer()
        self.assertIn(i2, self.gstate.players)
        self.assertIn(i2, self.a.suspiciousplayers)
        self.assertEqual(i2, self.b)
        self.assertIsNot(i1, self.h)
        self.assertIsNot(i1, self.i)

        # Inpsect player - 1 already inspected, 1 sus
        self.gstate.inspected_players.append((self.b, self.b.party))
        self.a.suspiciousplayers.append(self.c)
        i3 = self.a.inspectplayer()
        self.assertIn(i3, self.gstate.players)
        self.assertIn(i3, self.a.suspiciousplayers)
        self.assertEqual(i3, self.c)
        self.assertIsNot(i1, self.h)
        self.assertIsNot(i1, self.i)

    def test_choose_next_president_as_fascist(self):
        v1 = self.g.choosenextpresident()
        self.assertIn(v1, self.gstate.players)
        self.assertIsNot(v1, self.g)
        self.assertEqual(v1.party, "Fascist")
        self.assertNotEqual(v1.party, "Liberal")

    def test_choose_next_president_as_hitler(self):
        jvote = self.j.choosenextpresident()
        self.assertIn(jvote, self.gstate.players)
        self.assertIsNot(jvote, self.j)

    def test_choose_next_president_as_liberal(self):
        v1 = self.a.choosenextpresident()
        self.assertIn(v1, self.gstate.players)
        self.assertIsNot(v1, self.a)

        self.a.suspiciousplayers.append(self.b)
        v2 = self.a.choosenextpresident()
        self.assertIn(v2, self.gstate.players)
        self.assertIsNot(v2, self.a)
        self.assertIsNot(v2, self.b)

    def test_kill_as_fascist(self):
        k = self.g.kill()
        self.assertIn(k, self.gstate.players)
        self.assertIsNot(k, self.g)
        self.assertEqual(k.party, "Liberal")
        self.assertNotEqual(k.party, "Fascist")

    def test_kill_as_hitler(self):
        k = self.j.kill()
        self.assertIn(k, self.gstate.players)
        self.assertIsNot(k, self.j)

    def test_kill_as_liberal(self):
        k = self.a.kill()
        self.assertIn(k, self.gstate.players)
        self.assertIsNot(k, self.a)

        self.a.suspiciousplayers.append(self.b)
        k2 = self.a.kill()
        self.assertIn(k, self.gstate.players)
        self.assertIsNot(k, self.a)
        self.assertEqual(k2, self.b)

    def test_veto_as_fascist(self):
        p1 = ["Liberal", "Liberal"]
        vt1 = self.g.veto(p1)
        self.assertEqual(vt1, "ACCEPT VETO")

        p2 = ["Fascist", "Liberal"]
        vt2 = self.g.veto(p2)
        self.assertEqual(vt2, "REJECT VETO")

        p3 = ["Fascist", "Fascist"]
        vt3 = self.g.veto(p3)
        self.assertEqual(vt3, "REJECT VETO")

    def test_veto_as_liberal(self):
        p1 = ["Liberal", "Liberal"]
        vt1 = self.a.veto(p1)
        self.assertEqual(vt1, "REJECT VETO")

        p2 = ["Fascist", "Liberal"]
        vt2 = self.a.veto(p2)
        self.assertEqual(vt2, "REJECT VETO")

        p3 = ["Fascist", "Fascist"]
        vt3 = self.a.veto(p3)
        self.assertEqual(vt3, "ACCEPT VETO")

if __name__ == "__main__":
    unittest.main()