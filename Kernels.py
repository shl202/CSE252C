
# coding: utf-8

# In[1]:

import numpy as np

class Kernel:
    def __init__(self):
        pass

    def Eval(self, x1, x2=None):
        pass


class LinearKernel(Kernel):
    def __init__(self):
        Kernel.__init__(self)

    def Eval(self, x1, x2=None):
        if x2 is not None:
            x11 = np.array(x1)
            x22 = np.array(x2)
            return np.dot(x11, x22)
        else:
            return np.linalg.norm(x1)


class GaussianKernel(Kernel):
    def __init__(self, sigma):
        Kernel.__init__(self)
        self.sigma = sigma

    def Eval(self, x1, x2=None):
        if x2 is not None:
            # print("x1 - x2")
            # print(x1 - x2)
            # tmp = np.array(x1-x2, dtype = np.float32)
            # norm_val = (np.linalg.norm(x1 - x2, ord=2))
            x11 = np.array(x1)
            x22 = np.array(x2)
            norm_val = (np.linalg.norm(x11 - x22)) ** 2
            # print(-1 * float(self.sigma))
            # print(norm_val)
            return np.exp(-1 * float(self.sigma) * norm_val)
            # inner = map(lambda d: -1*float(self.sigma)*d, (x1-x2))
            # return np.exp(np.linalg.norm(inner))
        else:
            return 1.0


class IntersectionKernel(Kernel):
    def __init__(self):
        Kernel.__init__(self)

    def Eval(self, x1, x2=None):
        if x2 is not None:
            x11 = np.array(x1)
            x22 = np.array(x2)
            return np.sum(np.minimum(x11, x22))
        else:
            return np.sum(x1)


#complete
class Chi2Kernel(Kernel):
    def __init__(self):
        Kernel.__init__(self)

    def Eval(self, x1, x2=None):
        if x2 is not None:
            x11 = np.array(x1)
            x22 = np.array(x2)
            result = 0.0
            for i in range(len(x1)):
                a, b = x11[i], x22[i]
                result += (a-b)*(a-b)/(0.5*(a+b)+1e-8)
            return 1.0 - result
        else:
            return 1.0



#complete    
class MultiKernel(Kernel):
    def __init__(self, kernels, featureCounts):
        Kernel.__init__(self)
        self.numKernel, self.norm, self.kernels, self.counts = len(kernels), 1.0/len(kernels), kernels, featureCounts

    def Eval(self, x1, x2=None):
        total, start = 0.0, 0.0
        if x2 is not None:
            for i in range(self.numKernel):
                c = self.counts[i]
                total += self.norm * self.kernels[i].Eval(x1[start:start+c], x2[start:start+c])
                start+=c
        else:
            for i in range(self.numKernel):
                c = self.counts[i]
                total += self.norm * self.kernels[i].Eval(x1[start:start+c])
                start+=c
        return total
