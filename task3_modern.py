import urllib.request
import io
import zipfile
import networkx as nx
import random

url = "http://www-personal.umich.edu/~mejn/netdata/football.zip"

sock = urllib.request.urlopen(url)
s = io.BytesIO(sock.read())
sock.close()

zf = zipfile.ZipFile(s)
txt = zf.read("football.txt").decode()
gml = zf.read("football.gml").decode()
gml = gml.split("\n")[1:]
G = nx.parse_gml(gml)

# Побудова словника з вагами
graph = {}

for u, v in G.edges():
    weight = random.randint(1, 10)

    if u not in graph:
        graph[u] = {}
    if v not in graph:
        graph[v] = {}

    graph[u][v] = weight
    graph[v][u] = weight  # бо граф неорієнтований

# # Вивід перших 5 елементів
# for node in list(graph)[:5]:
#     print(f"{node}: {graph[node]}")



def print_table(distances, visited):
    # Верхній рядок таблиці
    print("{:<10} {:<10} {:<10}".format("Вершина", "Відстань", "Перевірено"))
    print("-" * 30)
    
    # Вивід даних для кожної вершини
    for vertex in distances:
        distance = distances[vertex]
        if distance == float('infinity'):
            distance = "∞"
        else:
            distance = str(distance)
        
        status = "Так" if vertex in visited else "Ні"
        print("{:<10} {:<10} {:<10}".format(vertex, distance, status))
    print("\\n")

def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    unvisited = list(graph.keys())
    visited = []

    while unvisited:
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        if distances[current_vertex] == float('infinity'):
            break

        for neighbor, weight in graph[current_vertex].items():
            distance = distances[current_vertex] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance

        visited.append(current_vertex)
        unvisited.remove(current_vertex)
        
        # Вивід таблиці після кожного кроку
        print_table(distances, visited)

    return distances

# Приклад графа у вигляді словника
# graph = {
#     'A': {'B': 5, 'C': 10},
#     'B': {'A': 5, 'D': 3},
#     'C': {'A': 10, 'D': 2},
#     'D': {'B': 3, 'C': 2, 'E': 4},
#     'E': {'D': 4}
# }

# Виклик функції для вершини A
dijkstra(graph, 'Iowa')