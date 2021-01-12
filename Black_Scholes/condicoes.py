
from abc import ABC, abstractmethod
import numpy as np


class conditions_base(ABC):

    def __init__(self, variaveis, tipo = 'European', opcao = 'Put'):

        self.variaveis = variaveis
        self.tipo = tipo
        self.opcao = opcao
        self.k1 = (2 * self.variaveis.r) / (self.variaveis.v**2)
        super().__init__()

        @abstractmethod
        def left(self, x, t):
            pass

        @abstractmethod
        def right(self, x, t):
            pass

        @abstractmethod
        def initial(self, x):
            pass


class conditions(conditions_base):

    def left(self, x, t):

        if self.opcao == 'Call':
            return 0
        else:
            return np.exp(0.5 * (self.k1 - 1) * x + 0.25 * ((self.k1 - 1)**2) * t)

    def right(self, x, t):

        if self.opcao == 'Call':
            return np.exp(0.5 * (self.k1 + 1) * x + 0.25 * ((self.k1 + 1)**2) * t) - np.exp(0.5 * (self.k1 - 1) * x + 0.25 * ((self.k1 - 1)**2) * t)
        else:
            return 0

    def initial(self, x):

        if self.opcao == 'Call':
            return np.maximum(np.exp(0.5 * (self.k1 + 1) * x) - np.exp(0.5 * (self.k1 - 1) * x), 0)
        else:
            return np.maximum(np.exp(0.5 * (self.k1 - 1) * x) - np.exp(0.5 * (self.k1 + 1) * x), 0)
