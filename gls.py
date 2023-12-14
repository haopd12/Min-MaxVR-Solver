import numpy as np
import time
import copy

def loadData(path = "./test/test2.txt"):
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
# N,K,dis_matrix = loadData()

def init(K,N):
  X = [[0] for i in range(K)]
  for i in range(N):
    a = np.random.randint(0,K)
    X[a].append(i+1)
  return X

def calculateDis(X, dis_matrix, K):
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

def calculateCandidate(Q, dis_matrix):
  dis = 0
  for i in range(len(Q) - 1):
    dis += dis_matrix[Q[i]][Q[i+1]]
  dis += dis_matrix[Q[-1]][Q[0]]
  return dis

def augmentedDisMatrix(dis_matrix, penalties, eta):
  return dis_matrix + eta * penalties

def utilityFunction(edge, tour, dis_matrix, penalties):
  if set(edge).issubset(tour):
    [i, j] = edge
    penalty = penalties[i][j]
    distance = dis_matrix[i][j]
    return distance / (1 + penalty)
  else:
    return 0

def guidedLocalSearch(N, K, dis_matrix):
  start_time = time.time()
  X = init(K, N)
#   print(X)
#   print(calculateDis(X, dis_matrix, K).max())

  eta = 0.25
  penalties = np.zeros([N+1,N+1])
  utilities = np.zeros([N+1,N+1])
  amDisMatrix = augmentedDisMatrix(dis_matrix, penalties, eta)
  def localSearch(X, dis_matrix, K):
    penalized_edge = [0 for _ in range(2)]
    curDis = calculateDis(X, dis_matrix, K)
    improved = True
    while improved:
      improved = False
      for i in range(K):
        for j in range (1, len(X[i]) - 1):
          for k in range(j + 1, len(X[i])):
            if (k == j):
              continue
            temp_X = copy.deepcopy(X)
            temp_X[i] = X[i][:j] + X[i][j:k+1][::-1] + X[i][k+1:]
            newDis = calculateDis(temp_X, dis_matrix, K)
            if newDis.max() < curDis.max():
              X = temp_X
              curDis = newDis
              penalized_edge = [int(X[i][j]), int(X[i][k])]
              utilities[int(X[i][j])][int(X[i][k])] = utilityFunction(penalized_edge, X[i], dis_matrix, penalties)
              if utilities[int(X[i][j])][int(X[i][k])] == utilities.max():
                penalties[int(X[i][j])][int(X[i][k])] += 1
              improved = True
    return X
  best_X = localSearch(X, amDisMatrix, K)
  eta = eta * (calculateDis(best_X, dis_matrix, K).max()/N)
  X = best_X

  for _ in range(0,300):
    amDisMatrix = augmentedDisMatrix(dis_matrix, penalties, eta)
    best_X = localSearch(X, amDisMatrix, K)
    X = best_X
  dis = calculateDis(X, dis_matrix, K)
  end_time = time.time()
  # print(end_time)
  time_load = round(end_time - start_time, 3)
#   print(utilities)
#   print(penalties)
  print(time_load)
  for road in X:
    road.append(0)
  print(X)
  return X, dis.max(), time_load

# best_X, best_dis, time_load = guidedLocalSearch(N, K, dis_matrix)
# for i in range(0,len(best_X)):
#   best_X[i].append(best_X[i][0])
# print(best_X)
# print(best_dis.max())
# print(time_load)