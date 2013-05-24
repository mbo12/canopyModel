import math
import numpy
import numpy.random as random
import time
def squaredDistance( x,y):
  return (x**2+y**2)

### shuffling/subsample alg 
def subsample(population,numToSample):
  n = len(population)
  for i in range(numToSample):
    ind = random.randint(i,n-1)
    swap = population[ind]
    population[ind] = population[i]
    population[i] = swap
  return population[:numToSample]


### take an position index and return x,y coords
def indToCoords(index):
  x = int(index/500)+12 #M
  y = index%500 + 12
  return x,y
  
        
class Model() :
  def __init__(self):
   self.k = 3
   self.M = 12
   ## initialize local distance to neighbors matrix
   self.distance = numpy.zeros((2*self.M+1,2*self.M+1))
   for i in range(-self.M,self.M+1):
     for j in range(-self.M,self.M+1):
       if i==0 and j == 0: 
         self.distance[i+self.M,j+self.M] = 0
         continue
       self.distance[i+self.M,j+self.M] = (math.pow(squaredDistance(abs(i),abs(j)),-self.k/2))
   self.weighted = self.distance.sum()
   self.distance = self.distance/self.distance.sum()
   
   self.PLOTSIZE = 500
   self.POSITIONS = numpy.arange((self.PLOTSIZE)**2)
   self.INDPOSITIONS = []
   for i in self.POSITIONS:
     self.INDPOSITIONS.append(indToCoords(i))
   
   
   self.fracStar = 0.4  ### global expected fraction of trees
   self.frac = 0.5      ### current actual fraction of trees
   self.dFrac = 1.0/self.PLOTSIZE/self.PLOTSIZE ### change in tree density per
                                                ### death of tree
   
   
   
   ### spatial map of trees (trees[i,j]==1 if tree is present at i,j)
   self.trees = numpy.zeros((self.PLOTSIZE+2*self.M,self.PLOTSIZE+2*self.M))
   for j in subsample(self.POSITIONS,int(len(self.POSITIONS)*self.frac)):
     x,y = self.INDPOSITIONS[j]
     self.trees[x,y] = 1
   
   self.wrapAround()  ###  multiplication faster by allowing indices to wraparound
   self.established = []
   self.dead = []
   for i in range(self.PLOTSIZE+2*self.M):
     for j in range(self.PLOTSIZE+2*self.M):
       if self.trees[i,j]:
         self.established.append([i,j])

      
  def neighborhoodDensity(self,x,y):
    ### calculate local tree density
    return (self.trees[x-self.M:x+self.M+1,y-self.M:y+self.M+1]*self.distance).sum()
  
  
  def wrapAround(self):
    ### do the reflection to handle edge case (assume trees wrap around)
    self.trees[:,self.M+self.PLOTSIZE:]= self.trees[:,self.M:2*self.M]
    self.trees[:,:self.M] = self.trees[:,self.PLOTSIZE:self.M+self.PLOTSIZE]
    self.trees[self.M+self.PLOTSIZE:,] = self.trees[self.M:2*self.M,:]
    self.trees[:self.M,:] = self.trees[self.PLOTSIZE:self.M+self.PLOTSIZE,:]  
    return
    
    
  def aliveTrees(self):
   return self.trees
    
  def killTree(self,x,y):
    self.trees[x,y] = 0

  def establishTree(self,x,y):
    self.trees[x,y] = 1
  
  
  ### 1 timestep in model
  def transition(self):
    self.established = []
    self.dead = []
    for j in subsample(self.POSITIONS,int(len(self.POSITIONS)/5)):
      x,y = self.INDPOSITIONS[j]
      if self.trees[x,y]:
        prob = (1 - self.neighborhoodDensity(x,y)) + (self.frac-self.fracStar)/self.frac
        if random.random() <= prob:
          self.killTree(x,y)
          self.dead.append([int(x),int(y)])
          self.frac-=self.dFrac
      else:
        prob = self.neighborhoodDensity(x,y) + (self.fracStar - self.frac)/(1- self.frac)
        if random.random() <= prob:
          self.establishTree(x,y)  
          self.established.append([int(x),int(y)])
          self.frac+= self.dFrac    
    self.wrapAround()


