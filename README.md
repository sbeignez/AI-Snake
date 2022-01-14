# AI-Snake Competition
![](https://img.shields.io/badge/Status-In--Progress-orange)

![snake](docs/img/AI-Snake.Screen.256.png)

---
## 1. Presentation

### 1.1. Problem definition

#### 1.1.1. Origin

Nokia original game:
* https://playsnake.org

#### 1.1.2. Rules and Objective

* Max: Score/Max_Score
    * Eat a maximum number of apples
    * Until end/win the game (max apples = rows * cols - snake.init_len)
* Min: Step/Score
    * With the minimum number of time-steps


#### 1.1.3. The problem as a graph

Shortest distance in a time dependant graph.

Partly Stochastic: next objective location is unkonwn and random.   


#### 1.1.4. The problem as a Markov Decision MDP  

States space:  
Actions space:  
Transitions: Deterministic (vs. Probabilistic). P(s, a, Succ(s,a)) = 1  
Rewards:  

### 1.2 The Snake Competition

#### 1.2.1. _
todo

#### 1.2.2. Game variations

The game can be modified for the competition:

Parameters | Nokia | Snake Competition
---| ----- | ---
Board size | _ rows x 15 cols | 30 rows x 30 cols
Snake Starting length | 3 body parts | 1 body part
Snake Starting position | Top Center | Random 
Snake Starting direction | Top-Down | n/a

#### 1.2.3. Performance indicators

1) The Game Completion Score (GCS)
    - Avg. score over the maximum score (Score = number of Apples eaten)
    - Obj: Maximise (up to 100%)  
2) The Game Over rate (GOR)
    - Number of game_over / total_games played  
    - Objective: Minimize  
3) The Performance rate (PR)
    - Avg. ( number of Steps / score )  
    - Obj: Minimise 
    - Max: n^2    
4) The Performance Rate at 0% and at 1% (PR0 and PR1)
    - The Performance rate with 0% Game-over rate (all win)
    - The Performance rate with a Game-over rate < 1%

---
## 2. Possible appoaches

* A. Operational Research 
    * A1. **Graph theory**   
        Pathfinding algorithms, such as: Dijkstra, A*..   
        To research: Pathfinding in time-dependent graphs
    * A2. **Optimization**  
        Method: Linear Programming
    * A3. **Genetic algorithm**   
        NEAT algo with NN
* B. AI Machine Learning
    * B1. **Supervised Learning** Deep Learning  
        Methods: Neural Network, Deep (DNN), Convo (CNN)
    * B2. **Reinforcement Learning (RL)**  
        Q-value iteration    
        Deep Q-Netwrok (DQN)  
        Further: Advantage Actor-Critic (A2C), Proximal Policy Optimization (PPO), Monte Carlo Tree Search

---
## 3. Current Development

Game features:

- General
    - [x] Basic game logic
    - [x] Human agent (Keyboard)
    - [x] Create GIU using pygame
    - [x] Refactor code using OOP
    - [x] Separate Engine and Agent logic
    - [ ] Refactor Session/Engine class for OpenAI Gym interface Env()
    - [ ] Refactor Agent
- History
    - [ ] Record Episodes
- Replay and Tests
    - [ ] Save env states and solutions
    - [ ]   
- Benchmarking
    - [ ]

A1. Pathfinding Algorithms:
- [x] Add Greedy algo / agent
- [x] Add A* algo / agent
- [x] Add Modes: Play and Benchmark
- [ ] Logging history
- [ ] Create snapshot of game configuration/situation/..
- [ ] Replay of snapshots
- [ ] Rewind steps (manual)

A3. Evolution/Genetic algorithm selecting NN:
- [ ] 

B1. Supervised Learning: Deep Learning:
- [ ] Generating Training data

B2. Reinforcement Learning:
1. Q-Learning
- [ ] 

2. Deep Q-Learning
- [ ] 

---

[![GitHub stars](https://img.shields.io/github/stars/sbeignez/AI-Snake.svg)](https://github.com/sbeignez/AI-Snake) [![GitHub stars](https://img.shields.io/github/last-commit/sbeignez/AI-Snake.svg)](https://github.com/sbeignez/AI-Snake)