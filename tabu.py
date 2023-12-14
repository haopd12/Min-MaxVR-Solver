import numpy as np
import time
import copy
from datetime import datetime
import heapq

# Load data from openerp
def load_data_openerp(path = "./test/test3.txt"):
    with open(path, 'r') as f:
        inputData = f.readlines()
    line_1 = inputData[0].strip().split(' ')
    N = int(line_1[0])
    K = int(line_1[1])
    node_list=[]
    for node in inputData[1:]:
        #del '\n'
        node = node.strip()
        #split by ' '
        node = node.split(' ')
        row = []
        for n in node:
            row.append(n)
        node_list.append(row)
        del row
    node_list = np.array(node_list, dtype= "float64")
    return node_list, N, K

def load_result_openerp(path = "./test/result.txt"):
  with open(path, 'r') as f:
        inputData = f.readlines()
  X = [[] for i in range(20)]
  for i in range (2,42,2):
      node = inputData[i].strip().split(' ')
      # print(i)
      for n in node:
          X[int(i/2-1)].append(int(n))
  return X
# dis_matrix, N, K =load_data_openerp()
# print(dis_matrix)

"""# META HEURISTIC USING TABU SEARCH"""

# random initialization from N nodes and K people
def init(K,N):
  X = [[0] for i in range(K)]
  for i in range(N):
    a = np.random.random_integers(0,K-1)
    X[a].append(i+1)
  return X
def init_greedy(K,N, dis_matrix):
  heap = []
  dis_dis = []
  points = list(range(1 , N+1))
  points.sort(key=lambda x:dis_matrix[x][0],reverse=False)
  for i in range(K):
      # heapq.heappush(heap,(dis_matrix[0][points[0]],dis_matrix[0][points[0]],[0,points[0]],[0,points[0]]))
    road = []
    road.append(0)
    road.append(points[0])
    heap.append(road)
    dis_dis.append(dis_matrix[points[0]][0])
    points.remove(points[0])

  # index = 0
  while (len(points)>0):
    index = np.argmin(dis_dis)
    temp = heap[index]
    current_point = temp[-1]
    min_distance = 9999
    next_point = points[0]
    for point in points:
      if (dis_matrix[point][current_point] < min_distance):
        min_distance = dis_matrix[point][current_point]
        next_point = point
    points.remove(next_point)
    heap[index].append(next_point)
    dis_dis[index] = dis_dis[index] + dis_matrix[next_point][current_point]
    # index = (index + 1) % K
  
  return heap

# calculate dis => sum of distance people matrix 
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
# road = load_result_openerp()
# road.pop(-1)
# print(road)
# print(calculate_dis(road, dis_matrix, K).max())
# Get neighbors of previous solution by put 1 element of the person
  # with the longest path and putting it in any position of the person 
  # with the lowest path
def getNeighbors(X, K, index_max, index_min, dis_matrix):
    neighbors = []
    index_candidate = 0
    dis = calculate_dis(X, dis_matrix, K)
    for i in range(len(X[index_max])-1):
        Y = copy.deepcopy(X)
        a = np.random.randint(1,len(X[index_min])+1)
        tmp = X[index_max][i+1]
        Y[index_max].remove(tmp)
        Y[index_min].insert(a, tmp)
        neighbors.append(Y)
    return neighbors

# X = init(K,N)
# dis = calculate_dis(X, dis_matrix, K)
def tabu_search(N, K, dis_matrix):
    initial_time = datetime.now()
    # random initialization from N nodes and K people
    # X = init(K,N)
    X = init_greedy(K,N, dis_matrix)
    print(X)
    dis = calculate_dis(X, dis_matrix, K)
    index_max, index_min = np.argmax(dis), np.argmin(dis)
    # create first global solution
    best_X = X
    best_dis = dis
    # create first local solution
    bestCandidate = X
    bestCandidateDis = calculate_dis(X, dis_matrix, K)
    # create tabu list where save moves of search
    tabuList = []
    tabuList.append((best_X[index_max],best_X[index_min])) 
    stop = False    
    # threshold of search if the solution doesn't improve                                                                                    
    best_keep_turn = 0

    #loop search the best solution
    while not stop:
        index_max = np.argmax(bestCandidateDis)
        index_min = np.argmin(bestCandidateDis)
        #get neighbor list by putting 1 element of postman max to postman min
        # print(bestCandidate)
        NeighborX = getNeighbors(bestCandidate, K, index_max, index_min, dis_matrix)
        bestCandidate = NeighborX[0]
        bestCandidateDis = calculate_dis(bestCandidate,dis_matrix, K)

        # search for local solution where satisfies the condition that the best move isn't in tabuList
        for i, candidate in enumerate(NeighborX):
            candidateDis = calculate_dis(candidate, dis_matrix, K)
            if ((candidate[index_max], candidate[index_min]) not in tabuList) and (candidateDis.max()< bestCandidateDis.max()):
              bestCandidate = candidate
              bestCandidateDis = candidateDis
            # check if tabu list violation score is better than global solution?
            if ((candidate[index_max], candidate[index_min]) in tabuList) and (candidateDis.max()< best_dis.max()):
              best_X = candidate
              best_dis = candidateDis
              best_keep_turn = 0
              
        # compare global solution and local solution
        if (bestCandidateDis.max()<best_dis.max()):
            best_X = bestCandidate
            best_dis = bestCandidateDis
            best_keep_turn = 0
        # save move of local solution
        tabuList.append((bestCandidate[index_max], bestCandidate[index_min]))
        if (len(tabuList)> 1000):
            tabuList.pop(0)
        if best_keep_turn == 500:
            stop = True

        best_keep_turn += 1
        time = datetime.now()
        time_release = time - initial_time
        print("{}:Max distance: {}".format(time_release, bestCandidateDis.max()))
        
    for i in range(0,K):
      best_X[i].append(0)
    time = datetime.now()
    time_release = time - initial_time
    return best_X, best_dis.max(), time_release 

# def pineline(N, K, dis_matrix):

# dis_matrix, N, K =load_data_openerp()
# print(dis_matrix)
  
# time = datetime.now()
# best_X, best_dis, time = tabu_search(N, K, dis_matrix)

# print("_____________TABU_SEARCH________________")
# print(best_X)
# print(best_dis)

