import random
import SHPlayer
import copy

import sb3_dqn
from SecretHitlerGym import SecretHitlerEnv

class DQLAgent(SHPlayer.Player):
    def __init__(self, id, name, party, role, state):
        super().__init__(id, name, party, role, state)

        self.env = SecretHitlerEnv()

        self.current_obs = {
            "phase":0,
            "current_role":0,
            "is_president":0, 
            "is_chancellor":0, 
            "current_policies":0,
            "current_players_alive":0,
        }

        self.model = sb3_dqn.DQNLoader("SHModel", self.env)
        self.model.model_setup()
    
    def __str__(self):
        return "DQLAgent"
    
    ###### CHANGE THE OBS IN THE METHODS THEMSELVES
    
    def returnvalidplayers(self):
        currentplayers = copy.copy(self.state.players)
        currentplayers.remove(self)
        return currentplayers
    
        

    def reload_model_env(self):
        self.env.overwrite_obs_space(self.current_obs)
        self.model = sb3_dqn.DQNLoader("SHModel", self.env)
    
    def nominatechancellor(self):
        self.current_obs["current_players_alive"] = len(self.state.players) - 1
        try:
            arr = self.returnvalidplayers()

            # Ex president can't be nominated
            if (self.state.ex_president != None) and (self.state.ex_president in arr): 
                arr.remove(self.state.ex_president)
            
            # Ex chancellor can't be nominated
            if (self.state.ex_chancellor != None) and (self.state.ex_chancellor in arr): 
                arr.remove(self.state.ex_chancellor)
            
            self.reload_model_env()
            action = self.model.predict(self.current_obs, deterministic=True)
            return arr[action[0]]
        except:
            x = self.returnvalidplayers()
            r = random.randint(0, (len(x)-1))
            return x[r]

    def choosepolicydiscard(self, policies):
        try:
            self.current_obs["current_policies"] = len(policies)
            self.reload_model_env()
            action = self.model.predict(self.current_obs, deterministic=True)
            return action[0]
        except:
            r = random.randint(0, (len(policies)-1))
            return r
    

    def vote(self):
        try:
            self.reload_model_env()
            action = self.model.predict(self.current_obs, deterministic=True)
            return action[0]
        except:
            r = random.randint(0,1)
            if r == 1:
                return "Ja"
            else:
                return "Nein"

    def inspectplayer(self):
        self.current_obs["current_players_alive"] = len(self.state.players) - 1
        temp = self.returnvalidplayers()
        for insp in self.state.inspected_players:
            # Can't inspect players already inspected
            temp.remove(insp[0])

        try:
            self.reload_model_env()
            action = self.model.predict(self.current_obs, deterministic=True)
            return temp[action[0]]
        except:
            r = random.randint(0, (len(temp) - 1))
            return temp[r]

    def choosenextpresident(self):
        self.current_obs["current_players_alive"] = len(self.state.players) - 1
        temp = self.returnvalidplayers()            
        try:
            self.reload_model_env()
            action = self.model.predict(self.current_obs, deterministic=True)
            return temp[action[0]]
        except:
            r = random.randint(0, (len(temp) - 1))
            return temp[r]

    def kill(self):
        self.current_obs["current_players_alive"] = len(self.state.players) - 1
        temp = self.returnvalidplayers()            
        try:
            self.reload_model_env()
            action = self.model.predict(self.current_obs, deterministic=True)
            return temp[action[0]]
        except:
            r = random.randint(0, (len(temp) - 1))
            return temp[r]

    def veto(self, policies):
        try:
            self.current_obs["current_policies"] = len(policies)
            self.reload_model_env()
            action = self.model.predict(self.current_obs, deterministic=True)
            if action[0] == 1:
                return "ACCEPT VETO"
            else:
                return "REJECT VETO"
        except:
            r = random.randint(0,1)
            if r == 1:
                return "ACCEPT VETO"
            else:
                return "REJECT VETO"