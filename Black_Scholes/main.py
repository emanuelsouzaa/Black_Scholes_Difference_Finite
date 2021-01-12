
# Importing packages

from variaveis import variable
from condicoes import conditions
from funcoes import functions
from MDF import solve
from dados import data

# Main

if __name__ == '__main__':

    T = 1                   # Maturity time
    K = 100                 # Strike price
    v = 0.4                 # Volatility
    r = 0.1                 # Interest rate
    m = 100                 # Number of intervals in the spatial variable
    n = 100                 # Number of intervals in the time variable
    s = [0.001, 1500]       # Price [min,max]
    w = 1

    # Variables

    var = variable(K, r, v, T)

    # Conditions

    cond = conditions(var, 'European', 'Put')

    # Functions

    func = functions()

    # Solves the equation

    resol = solve(cond, func, m, n, s, w)
    resol.solution()

    # Data analysis

    dt = data(resol, var)

    # graph plot

    # 0 - price x premium
    # 1 - price x error
    # 2 - exact x approx.

    dt.plot(2)
