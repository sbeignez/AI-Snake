from snake_utils import *
from snake_agent_ai import *
from snake_agent_astar import *
from snake_agent_greedy import *
from snake_agent_bfs import *
from snake_agent_rl_qlearning import *

class AgentFactory():

    def __init__(self, session, agent_type : Agents):
        self._session = session
        self._agent_type = agent_type


    def get_agent(self):
        if self._agent_type == Agents.AGENT_GREEDY:
            return AgentGreedy(self._session, self._agent_type)
        elif self._agent_type == Agents.AGENT_A_STAR:
            return AgentAStar(self._session, self._agent_type)
        elif self._agent_type == Agents.AGENT_BFS:
            return AgentBFS(self._session, self._agent_type)
        elif self._agent_type == Agents.AGENT_SUPER_STAR:
            return AgentSuperStar(self._session, self._agent_type)
        elif self._agent_type == Agents.AGENT_Q_LEARNING:
            return AgentQLearning(self._session, self._agent_type)
        else:
            raise ValueError("Agents type incorrect")


