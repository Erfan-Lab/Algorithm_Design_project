import heapq
import math

class Graph:

    # initialize the graph with an empty adjacency list, delay dictionary for vertices,
    # and a boolean to indicate whether or not it has a negative edge.
    
    def __init__(self): 
        self.delays = {}
        self.adjacency_list = {}
        self.has_negative_edge = False
    
    # define a method to add a new vertex, add the delay to the dictionary, and add the vertex to the adjacency list. 
    
    def add_vertex(self, vertex_id, vertex_delay):
        self.delays[vertex_id] = vertex_delay

        if vertex_id not in self.adjacency_list:
            self.adjacency_list[vertex_id] = []

    # define a method to add a new edge, calculate the cost, add the vertices to the adjacency list,
    # and change the boolean for having a negative edge to True if we find any.

    def add_edge(self, source_id, destination_id, distance, traffic_coefficient, weather_coefficient):
        cost = (distance * traffic_coefficient * weather_coefficient) + self.delays[destination_id]
        
        if cost < 0:
            self.has_negative_edge = True
        
        self.adjacency_list[source_id].append((destination_id, cost))


def build_graph(file_path="map.txt"):

    # we build the graph, and start to add the edges and vertices from the txt file to construct the graph completely.

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

    # we write a function to construct the whole path, going back to each node's parent and reversing the path at the end. 

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

    # this function calculates the shortest paths to all vertices from the starting vertex, using the dijkstra algorithm.
    # we also keep the parent of each vertex so that we can construct the whole path after the whole algorithm is done.

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

    # in this function, we calculate the shortest path using the Bellman-Ford algorithm.
    # we check whether or not we have a negative cycle. if we do, the problem would be meaningless. 
    # if we don't, we would proceed to the next steps of the allgorithm to find the shortest path to each vertex.
    # like the dijkstra function, we keep the parents to make sure we can construct the complete path at the end. 

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

    # in this function, we choose to use the dijkstra algorithm if there exists no negative vertices, 
    # or to use the Bellman-Ford algorithm if there is at least one. 
    # we also construct and return the complete path and return both of these values,
    # (cost of the shortest path to destination, and the path itself). 

    if graph.has_negative_edge:
        shortest_distances, parent_vertices, has_negative_cycle = shortest_path_bellman_ford(graph, start_vertex)
        if has_negative_cycle:
            return None, math.inf
    else:
        shortest_distances, parent_vertices = shortest_path_dijkstra(graph, start_vertex)
        
    path = build_path(parent_vertices, start_vertex, destination_vertex)
    return path, shortest_distances[destination_vertex]


def multiple_destinations_shortest_path(graph, start_vertex, delivery_destinations):

    # for the multiple destinations shortest path problem, we will use a greedy approach. 
    # greedy might not always be the optimal answer, but the optimal solution to this problem is calculated in O(K! * E * V).
    # this is a huge time complexity, so to reduce the time complexity, we use a greedy approach,
    # to find a semi-optimal answer in O(K^2 * E * V).
    # while there are still unvisited paths, we search for the nearest vertex.
    # then, we go to the nearest vertex, we add it to the pass, and we mark it as read.
    # we continue this procedure until all of the vertices are visited. 
    # we also make sure to use the correct path finding algorithm according to the graph we are working on.
    # p.s : the time complexities are written for when the Bellman-Ford algorithm is chosen. 
    # when the dijkstra algorithm is chosen, the time complexities would shrink from O(EV) to O((E+V)log(V)).

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