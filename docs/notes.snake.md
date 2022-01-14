# AI Snake 

## Problem definition

Graph:
- Pathfinding problem
- Shortest path (over all iterations)
- Deterministic Time-dependant graph (the snake tail changes graph)
- 
- ..

### 2.0.2 Objects  definition

> UML Graph of objects

* Game
    - GameParams (mode, ..)
    * UI [1]
    * Engine [1]
    * Session [1-*]
        - SessionParams (steps, points)
        * Agent [1][Abstract]
        * Board
        * Snake
        * Apple
        * History

The board:
* x: columns From 1, Axe: Horizontal, from Left to right
* y: rows From 1, Axe: vertical, from bottom to top


Python Libraries for viz:
* [v] Pygame
* Pyglet



# A1. Graph Theory and Pathfinding

## 2.1. Notes about Graph Theory

1. Graph
    1. Data structures for Graph-Network representations
        * Adjacent Matrix
        * Adjacent List / Set 
    1. Graph libraries  
        1. NetworkX
    1. Graph algorithms
        * Branch & Bound > Dynamic Prgramming > A* > Dijkstra
    1. Graph and Time
        * "Time-dependant", "Time variaing", "Temporal network", "evolving network", ..
    1. Graph concepts
        * Hamiltonian (hamiltonicity)
        * vs. Eulerian
        * path and cycles/ loop. Hamiltonian loop/cycle
        * Connectivity
        * 

## 2.2. Pathfinding Algorithms   

* Shortest path problems
    - https://en.wikipedia.org/wiki/Shortest_path_problem
* The Greedy algo
* The Dijkstras Algorithm 
* The A* Pathfinding Algorithm
    - http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
* Finding the K-shortest paths  
    [Alternative Routing: k-Shortest Paths with Limited Overlap](https://www.informatik.hu-berlin.de/de/forschung/gebiete/wbi/research/publications/2015/sigspatial_kshortest.pdf)

Source:  
* [Shortest Path Problem (Wiki)](https://en.wikipedia.org/wiki/Shortest_path_problem)  
 
* A star  
* [A* Pathfinding (E01: algorithm explanation)](https://www.youtube.com/watch?v=-L-WgKMFuhE&ab_channel=SebastianLague)
* [..](https://www.researchgate.net/publication/237197542_Shortest_Path_Finding_Problem_in_Stochastic_Time-Dependent_Road_Networks_With_Stochastic_First-In-First-Out_Property)
* [..](https://neo4j.com/developer/graph-data-science/path-finding-graph-algorithms/)

Pathfinding in a grid:
* https://harablog.wordpress.com/2011/08/26/fast-pathfinding-via-symmetry-breaking/amp/

## 2.3

Tools, Libraries  

## 2.4 Notes and Ideas

Problem definition:
* Graph with special properties: a GRID
    * Maximun number of vertices = 4
    * All distances = 1
* Time-dependant
    * Snake body desactivate nodes temporalily
* Objective
    * Next apple position is random

Strategy:
* Min ( path lenght to objective + avg. shortest path to all next possible objectives )

Functions to dev:
* is_valid_path()
* is_reachable( $f state_{board,snake} (objective) \to Bool $ )

Idea: the optimal paths don't need to respect cycle hamiltonicity, if {...}

### Create a library of Test cases for algorithm

* generation
    * By hand
    * By brute force
    * While learning / Record when failing

* archiving
    * what to store
        * initial state: board, snake body with sequence, apple
        * best solution(s) to reach apple
    * which representation, data structure?

* running tests
    * loading test(s) from archive
    * invoke agent
    * compare results
    * return Pass/Fail or a mark






# A2. Optimization & Linear programming 

* ...

# A3. Genetic algorithm with NN selection

# B1. Supervised Learning
Neural Network, trained by Gradient Descent  
NN type: deep FFNN, 

Feature engineering:

Point of view | "Bird view" | "Snake vision"
------------- | -------------- | -----------
.. | .. | From the pixel<br> global view (whole board) or local view (NxN matrix around head)
Actions | The 4 directions (N,S,E,W) | 3 actions (turn right, turn left, go straight) relative to snake body
.. | .. | - Distance head to Danger (R,L,S)<br> - Direction (NSEW)<br>  - Food (NSEW)

# B2. Re-inforcement Learning

Technics:
- Q Learning
- Deep Q Learning
- Advantage Actor-Critic (A2C)
- Proximal Policy Optimization (PPO)
- Monte Carlo Tree Search
* Policy Gradient Theorem
    * https://www.youtube.com/watch?v=cQfOQcpYRzE&ab_channel=ElliotWaite

## Q-Learning

Problem definition for Q-Learning

* States S
* Actions A
* Transition proba T(s, a, s')
* Rewards R(s, a, s')

Design issues:
* Model design: How to represent the States and Actions
* Reward design

Terminal:
* Game-over: hit tail or wall
* Loop: over (x) moves since last apple

Reward design:  
* Keep in the range [-1;+1]
* Reward when eating apple
* Parse reward issue
    * reward for getting closer to apple
    * Eval function


NN design
FFNN (feed forward NN): 
- input layer size = State dim (one hot)
- output layer size = Actions dim (3)





Tools:
* [Keras RL](https://keras.io/examples/rl/)
* [OpenAI GYM]()


# R. References

## R1. Open Projects - Solving Snake

* Code Bullet  
    * Video 1: [A.I. Learns to play Snake using Deep Q Learning](https://www.youtube.com/watch?v=3bhP7zulFfY&ab_channel=CodeBullet)
    * Video 2: [I Created a PERFECT SNAKE A.I.](https://www.youtube.com/watch?v=tjQIO1rqTBE)
    * GitHub: [Code-Bullet/SnakeFusion](https://github.com/Code-Bullet/SnakeFusion) - Language: Processing
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
* Square Robot
    * Video: [AI learns to play SNAKE using Reinforcement Learning](https://www.youtube.com/watch?v=8cdUree20j4&ab_channel=SquareRobots) - Q-Learning
    * Video: [AI learns to play SNAKE using Reinforcement Learning Part 2](https://www.youtube.com/watch?v=WjuLQVg04JY)

To watch:  

* Crispresso
    * Video: [AI Learns to play Snake!](https://www.youtube.com/watch?v=vhiO4WsHA6c&t=99s)
    * GitHub: [SnakeAI](https://github.com/Chrispresso/SnakeAI) - Python - RL
* XX
    * GreerViau [GreerViau](https://www.youtube.com/watch?v=zIkBYwdkuTk&ab_channel=GreerViau)
    * Ludius0 [..](https://www.youtube.com/watch?v=7Vh77YytDgg&ab_channel=ludius0)


## R2. Domain (References)

Graph / Pathfinding
* https://www.researchgate.net/publication/254184076_Neural_Networks_for_Real-time_Pathfinding_in_Computer_Games

AI
* https://www.davidsilver.uk/teaching/

RL
* https://www.youtube.com/watch?v=bD6V3rcr_54&list=LL&t=1333s
* Video: [Policy Gradient Theorem Explained - Reinforcement Learning](https://www.youtube.com/watch?v=cQfOQcpYRzE&ab_channel=ElliotWaite)




 



