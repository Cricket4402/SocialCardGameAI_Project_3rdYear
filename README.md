# SocialCardGameAI_Project_3rdYear
AI for social card game AI project (3rd year).


REQUIRED:
- Python version 3.10 (RLlib not supported on 3.12)
- pip install pytorch
- pip install -U "ray[rllib]"
- pip install gymnasium
- pip install gym
- pip install matplotlib
- pip install tensorflow
- pip install keras
- pip install keras-rl2
- pip install stable-baselines3

## To run games
- Download and extract the folder named "SocialCardGameAI_Project_3rdYear"
- Open terminal and navigate to the folder using the "cd" command
- Run the game_environment.py file by typing "python game_environment.py"
- If you want to change the number of games played, change the value of n in the file
- Note: games over 1000 take a long time (~20 mins)

## To train a new model
- Delete SHModel.zip
- Run sb3_dqn.py with "python sb3_dqn.py"