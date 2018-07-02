import sys
sys.path.append('/usr/local/lib/python3.4/dist-packages/')
import numpy as np


def fvecs_read(filename):
    fv = np.fromfile(filename, dtype=np.float32)
    if fv.size == 0:
         raise IOError("Empty dataset in " + filename)
    dim = fv.view(np.int32)[0]
    if dim <= 0:
        raise IOError("Dimension <=0 in " + filename)
    fv = fv.reshape(-1, 1 + dim) 
    if not all(fv.view(np.int32)[:, 0] == dim):
        raise IOError("Non-uniform vector sizes in " + filename)
    fv = fv[:, 1:]
    fv = fv.copy()
    return (dim,fv)
def findmean(P, D, r):
    if len(P)>1000:
        s=int(len(P)/r)
    else:
        s=len(P)
    #randomly sample pointset
    J=np.random.choice(range(len(P)),s)
    m=np.zeros(D)
    for i in J:
        m=np.add(m,P[i])
    m=np.divide(m,s)
    return m
def isotropize(P, D, m):
     #find mean in order to isotropize
    for i in range(len(P)):
        P[i]=np.subtract(P[i],m)
    return P






#TODO
#consider saving both the int and the vector
#to optimize for both search and result gathering

class Trie:

    idxset = []
    tqr = 0

    class Node:

        def __init__(self, val):
            self.l = None
            self.r = None
            self.val = val
        def insert(self, key, val, s):
            # if node is leaf (aka contains a vector)
            if self.isLeaf():
                idx = Trie.findDif(self.val[0] , key, s)
                if idx == -1:           # if equals
                    return 0

                # change the type of this node
                # add the vectors to it's children
                if key[idx] == 1:
                    self.r = Trie.Node((key,val))
                    self.l = Trie.Node(self.val)
                else:
                    self.l = Trie.Node((key,val))
                    self.r = Trie.Node(self.val)

                # value stores the ith bit that is changed
                self.val = idx
            else:
                s.add(self.val) 
                if key[self.val] == 1:
                    self.r.insert(key, val,  s)
                else:
                    self.l.insert(key, val, s)

        #r-distance range query
        # val : query vector
        # r   : maximum radius
        # D   : Dimension - Depth
        def rangeq(self, key, r, D):

            if self.isLeaf():
                if Trie.hammingDist(key,self.val[0]) <= Trie.tqr:
                    return [self.val[1]]
                else:
                    return []

            if (r > D):
                return self.gatherall()
            
            if r < 0:
                return []            
            rv = []

            if (key[self.val] == 1):
                rv += (self.r.rangeq(key, r, D-1))
                rv += (self.l.rangeq(key, r-1, D-1))
            else:
                rv += (self.r.rangeq(key, r-1, D-1))
                rv += (self.l.rangeq(key, r, D-1))

            return rv

        def gatherall(self):
            if self.isLeaf():
                return [self.val[1]]

            rv = self.l.gatherall()
            rv += (self.r.gatherall())
            return rv

        #debugging function
        def print(self):

            if self.isLeaf():
                print ("~",self.val)
            else:
                print ("X:",self.val)
                self.l.print()
                self.r.print()





        def isLeaf(self):
            return self.l == None and self.r == None

    def findDif(v, u, st):
        for i in Trie.idxset:
            if i not in st and v[i] != u[i]:
                return i
        return -1

    def hammingDist(v, u):
        return abs(np.sum(np.bitwise_xor(u,v)))/2

    def __init__(self, D):
        self.D = D
        self.root = None
        Trie.idxset = [i for i in range(D)]

    def setRoot(self, node):
        key,val = node
        key = key.astype(int)
        self.root = Trie.Node((key,val))


    def insert(self , key, val):
        s = set([])
        key = key.astype(int)
        self.root.insert(key, val, s)

    def rangeq(self , q, r):
        Trie.tqr = r
        q = q.astype(int)
        return self.root.rangeq(q,r,self.D)

    #debugging function
    def print(self):
        self.root.print()





