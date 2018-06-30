import random, itertools
import numpy as np

#N  cubes implementation

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
             b=np.array([2**j for j in range(self.K)])
             Y=X.dot(b)
             self.cubes[k]=dict([])
             for i in range(len(Y)):
                 if self.cubes[k].get(int(Y[i]))==None:
                      self.cubes[k][int(Y[i])]=[]
                 self.cubes[k][int(Y[i])].append(i)

     def queries(self, Q, M, num_of_probes):
        n=0
        flag=False
        num_of_probes = int(num_of_probes/self.N)
        combs=np.ones((num_of_probes,self.K))
        for r in range(self.K+1):
             for c in itertools.combinations(range(self.K),r):
                 for i in c:
                    combs[n,i]=-1
                 n=n+1
                 if n>=num_of_probes:
                    flag=True
                    break
             if flag:
                 break
        #Queries
        #assign keys to queries
        A = [0 for i in range(self.N)]
        for i in range (self.N):
          A[i]=np.sign(Q.dot(self.h[i]))
        b=np.array([2**j for j in range(self.K)])

        solQ=[]
        for j in range(len(A)):
           cands=[]
           N = [0 for i in range(self.N)]
           for k in range(self.N):
               N[k]=np.multiply(combs,A[k][j])
               N[k]=N[k].dot(b)
           for i in range(len(N[0])):
               for ii in range(self.N):
                  if self.cubes[ii].get(int(N[ii][i]))!= None:
                      cands.extend(self.cubes[ii][int(N[ii][i])])             
           if len(cands)>M:
              args=np.argpartition([np.linalg.norm(np.subtract(self.P[i],Q[j])) for i in cands],M)
              sols=[]
              for i in range(M):
                   sols.append(cands[args[i]])    
              solQ.append(sols)       
           else:
              solQ.append([-1])
        return solQ
