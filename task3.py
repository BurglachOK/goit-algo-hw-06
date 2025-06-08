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
    graph[v][u] = weight  

# # Вивід перших 5 елементів
# for node in list(graph)[:5]:
#     print(f"{node}: {graph[node]}")

def dijkstra(graph, start):
    # Ініціалізація відстаней та множини невідвіданих вершин
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    unvisited = list(graph.keys())

    while unvisited:
        # Знаходження вершини з найменшою відстанню серед невідвіданих
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        # Якщо поточна відстань є нескінченністю, то ми завершили роботу
        if distances[current_vertex] == float('infinity'):
            break

        for neighbor, weight in graph[current_vertex].items():
            distance = distances[current_vertex] + weight

            # Якщо нова відстань коротша, то оновлюємо найкоротший шлях
            if distance < distances[neighbor]:
                distances[neighbor] = distance

        # Видаляємо поточну вершину з множини невідвіданих
        unvisited.remove(current_vertex)

    return distances

# Виклик функції для вершини A
print(dijkstra(graph, 'Iowa'))

