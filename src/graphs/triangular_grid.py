X_DIFFERENCE = lambda tuple_1, tuple_2: tuple_1[0] - tuple_2[0]
Y_DIFFERENCE = lambda tuple_1, tuple_2: tuple_1[1] - tuple_2[1]
MANHATTAN_DISTANCE = lambda tuple_1, tuple_2: abs(tuple_1[0] - tuple_2[0]) + abs(tuple_1[1] - tuple_2[1])

CONDITION_1 = lambda tuple_1, tuple_2: MANHATTAN_DISTANCE(tuple_1, tuple_2) == 1
CONDITION_2 = lambda tuple_1, tuple_2: MANHATTAN_DISTANCE(tuple_1, tuple_2) == 2 and X_DIFFERENCE(tuple_1, tuple_2) != Y_DIFFERENCE(tuple_1, tuple_2) and abs(Y_DIFFERENCE(tuple_1, tuple_2)) == abs(X_DIFFERENCE(tuple_1, tuple_2)) == 1
EDGE_CONDITION = lambda tuple_1, tuple_2: CONDITION_1(tuple_1, tuple_2) or CONDITION_2(tuple_1, tuple_2)

def define_graph(n):

    vertices_coordinate = [(x, n_i - x) for n_i in range(n+1) for x in range(n_i +1) ]
    vertices_code = list(range(len(vertices_coordinate)))
    code_to_coordinate = dict(zip(vertices_code, vertices_coordinate))
    coordinate_to_code = dict(zip(vertices_coordinate, vertices_code))

    adjacency_list_coordinate = {initial_vertex: [final_vertex for final_vertex in vertices_coordinate if EDGE_CONDITION(initial_vertex, final_vertex)] for initial_vertex in vertices_coordinate}
    adjacency_list_code = {coordinate_to_code[initial_vertex]: [coordinate_to_code[final_vertex] for final_vertex in adjacency_list_coordinate[initial_vertex] ] for initial_vertex in adjacency_list_coordinate}

    edges_code = list(set([tuple(sorted([initial_vertex, final_vertex])) for initial_vertex in adjacency_list_code for final_vertex in adjacency_list_code[initial_vertex]]))
    edges_coordinate = [(code_to_coordinate[edge[0]], code_to_coordinate[edge[1]]) for edge in edges_code]

    degrees = {vertex: len(adjacency_list_code[vertex]) for vertex in adjacency_list_code}
    border = [(0,0)] + [(i, 0) for i in range(1, n+1)] + [(0, i) for i in range(1, n+1)] + [(n-i, i) for i in range(1, n)]

    details =  {
        "miscelaneous": {
            "degree": degrees,
            "border": border
        },
        "code": {
            "vertices": vertices_code,
            "edges": edges_code,
            "adjacency_list": adjacency_list_code,
            "to_coordinate": code_to_coordinate
        },
        "coordinate": {
            "vertices": vertices_coordinate,
            "edges": edges_coordinate,
            "adjacency_list": adjacency_list_coordinate,
            "to_code": coordinate_to_code
        }
    } 
    return details

if __name__ == "__main__":
    information = define_graph(4)
    print(information)