

import numpy as np

class functions(object):

    # Thomas algorithm for solving three-dimensional systems

    def thom(self, a, b, c, d):

        n = len(d)
        a1, b1, c1, d1 = map(np.array, [a, b, c, d])
        x = np.zeros(n)

        c1[0] /= b1[0]
        for i in range(1, n):
            c1[i] = c1[i] / (b1[i] - a1[i] * c1[i - 1])
        d1[0] /= b1[0]
        for i in range(1, n):
            d1[i] = (d1[i] - a1[i] * d1[i - 1]) / (b1[i] - a1[i] * c1[i - 1])
            x[n - 1] = d1[n - 1]
        for i in range(n - 2, -1, -1):
            x[i] = d1[i] - c1[i] * x[i + 1]
        return x

    # Auxiliary function

    def join(self, ind, a, C, C1, m):

        ans = a * (-4 * C[ind,1:-1] + C[ind - 1,1:-1])
        ans1 = np.concatenate(([2 * C1[ind + 1,0]], np.zeros(m - 3), [2 * C1[ind + 1,-1]]))
        return (ans - ans1)
