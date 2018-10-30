import random, itertools
import numpy as np

#N  cubes implementation

from utils import Trie
from math import log2

class Dolphinn:
     def __init__(self, P, D, K, N):
         self.P=P
         self.D=D
         self.K=K
         self.N = N
         self.h = [0 for i in range (N)]
         self.cubes = [0 for i in range(N)]
         for k in range(N):
             self.h[k]=np.random.multivariate_normal(np.zeros(K), np.eye(K), size=self.D)
             X=np.sign(P.dot(self.h[k]))
             self.cubes[k]= Trie(K)
             self.cubes[k].setRoot((X[0], 0))
             for i in range(1,len(X)):
                self.cubes[k].insert(X[i], i)

                 

     def queries(self, Q, M, num_of_probes):
        n=0
        flag=False
        num_of_probes = int(num_of_probes/self.N) 
        qrange = int(log2(num_of_probes+2)+1)       #upper log
        #Queries
        #assign keys to queries
        A = [0 for i in range(self.N)]
        for i in range (self.N):
          A[i]=np.sign(Q.dot(self.h[i]))

        solQ=[]
        for j in range(len(A[0])):
           cands=[]
           for i in range(self.N):
              cands.extend(self.cubes[i].rangeq(A[i][j], qrange))             
           if len(cands)>M:
              args=np.argpartition([np.linalg.norm(np.subtract(self.P[i],Q[j])) for i in cands],M)
              sols=[]
              for i in range(M):
                   sols.append(cands[args[i]])    
              solQ.append(sols)       
           else:
              solQ.append([-1])
        return solQ
