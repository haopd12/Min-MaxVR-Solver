from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.collections import LineCollection
from tabu import tabu_search
from gls import guidedLocalSearch
from hill_climbing import hill_climbing
from Greedy import solution
import numpy as np
import argparse

# N = 10
# K = 2
colors = [
    'blue', 'green', 'purple', 'orange', 'cyan', 'brown', 'pink', 'yellow', 'gray',
    'darkred', 'darkblue', 'darkgreen', 'darkpurple', 'darkorange', 'darkcyan', 'darkbrown', 'darkpink', 'darkyellow', 'darkgray',
    'lightred', 'lightblue', 'lightgreen', 'lightpurple', 'lightorange', 'lightcyan', 'lightbrown', 'lightpink', 'lightyellow', 'lightgray',
    'firebrick', 'royalblue', 'limegreen', 'darkslategray', 'darkolivegreen', 'deepskyblue', 'saddlebrown', 'hotpink', 'gold', 'darkslateblue',
    'crimson', 'mediumblue', 'forestgreen', 'darkorchid', 'darkgoldenrod', 'dodgerblue', 'sienna', 'palevioletred', 'khaki', 'slateblue',
    'tomato', 'midnightblue', 'seagreen', 'mediumorchid', 'peru', 'lightskyblue', 'chocolate', 'indianred', 'darkkhaki', 'mediumpurple',
    'orangered', 'navy', 'olivedrab', 'rebeccapurple', 'darkmagenta', 'skyblue', 'rosybrown', 'deeppink', 'darkolivegreen', 'slategray',
    'maroon', 'darkslateblue', 'teal', 'darkviolet', 'darkseagreen', 'lightsteelblue', 'burlywood', 'indigo', 'darkgreen', 'mediumvioletred',
    'mediumseagreen', 'violet', 'lime', 'mediumaquamarine', 'mediumslateblue', 'mediumturquoise', 'palegreen', 'darkturquoise', 'thistle',
    'darkcyan', 'lightseagreen', 'lavender', 'darkred', 'mediumspringgreen', 'cadetblue', 'palegoldenrod', 'darkorange', 'plum', 'lightcoral'
]

# Print the first 10 colors as an example
# print(colors[:10])

# gen random points
def generate_test(K,N):
    f = open('generated_test', 'w')
    f.write(str(N+1)+'\n')
    f.write(str(K) + '\n')
    f.write('0 0\n')

    for i in range(N):
        x = np.random.randint(-100, 100)
        y = np.random.randint(-100, 100)
        f.write('{} {}\n'.format(x, y))

    f.close()

# generate_test(K,N)

def load_data(path = "generated_test"):
    with open(path, 'r') as f:
        inputData = f.readlines()
    
    N = int(inputData[0].strip())
    K = int(inputData[1].strip())
    node_list=[]
    for node in inputData[2:]:
        #del '\n' 
        node = node.strip()
        #split by ' '
        node = node.split(' ')
        node_list.append((int(node[0]), int(node[1])))

    return node_list, N, K
# node_list, N, K = load_data()
def DistanceMatrix(cities, n):
    dis_matrix = np.zeros([n,n])
    min_dis = np.full((n, 2), np.inf)
    adv0 = []
    for i in range(n):
        for j in range(i+1, n):
            a = np.array(cities[i])
            b = np.array(cities[j])
            c = a - b
            dis_matrix[i, j] = np.sqrt(np.sum(c*c))
            if dis_matrix[i, j] < min_dis[i, 1]:
              min_dis[i, 0] = j
              min_dis[i, 1] = dis_matrix[i, j]
            dis_matrix[j, i] = dis_matrix[i, j]
            if dis_matrix[j, i] < min_dis[j, 1] and i != 0:
              min_dis[j, 0] = i
              min_dis[j, 1] = dis_matrix[i, j]
            if i == 0: adv0.append((dis_matrix[i, j], j))
    
    adv0.sort(key=lambda tup: tup[0], reverse = False)

    return np.around(dis_matrix, 2), np.around(min_dis, 2), adv0

def pipeline(K, N, algo):
    # generate_test(K,N)
    node_list, N, K = load_data()
    dis_matrix, min_dis, adv0 = DistanceMatrix(node_list, N)
    # print((dis_matrix))
    if algo == 'TABU':
        best_X, best_dis, time = tabu_search(N-1, K, dis_matrix)
        time = str(time)
        time = time[6:11]
    elif algo == 'GLS':
        best_X, best_dis, time = guidedLocalSearch(N-1, K, dis_matrix)
    elif algo == 'HC':
        best_X, best_dis, time = hill_climbing(N-1, K, dis_matrix)
        time = str(time)[0:5]
    else:
        best_X, best_dis, time = solution(N-1, K, dis_matrix)
        time = str(time)[0:8]
    # for l in best_X:
    #     l.append(0)
    # print(best_X)


    points = node_list

    # Separate x and y coordinates
    x_coordinates, y_coordinates = zip(*points)
    x_coordinates = np.array(x_coordinates)
    y_coordinates = np.array(y_coordinates)
    # print(x_coordinates, y_coordinates)
    # Plot the points
    plt.scatter(x_coordinates, y_coordinates, color='red', marker='o')
    # for index, roadK in enumerate(best_X):
    
    # print(len(roadK))
    for index,roadK in enumerate(best_X):
        # print(roadK)
        for i in range(0, len(roadK)-1):
            # print(i)
            # print(roadK)
            plt.plot([x_coordinates[roadK[i]], x_coordinates[roadK[i+1]]], [y_coordinates[roadK[i]], y_coordinates[roadK[i+1]]], color=colors[index])

    
    plt.text((x_coordinates.max() + x_coordinates.min())/2, y_coordinates.max() + 30 , 'Fitness_score: {}'.format(best_dis), fontsize=12, color='red', ha='center', va='center')
    # Add labels and title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('N = {}, K = {}, time = {} s'.format(N-1,K,time))

    # Display the plot
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

# Add command-line arguments
    parser.add_argument('-n','--num_node', type=int, default=10, help='number of node')
    parser.add_argument('-k','--num_K', type=int, default=2, help='number of salesman')
    parser.add_argument('--algorithm', type=str, default='TABU', choices=['HC', 'GREEDY', 'GLS', 'TABU'], help='Algorithm')
    
    args = parser.parse_args()
    N = args.num_node
    K = args.num_K
    algo = args.algorithm
    pipeline(K,N, algo)