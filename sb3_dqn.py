from stable_baselines3 import DQN
import os.path
from stable_baselines3.common.env_checker import check_env


class DQNLoader:
    def __init__(self, model_name, env):
        check_env(env)
        self.env = env
        self.model = None
        self.model_name = model_name
        self.model_path =  model_name + ".zip"
        self.trained_model_exists = os.path.isfile(self.model_path)


    ################## SETUP ##################
    # If trained model exists, load it up
    def model_setup(self):
        if self.trained_model_exists:
            self.model = DQN.load(self.model_path, self.env)
            # print(f"Loaded: {self.model_path}")
        else:
            print(f"No model named {self.model_name} found, training one from scratch...")

            # Train model from scratch, then save it
            self.model = DQN("MultiInputPolicy", self.env, verbose=1)

            # Code snippet from Stable Baseline 3 DQN
            # Source: https://stable-baselines3.readthedocs.io/en/v2.3.0/modules/dqn.html
            self.model.learn(total_timesteps=100, log_interval=1000)
            self.model.save(self.model_name)

            print(f"Model trained. Can be found in {self.model_path}.")

    def load_with_custom_env(self, custom_env):
        if self.trained_model_exists:
            self.model = DQN.load(self.model_path, custom_env)
            print(f"Loaded: {self.model_path} with custom env")
        else:
            print(f"No model named {self.model_name} found, cannot load custom env")


    ################## TRAINING ##################
    # Train the model further
    def train_model_default(self):
        train_timesteps = 100000 # Timesteps to train for
        train_log_interval = 10000 # Log at this given episode count

        print(f"Proceeding to train model {self.model_path}...")
        self.model.learn(total_timesteps=train_timesteps, log_interval=train_log_interval)
        self.model.save(self.model_path)

    def train_model_custom_obs(self):
        new_obs_loop = 1000
        train_timesteps = 1000 # Timesteps to train for


        for i in range(new_obs_loop):
            # get random obs
            random_obs = self.env.observation_space.sample()
            self.env.overwrite_obs_space(random_obs)

            # load model with the new loaded obs
            # train model on new obs
            self.model.verbose = 0
            self.model.load(self.model_path, self.env)
            # print(f"Proceeding to train model {self.model_path}...")
            self.model.learn(total_timesteps=train_timesteps)
            self.model.save(self.model_path)
            if i % 100 == 0:
                print(f"iteration {i} trained")
        
        print(f"Trained for {new_obs_loop * train_timesteps} total steps.")


    ################## EVALUATION ##################
    # Test the model performance against the environment
    def evaluate_model(self):
        print("Evaluating agent...")

        # Code snippet from Stable Baseline 3 Examples
        # Source: https://stable-baselines3.readthedocs.io/en/master/guide/examples.html
        vec_env = self.model.get_env()
        obs = vec_env.reset()
        sum = 0
        eval_steps = 10000

        for i in range(eval_steps):
            action, _states = self.model.predict(obs, deterministic=True)
            print(action)
            obs, rewards, dones, info = vec_env.step(action)
            sum += rewards[0]
        print(f"Average reward: {sum/eval_steps}")

# RUN THIS FILE AS MAIN TO TRAIN
if __name__ == "__main__":
    from SecretHitlerGym import SecretHitlerEnv

    env = SecretHitlerEnv()

    x = DQNLoader("SHModel", env)
    x.model_setup()
    x.train_model_custom_obs()
