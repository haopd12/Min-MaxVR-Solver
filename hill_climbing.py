import numpy as np
import time
import copy

def load_data(path = './test/test2.txt'):
  with open(path, 'r') as f:
    inputData = f.readlines()
  N_K=inputData[0].strip().split(' ')
  N=int(N_K[0])
  K=int(N_K[1])
  dis_matrix = np.zeros([N+1,N+1])
  for i in range(0,N+1):
    tmp_data=inputData[i+1].strip()
    tmp_data=tmp_data.split(" ")
    for j in range(0,N+1):
      dis_matrix[i,j]=tmp_data[j]
  return N,K,dis_matrix

# N,K,dis_matrix=load_data()

def init(K,N):
 
  X = [[0] for _ in range(K)]
    
  for i in range(N):
        a = np.random.randint(0, K)
        X[a].append(i + 1)
  return X

def calculate_dis(X, dis_matrix, K):
  dis = np.zeros((K,1))
  for i in range(K):
    len_Xi = len(X[i]) - 1
    for j in range(len_Xi):
      a = int(X[i][j])
      b = int(X[i][j+1])
      dis[i] = dis[i] + dis_matrix[a][b]
    c = int(X[i][len_Xi])
    dis[i] = dis[i] + dis_matrix[c][0]
  return dis 

# X = init(K,N)
# dis = calculate_dis(X, dis_matrix, K)

def getNeighbors(X, index_max, index_min):
    neighbors = []
   # index_candidate = 0
   # dis = calculate_dis(X, dis_matrix, K)
    for i in range(len(X[index_max])-1):
        Y = copy.deepcopy(X)
        a = np.random.randint(1,len(X[index_min])+1)
        tmp = X[index_max][i+1]
        Y[index_max].remove(tmp)
        Y[index_min].insert(a, tmp)
        neighbors.append(Y)
    return neighbors

def hill_climbing(N, K, dis_matrix ):
    start_time = time.time()
    X = init(K, N)
    dis = calculate_dis(X, dis_matrix, K)
    best_X = X
    best_dis = calculate_dis(X, dis_matrix, K)
    for _ in range(100):
        index_max = np.argmax(best_dis)
        index_min = np.argmin(best_dis)
        NeighborX = getNeighbors(best_X, index_max, index_min)     
        for neighbor in NeighborX:
            neighbor_dis = calculate_dis(neighbor, dis_matrix, K)
            max_neighbor_dis = max(neighbor_dis)
            if max_neighbor_dis < max(best_dis):
                best_X = neighbor
                best_dis = neighbor_dis
    for i in range(len(best_X)):
      best_X[i].append(0)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return best_X, best_dis.max(), elapsed_time

# print(pipeline(N,K,dis_matrix))