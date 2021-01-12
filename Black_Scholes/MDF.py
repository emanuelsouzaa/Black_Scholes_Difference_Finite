from abc import ABC, abstractmethod
import numpy as np


class MDF_Base(ABC):

    def __init__(self, condicoes, funcoes, m, n, s, w):

        try:
            self.condicoes = condicoes
            self.funcoes = funcoes
            assert m >= 0
            self.m = m
            assert n >= 0
            self.n = n
            assert s[0] < s[1]
            self.s = s
            self.w = w
            self.t_max = (self.condicoes.variaveis.v**2 * self.condicoes.variaveis.T) / 2
            self.x_max = np.log((self.s[1]) / self.condicoes.variaveis.K)
            self.x_min = np.log(self.s[0] / self.condicoes.variaveis.K)
            self.x = np.linspace(self.x_min, self.x_max, self.m + 1)
            self.t = np.linspace(0, self.t_max, self.n + 1)
            self.X, self.T = np.meshgrid(self.x, self.t)
            self.dx = np.diff(self.x)[0]
            self.dt = np.diff(self.t)[0]
            self.alpha = (self.dx**2) / (self.w * self.dt)
            self.C = np.zeros((self.n + 1, self.m + 1))
            self.G = np.zeros((self.n + 1, self.m + 1))
            super().__init__()
        except:
            raise ValueError(' Inconsistent or missing data !! ')

    @abstractmethod
    def calc_conditions(self):
         pass

    @abstractmethod
    def solution(self):
        pass


class solve(MDF_Base):

    def calc_conditions(self):

        self.C[0,:] = self.condicoes.initial(self.x)
        self.C[:,0] = self.condicoes.left(self.x_min, self.t)
        self.C[:,-1] = self.condicoes.right(self.x_max, self.t)

        if self.condicoes.tipo == 'American':
            if self.condicoes.opcao == 'Call':
                self.G = (np.exp(0.25 * (self.condicoes.k1 + 1)**2 * self.T) * np.maximum(np.exp(0.5 * (self.condicoes.k1 + 1) * self.X)
                          - np.exp(0.5 * (self.condicoes.k1 - 1) * self.X), 0))
                self.G[0,:] = self.C[0,:]
                self.G[:,0] = self.C[:,0]
                self.G[:,-1] = self.C[:,-1]
            else:
                self.G = (np.exp(0.25 * (self.condicoes.k1 + 1)**2 * self.T) * np.maximum(np.exp(0.5 * (self.condicoes.k1 - 1) * self.X)
                          - np.exp(0.5 * (self.condicoes.k1 + 1) * self.X), 0))
                self.G[0,:] = self.C[0,:]
                self.G[:,0] = self.C[:,0]
                self.G[:,-1] = self.C[:,-1]

    def solution(self):

        self.calc_conditions()

        # u1 calculation

        a_1 = np.concatenate(([0], -1 * np.ones(self.m - 2)))
        c_1 = np.concatenate((-1 * np.ones(self.m - 2), [0]))
        b_1 = np.repeat((2 + self.alpha), self.m - 1)
        d_1 = self.alpha * self.C[0, 1:-1]
        d_1[0] += self.C[1,0]
        d_1[-1] += self.C[1,-1]
        res = self.funcoes.thom(a_1, b_1, c_1, d_1)

        if self.condicoes.tipo == 'American':

            self.C[1,1:-1] = np.maximum(res, self.G[1,1:-1])

            # Calculation of other solutions

            a_k = np.concatenate(([0], 2 * np.ones(self.m - 2)))
            c_k = np.concatenate((2 * np.ones(self.m - 2), [0]))
            b_k = np.repeat(-(3 * self.alpha + 4), self.m - 1)

            for k in range(1, self.n):
                d_k = self.funcoes.join(k, self.alpha, self.C, self.G, self.m)
                res = self.funcoes.thom(a_k, b_k, c_k, d_k)
                self.C[k + 1,1:-1] = np.maximum(res, self.G[k + 1,1:-1])

        else:

            self.C[1,1:-1] = res

            # Calculation of other solutions

            a_k = np.concatenate(([0], 2 * np.ones(self.m - 2)))
            c_k = np.concatenate((2 * np.ones(self.m - 2), [0]))
            b_k = np.repeat(-(3 * self.alpha + 4), self.m - 1)

            for k in range(1, self.n):
                d_k = self.funcoes.join(k, self.alpha, self.C, self.C, self.m)
                self.C[k + 1,1:-1] = self.funcoes.thom(a_k, b_k, c_k, d_k)
