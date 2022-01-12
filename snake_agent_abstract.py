from abc import (ABC, abstractmethod, )
from snake_utils import *


class Agent(ABC):

    def __init__(self, session, agent):
        self._session = session
        self.paths = []

    # @property
    # @abstractmethod
    # def session(self):
    #     return self._session

    @abstractmethod
    def next_move(self):
        pass
