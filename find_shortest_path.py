import heapq
import math

class Graph:
    def __init__(self):
        self.delays = {}
        self.adjacency_list = {}
        self.has_negative_edge = False

    def add_vertex(self, vertex_id, vertex_delay):
        self.delays[vertex_id] = vertex_delay

        if vertex_id not in self.adjacency_list:
            self.adjacency_list[vertex_id] = []

    def add_edge(self, source_id, destination_id, distance, traffic_coefficient, weather_coefficient):
        cost = (distance * traffic_coefficient * weather_coefficient) + self.delays[destination_id]
        
        if cost < 0:
            self.has_negative_edge = True
        
        self.adjacency_list[source_id].append((destination_id, cost))


def build_graph(file_path="map.txt"):
    graph = Graph()
    try:
        with open(file_path, 'r') as map_file:
            for line in map_file:
                line = line.strip()
                data = line.split()
                if data[0] == 'V':
                    graph.add_vertex(data[1], float(data[2]))
                
                elif data[0] == 'E':
                    graph.add_edge(
                        data[1], 
                        data[2], 
                        float(data[3]), 
                        float(data[4]), 
                        float(data[5])
                    )
        return graph
    except:
        return None


def build_path(parent_vertices, start_vertex, destination_vertex):
    path = []
    current_vertex = destination_vertex
    
    while current_vertex:
        path.append(current_vertex)
        if current_vertex == start_vertex:
            break
        current_vertex = parent_vertices.get(current_vertex)
    
    if current_vertex != start_vertex:
        return []
    
    path.reverse()
    return path


def shortest_path_dijkstra(graph, start_vertex):
    shortest_distances = {vertex: math.inf for vertex in graph.delays}
    parent_vertices = {vertex: None for vertex in graph.delays}
    shortest_distances[start_vertex] = 0
    
    priority_queue = [(0, start_vertex)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_distance > shortest_distances[current_vertex]:
            continue
            
        for neighbor_vertex, cost in graph.adjacency_list[current_vertex]:
            if shortest_distances[current_vertex] + cost < shortest_distances[neighbor_vertex]:
                shortest_distances[neighbor_vertex] = shortest_distances[current_vertex] + cost
                parent_vertices[neighbor_vertex] = current_vertex
                heapq.heappush(priority_queue, (shortest_distances[neighbor_vertex], neighbor_vertex))
                
    return shortest_distances, parent_vertices


def shortest_path_bellman_ford(graph, start_vertex):
    shortest_distances = {vertex: math.inf for vertex in graph.delays}
    parent_vertices = {vertex: None for vertex in graph.delays}
    shortest_distances[start_vertex] = 0
    
    total_vertices = len(graph.delays)
    
    for _ in range(total_vertices - 1):
        for current_vertex in graph.delays:
            if shortest_distances[current_vertex] == math.inf:
                continue
            for neighbor_vertex, cost in graph.adjacency_list[current_vertex]:
                if shortest_distances[current_vertex] + cost < shortest_distances[neighbor_vertex]:
                    shortest_distances[neighbor_vertex] = shortest_distances[current_vertex] + cost
                    parent_vertices[neighbor_vertex] = current_vertex
                    
    for current_vertex in graph.delays:
        if shortest_distances[current_vertex] == math.inf:
            continue
        for neighbor_vertex, cost in graph.adjacency_list[current_vertex]:
            if shortest_distances[current_vertex] + cost < shortest_distances[neighbor_vertex]:
                return None, None, True
                
    return shortest_distances, parent_vertices, False


def find_optimal_shortest_path(graph, start_vertex, destination_vertex):
    if graph.has_negative_edge:
        shortest_distances, parent_vertices, has_negative_cycle = shortest_path_bellman_ford(graph, start_vertex)
        if has_negative_cycle:
            return None, math.inf
    else:
        shortest_distances, parent_vertices = shortest_path_dijkstra(graph, start_vertex)
        
    path = build_path(parent_vertices, start_vertex, destination_vertex)
    return path, shortest_distances[destination_vertex]


def multiple_destinations_shortest_path(graph, start_vertex, delivery_destinations):
    final_path = [start_vertex]
    current_location = start_vertex
    unvisited_destinations = set(delivery_destinations)
    total_cost = 0
    list_of_paths = []
    
    while unvisited_destinations:
        if graph.has_negative_edge:
            shortest_distances, parent_vertices, has_negative_cycle = shortest_path_bellman_ford(graph, current_location)
            if has_negative_cycle: 
                return None, 0, []
        else:
            shortest_distances, parent_vertices = shortest_path_dijkstra(graph, current_location)
            
        nearest_destination = None
        minimum_cost = math.inf
        
        for candidate_destination in unvisited_destinations:
            if shortest_distances[candidate_destination] < minimum_cost:
                minimum_cost = shortest_distances[candidate_destination]
                nearest_destination = candidate_destination
                
        if nearest_destination is None or minimum_cost == math.inf:
            return None, math.inf, []
            
        temporary_path = build_path(parent_vertices, current_location, nearest_destination)
        list_of_paths.append(temporary_path)
        
        final_path.append(nearest_destination)
        total_cost += minimum_cost
        current_location = nearest_destination
        unvisited_destinations.remove(nearest_destination)
        
    if graph.has_negative_edge:
        shortest_distances, parent_vertices, _ = shortest_path_bellman_ford(graph, current_location)
    else:
        shortest_distances, parent_vertices = shortest_path_dijkstra(graph, current_location)
        
    return_cost = shortest_distances[start_vertex]
    if return_cost == math.inf:
        return None, math.inf, []
        
    total_cost += return_cost
    final_path.append(start_vertex)
    list_of_paths.append(build_path(parent_vertices, current_location, start_vertex))
    
    return final_path, total_cost, list_of_paths