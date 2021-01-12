
from abc import ABC, abstractmethod
import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import norm as N
import matplotlib.pyplot as plt


class data_base(ABC):

    def __init__(self, MDF, variaveis):
        self.MDF = MDF
        self.variaveis = variaveis


    @abstractmethod
    def Exata(self, S):
         pass

    @abstractmethod
    def Value(self, S):
         pass

    @abstractmethod
    def plot(self, graph):
         pass


class data(data_base):

    def Exata(self, S):

        d1 = (np.log(S / self.variaveis.K) + (self.variaveis.r + self.variaveis.v**2 / 2) * self.variaveis.T) / (self.variaveis.v * np.sqrt(self.variaveis.T))
        d2 = d1 - (self.variaveis.v * np.sqrt(self.variaveis.T))

        if self.MDF.condicoes.opcao == 'Call':
            preco = S * N.cdf(d1) - self.variaveis.K * np.exp(-self.variaveis.r * self.variaveis.T) * N.cdf(d2)
        else:
            preco =  self.variaveis.K * np.exp(-self.variaveis.r * self.variaveis.T) * N.cdf(-d2) - S * N.cdf(-d1)

        return preco

    def Value(self, S):

        a1 = -0.5 * (self.MDF.condicoes.k1 - 1)
        b1 = -0.25 * (self.MDF.condicoes.k1 + 1)**2
        back = self.variaveis.K * np.exp(a1 * self.MDF.X + b1 * self.MDF.T) * self.MDF.C
        Si = self.variaveis.K * np.exp(self.MDF.x)
        f = interp1d(Si, back[-1,:])
        return f(S)

    def plot(self, graph = 0):

        s_new = np.linspace(self.MDF.s[0], self.MDF.s[1], 1500, dtype = 'float32')
        c_new = self.Value(s_new)
        c_ext = self.Exata(s_new)
        err = ((c_new - c_ext)**2) / len(c_new)



        if graph == 1:

            if self.MDF.condicoes.tipo == 'European':

                plt.plot(s_new, err, color = 'Black')
                plt.xlabel('Price')
                plt.ylabel('Error')
                plt.show()

            else:
                print('Inconsistent !!!')


        elif graph == 2:

            if self.MDF.condicoes.tipo == 'European':

                plt.figure( figsize=(15, 15))
                plt.rcParams.update({'font.size': 20})
                plt.plot(s_new, c_ext, color = 'black', label = 'Exact', linewidth=2.5)
                plt.plot(s_new, c_new, color= 'blue', label = 'Approximate',linewidth=2.5)
                plt.xlabel('Price')
                plt.ylabel('Premium')
                plt.legend()
                plt.savefig('Figure_1.png')
                plt.show()

            else:
                print('Inconsistent !!!')

        else:

            plt.plot(s_new, c_new, color = 'Black')
            plt.xlabel('Price')
            plt.ylabel('Premium')


            plt.show()
