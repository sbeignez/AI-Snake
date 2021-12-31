# Snake challenge 

## 1. Rules

* Board size: 30x30  
* Starting snake length: 3 
* Starting position: center  
* Starting direction: (free?)
* Game over rate < 0.01%

Nokia original game:
* https://playsnake.org
* Board size: ?? W x 15H
* Starting snake length: 3 
* Starting position: center: Top Center 
* Starting direction: Down


## 2. References

#### Algorithmic methods
  1. Pathfinding
      1. Shortest path problems
          - https://en.wikipedia.org/wiki/Shortest_path_problem
      1. A* Pathfinding Algorithm
         http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
  1. Hamiltonian loop
#### Machine Learning
  1. Supervised Learning
  1. Neurale Network, trained by Gradient Descent  
  1. Neural Networks, selected by Genetic algorithm
  - Re-inforcement Learning
    - Q Learning
    - Deep Q Learning


## 3. Public Projects

* Code Bullet  
    * Video 1: [A.I. Learns to play Snake using Deep Q Learning](https://www.youtube.com/watch?v=3bhP7zulFfY&ab_channel=CodeBullet)
    * Video 2: [I Created a PERFECT SNAKE A.I.](https://www.youtube.com/watch?v=tjQIO1rqTBE)
    * GitHub: [Code-Bullet/SnakeFusion](https://github.com/Code-Bullet/SnakeFusion) - 
* AlphaPhoenix
    * [Video](https://www.youtube.com/watch?v=TOpBcfbAgPg&ab_channel=AlphaPhoenix)
* Jack of Some
    * Video: [Neural Network Learns to Play Snake using Deep Reinforcement Learning](https://www.youtube.com/watch?v=i0Pkgtbh1xw) - March 2020
    * GitHub: ??
* V.Gedace  
    * [Generic solution for the Snake game via Hamiltonian Cycle and additional abbreviation logic.](https://www.youtube.com/watch?v=UI_I6sJXaJw&t=45s&ab_channel=V.Gedace) - Video - Oct 2020  
    * GitHub: [Hamiltonian-Cylce-Snake](https://github.com/UweR70/Hamiltonian-Cylce-Snake) - C# - Algo / Hamiltonian-Cycle
* Pyhton Engineer
    * [Teach AI To Play Snake - Reinforcement Learning Tutorial With PyTorch And Pygame (Part 1)](https://www.youtube.com/watch?v=PJl4iabBEz0&ab_channel=PythonEngineer) - Dec 2020
    * GitHub [snake-ai-pytorch](https://github.com/python-engineer/snake-ai-pytorch)
* Alex Patrenko
    * [Advantage Actor-Critic solves 6x6 Snake (Reinforcement Learning)](https://www.youtube.com/watch?v=bh_5aIqVTUY) - Apr 2018
    * GitHub: [snake-rl](https://github.com/alex-petrenko/snake-rl) - Python - RL Reinforcement Learning, "Monte-Carlo rollout into the future predicted by DNN"
    * GitHub: [sample-factory](https://github.com/alex-petrenko/sample-factory) - Python - Asynchronous reinforcement learning, samples
* Paweł Kamiński
    * Blog: [Training an AI bot to play Snake](https://www.codeer.dev/blog/2020/05/03/ai-snake.html)
    * Video: [AI learns to play Snake - Deep Q Learning - Neural Network](https://www.youtube.com/watch?v=ozFDavKIvpk&ab_channel=Pawe%C5%82Kami%C5%84ski)
    * GitHub: [AI-Snake](https://github.com/pawelkami/AI-Snake) - Python - Deep Reinforcement Learning algorithm, Deep Q Neural Network


* Others:
    * GreerViau [GreerViau](https://www.youtube.com/watch?v=zIkBYwdkuTk&ab_channel=GreerViau)

* To watch:
    * Square Robot [Square Robot](https://www.youtube.com/watch?v=8cdUree20j4&ab_channel=SquareRobots)
    * Ludius0 [..](https://www.youtube.com/watch?v=7Vh77YytDgg&ab_channel=ludius0)


* Dijkstras Algorithm, A*
  * https://www.youtube.com/watch?v=-L-WgKMFuhE&ab_channel=SebastianLague
  * https://www.gamedeveloper.com/programming/toward-more-realistic-pathfinding
  * https://www.researchgate.net/publication/237197542_Shortest_Path_Finding_Problem_in_Stochastic_Time-Dependent_Road_Networks_With_Stochastic_First-In-First-Out_Property
  * https://neo4j.com/developer/graph-data-science/path-finding-graph-algorithms/



### 2.b Technics



## 2. link

[Link to reference](#2-link)


---
Video: Jack   
www.wandb.com ?

NN Learning need learning data  

exploration strategy:
- epsilon greedy (exploration: random move / explotation: NN output)



64 snakes games running in parallel, 16 steps, >> train

RL Improvements:
- Advantage Actor-Critic (A2C)
- Proximal Policy Optimization (PPO) OpenAI
- Monte Carlo Tree Search

Use a model (model-free vs. ..)  
Calculate the next few frames

AlphaGo: 

---
Q-Learning:
* States S
* Actions A
* Transition proba T(s, a, s')
* Rewards R(s, a, s')

States:
* Me:  
  - ??
  - Current direction
* PE
  - Danger (R,L,S)
  - Direction (NSEW)
  - Food (NSEW)

Actions:
- 4 directions (N,S,E,W) or 3 relative actions (turn right, turn left, go straight = continue) relative to current direction

MODEL

FFNN (feed forward NN): 
- input layer size = State dim (one hot)
- output layer size = Actions dim (3)
