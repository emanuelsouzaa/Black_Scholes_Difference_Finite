

class variable(object):

    def __init__(self, K, r, v, T):

        try:
            assert T > 0
            self.T = T
            assert K > 0
            self.K = K
            assert v >= 0
            self.v = v
            assert r >= 0
            self.r = r
        except:
            raise ValueError(' Inconsistent or missing data !! ')
