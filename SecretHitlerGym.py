import gymnasium
from gymnasium import spaces


class SecretHitlerEnv(gymnasium.Env):

    # Add "env_config:Dict" to __init__ to enable it to work with ray RLlib algorithms
    def __init__(self):     
        
               
        # 0-8 for choosing a player (nominate or exec actions)
        # 0-1 for voting/veto 0 -> no 1->yes
        self.action_space = spaces.Discrete(9)

        self.observation_space = spaces.Dict(
            {
                "phase" : spaces.Discrete(8),
                "current_role": spaces.Discrete(3),
                "is_president": spaces.Discrete(2), 
                "is_chancellor": spaces.Discrete(2), 
                "current_policies": spaces.Discrete(4), # policies in hand
                "current_players_alive": spaces.Discrete(10), # players alive
            }
        )
        
        self.obs_space_dict = {
            "phase":0,
            "current_role":0,
            "is_president":0, 
            "is_chancellor":0, 
            "current_policies":0,
            "current_players_alive":0,
        }
    

    def overwrite_obs_space(self, dict):
        self.obs_space_dict = dict
            
    
    def step(self, action):
        terminated = False
        reward = 0
        info = {}

        # Comment this out when learning is done.
        # self.obs_space_dict["phase"] += 1


        # 1 - Nominate Chancellor
        if self.obs_space_dict["phase"] == 1:
            if action < self.obs_space_dict["current_players_alive"]:
                # should choose a valid alive player
                reward = 10
            else:
                reward = -200
        
        # 2 - Vote
        elif self.obs_space_dict["phase"] == 2:
            if action == 0 or action == 1:
                reward = 10
            else:
                reward = -200

        # 3 - Discard
        elif self.obs_space_dict["phase"] == 3:
            # if Liberal
            if self.obs_space_dict["current_role"] == 0:
                if action < self.obs_space_dict["current_policies"]:
                    reward = 10
                else:
                    reward = -200
            # if Fasc/Hitler
            else:
                if action < self.obs_space_dict["current_policies"]:
                    reward = 10
                else:
                    reward = -200

        # 4 - Veto
        elif self.obs_space_dict["phase"] == 4:
            if action == 0 or action == 1:
                reward = 10
            else:
                reward = -200
                

        # 5 - Executive action
        elif self.obs_space_dict["phase"] == 5:
            if action < self.obs_space_dict["current_players_alive"]:
                # should choose a valid alive player
                reward = 10
            else:
                reward = -200
        
        elif self.obs_space_dict["phase"] == 6:
            terminated = True

        return self.obs_space_dict, reward, terminated, False, info

    def reset(self, *, seed=None, options=None):
        self.obs_space_dict["phase"] = 0
        info = {}
        return self.obs_space_dict, info

