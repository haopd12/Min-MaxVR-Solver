import heapq
import time
def solution(n,k,distance):
    start_time = time.time()
    heap = []
    points = list(range(1 , n+1 ))
    points.sort(key=lambda x:distance[x][0],reverse=False)
    for i in range(k):
        heapq.heappush(heap,(distance[0][points[0]],distance[0][points[0]],[0,points[0]],[0,points[0]]))
        points.pop(0)
    for i in range(k):
        temp=heapq.heappop(heap)
        current_point = temp[3][-1]
        min_distance = 10**9
        min_point = 0
        for point in points:
            if distance[current_point][point] < min_distance:
                min_distance = distance[current_point][point]
                min_point = point
        heapq.heappush(heap,(temp[0]+min_distance,temp[1],temp[2]+[min_point],temp[3]))
    while points:
        first_route = heapq.heappop(heap)
        next_point = first_route[2][-1]
        current_point = first_route[3][-1]
        if next_point not in points:
            min_distance = 10**9
            min_point = 0
            for point in points:
                if distance[current_point][point] < min_distance:
                    min_distance = distance[current_point][point]
                    min_point = point
            min_tmp_distance = first_route[1] + distance[current_point][min_point]
            min_tmp_route = first_route[3] + [min_point]
            heapq.heappush(heap,(min_tmp_distance,first_route[1],min_tmp_route,first_route[3]))
        else:
         points.remove(next_point)
         current_distance = first_route[0]
         current_route = first_route[2]
         min_distance = 10**9
         min_point = 0
         for point in points:
            if distance[next_point][point] < min_distance:
                min_distance = distance[next_point][point]
                min_point = point
         if min_distance < 10**9 and min_point != 0:
            heapq.heappush(heap,(current_distance+min_distance,current_distance,current_route+[min_point],current_route))
         else:
            heapq.heappush(heap,(current_distance,current_distance,current_route,current_route))
    min_max_f = 0
    result = []
    while heap:
        first_courier = heapq.heappop(heap)
        final_distance = first_courier[1] + distance[first_courier[3][-1]][0]
        first_courier[3].append(0)
        if final_distance > min_max_f:
           min_max_f = final_distance
        result.append(first_courier[3])
    end_time = time.time()
    return result,min_max_f,end_time-start_time
#n, k = map(int, input().split())
#distance = [list(map(int, input().split())) for _ in range(n+1)]
# file_path = './ttest1.txt'
# with open(file_path, 'r') as file:
#     n, k = map(int, file.readline().strip().split())
#     distance = []
#     for _ in range(n+1):
#         row = list(map(int, file.readline().strip().split()))
#         distance.append(row)
# result,min_max_f,run_time = solution(n,k,distance)
# print(result)
# print(min_max_f)
# print(run_time)

