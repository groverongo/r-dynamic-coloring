from RecursiveColoring import T_Grid_Graph
from graph_constants import MODEL_METHOD

def create_n_color_standard(n: int, r: int, k: int, output_file: str, output_directory: str = None, model_name: MODEL_METHOD = MODEL_METHOD.ACR):

    Grid = T_Grid_Graph(n, r, k)
    Grid.define_graph()

    new_edges: list[tuple[int, int]] = []
    if n == 2:
        new_edges = [
            [(0,0), (0,2)],
            [(0,0), (2,0)],
            [(0,2), (2,0)],
        ]
    elif n == 3:
        new_edges = [
            ((0,3), (0,1)),
            ((1,2), (3,0)),
            ((1,2), (2,0)),
            ((1,2), (1,0)),
            ((1,2), (0,1)),
            ((1,2), (0,0)),
        ]
    elif n >= 4:
        if n % 2 == 0:
            origin_connections_coordinate = (n//2, n//2)
            neighbor_omit_coordinates = [
                (origin_connections_coordinate[0] + 1 , origin_connections_coordinate[1] - 1),
                (origin_connections_coordinate[0] - 1 , origin_connections_coordinate[1] + 1)
            ]
        else:
            origin_connections_coordinate = (n//2+1, n//2)
            neighbor_omit_coordinates = [
                (origin_connections_coordinate[0] + 1 , origin_connections_coordinate[1] - 1),
                (origin_connections_coordinate[0] - 1 , origin_connections_coordinate[1] + 1)
            ]

        border_vertices_coordinates: list[tuple[int, int]] = list(Grid.details.coordinate.border)
        border_vertices_coordinates.remove(origin_connections_coordinate)
        border_vertices_coordinates.remove(neighbor_omit_coordinates[0])
        border_vertices_coordinates.remove(neighbor_omit_coordinates[1])

        new_edges = [(origin_connections_coordinate, v) for v in border_vertices_coordinates]
        

    Grid.add_edges(new_edges)
    Grid.linear_programming_model(model_name=model_name,previous_variables=None)
    Grid.coloring_assignment(coloring_function=None)
    Grid.coloring_table()
    Grid.graph_image(bw=False, label='coordinate', output_file=output_file, output_directory=output_directory)
    
for n in range(4, 5):
    for r in range(3, 4):
        create_n_color_standard(n, r, 5, f"Tstar{n}Max-{r}.png", model_name=MODEL_METHOD.ACR)
"""
Grid = T_Grid_Graph(3, 2, 8)
Grid.define_graph()
Grid.add_edges([
    ((0,3), (0,1)),
    ((1,2), (3,0)),
    ((1,2), (2,0)),
    ((1,2), (1,0)),
    ((1,2), (0,1)),
    ((1,2), (0,0)),
])
Grid.linear_programming_model(model_name='ACR',previous_variables=None)
Grid.coloring_assignment(coloring_function=None)
Grid.graph_image(bw=False, label='coordinate', output_file='TstarConcetrated.png')


Grid = T_Grid_Graph(3, 2, 8)
Grid.define_graph()
Grid.add_edges([
    ((0,3), (0,1)),
    ((0,3), (2,1)),
    ((0,3), (3,0)),
    ((0,0), (3,0)),
    ((0,0), (0,3)),
    ((1,0), (3,0)),
    
])
Grid.linear_programming_model(model_name='ACR',previous_variables=None)
Grid.coloring_assignment(coloring_function=None)
Grid.graph_image(bw=False, label='coordinate', output_file='TstarEquilibrium.png')



Grid = T_Grid_Graph(3, 2, 8)
Grid.define_graph()
Grid.linear_programming_model(model_name='ACR',previous_variables=None)
Grid.coloring_assignment(coloring_function=None)
Grid.graph_image(bw=False, label='coordinate', output_file='T.png')
"""