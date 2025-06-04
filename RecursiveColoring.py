from typing import Callable, Tuple, Union
from numpy import array
from numpy.typing import NDArray
from pulp import LpVariable, LpMinimize, LpStatus, LpProblem, lpSum, GLPK
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os
from graph_constants import AVAILABLE_COLORS, MODEL_METHOD, EDGE_CONDITION
from graph_details import Coloring_Solution, Graph_Colors, Graph_Details
        
class T_Grid_Graph():
    def __init__(self, n: int, r: int, k: int):
        self.n = n
        self.r = r
        self.k = k

    def define_graph(self):
        n = self.n

        vertices_coordinate = [(x, n_i - x) for n_i in range(n+1) for x in range(n_i +1) ]
        vertices_code = list(range(len(vertices_coordinate)))
        code_to_coordinate = dict(zip(vertices_code, vertices_coordinate))
        coordinate_to_code = dict(zip(vertices_coordinate, vertices_code))

        adjacency_list_coordinate = {initial_vertex: [final_vertex for final_vertex in vertices_coordinate if EDGE_CONDITION(initial_vertex, final_vertex)] for initial_vertex in vertices_coordinate}
        adjacency_list_code = {coordinate_to_code[initial_vertex]: [coordinate_to_code[final_vertex] for final_vertex in adjacency_list_coordinate[initial_vertex] ] for initial_vertex in adjacency_list_coordinate}

        edges_code = list(set([tuple(sorted([initial_vertex, final_vertex])) for initial_vertex in adjacency_list_code for final_vertex in adjacency_list_code[initial_vertex]]))
        edges_coordinate = [(code_to_coordinate[edge[0]], code_to_coordinate[edge[1]]) for edge in edges_code]

        degrees = {vertex: len(adjacency_list_code[vertex]) for vertex in adjacency_list_code}

        border_coordinate = [(0,0)] + [(i, 0) for i in range(1, n+1)] + [(0, i) for i in range(1, n+1)] + [(n-i, i) for i in range(1, n)]
        border_code = [coordinate_to_code[coordinate] for coordinate in border_coordinate]

        triad_candidates_coordinates = [((0, i), (0, i+1), (0, i+2)) for i in range(n-1)] + [((i, 0), (i+1, 0), (i+2, 0)) for i in range(n-1)] + [((n-i, i), (n-i-1, i+1), (n-i-2, i+2)) for i in range(n-1)]
        triad_candidates_code = [(coordinate_to_code[triad[0]], coordinate_to_code[triad[1]], coordinate_to_code[triad[2]]) for triad in triad_candidates_coordinates]

        self.details = Graph_Details(
            misc=Graph_Details.Misc(degree=degrees),
            code=Graph_Details.Graph_Info(
                vertices=vertices_code,
                edges=edges_code,
                adjacency_list=adjacency_list_code,
                to_other=code_to_coordinate,
                border=border_code,
                triad_candidates=triad_candidates_code
            ),
            coordinate=Graph_Details.Graph_Info(
                vertices=vertices_coordinate,
                edges=edges_coordinate,
                adjacency_list=adjacency_list_coordinate,
                to_other=coordinate_to_code,
                border=border_coordinate,
                triad_candidates=triad_candidates_coordinates
            )
        )

    def add_edges(self, edges:list[tuple[tuple[int, int], tuple[int, int]]]):
        for edge in edges:
            initial_vertex, final_vertex = edge
            self.details.coordinate.adjacency_list[initial_vertex].append(final_vertex)
            self.details.coordinate.adjacency_list[final_vertex].append(initial_vertex)
            self.details.coordinate.edges.append(tuple(sorted((initial_vertex, final_vertex))))

            initial_vertex_code = self.details.coordinate.to_other[initial_vertex]
            final_vertex_code = self.details.coordinate.to_other[final_vertex]
            self.details.code.adjacency_list[initial_vertex_code].append(final_vertex_code)
            self.details.code.adjacency_list[final_vertex_code].append(initial_vertex_code)
            self.details.code.edges.append(tuple(sorted((initial_vertex_code, final_vertex_code))))

        self.details.misc.degree = {vertex: len(self.details.code.adjacency_list[vertex]) for vertex in self.details.code.adjacency_list}
   
    def linear_programming_model(self, model_name: MODEL_METHOD, previous_variables=None):
        if model_name not in [MODEL_METHOD.ACR, MODEL_METHOD.ACR_H, MODEL_METHOD.ACR_R, MODEL_METHOD.ACR_RH]:
            raise ValueError(f"model_name must be '{MODEL_METHOD.ACR}', '{MODEL_METHOD.ACR_H}', '{MODEL_METHOD.ACR_R}' or '{MODEL_METHOD.ACR_RH}'")
        print(f'For n: {self.n}')
        print(f'For r: {self.r}')
        adjacency_list = self.details.code.adjacency_list
        edges = self.details.code.edges
        degrees = self.details.misc.degree
        k = self.k
        n = self.n
        r = self.r

        w: NDArray[LpVariable] = array([LpVariable(f"w({k_i})", 0, 1, cat="Binary") for k_i in range(k)])
        x: NDArray[NDArray[LpVariable]] = array([[LpVariable(name=f"x({v},{k_i})", lowBound=0, upBound=1, cat="Binary") for k_i in range(k)] for v in range(len(adjacency_list)) ])
        q: NDArray[NDArray[LpVariable]] = array([[LpVariable(name=f"q({v},{k_i})", lowBound=0, upBound=1, cat="Binary") for k_i in range(k)] for v in range(len(adjacency_list)) ])

        model = LpProblem(name=f'Coloring_T{n}', sense=LpMinimize)
        model += lpSum(w)


        if previous_variables and model_name in [MODEL_METHOD.ACR_R, MODEL_METHOD.ACR_RH]:
            for k_i in range(k):
                if previous_variables["w"][k_i].varValue == 0:
                    break
                model += w[k_i] == previous_variables["w"][k_i].varValue
            for v in range(previous_variables['x'].shape[0]):
                for k_i in range(k):
                    model += x[v, k_i] == previous_variables["x"][v, k_i].varValue

        # Constraint 1
        for v in adjacency_list.keys():
            model += lpSum(x[v]) == 1
        # Constraint 2
        for (u, v) in edges:
            for k_i in range(k):
                if model_name in [MODEL_METHOD.ACR_H, MODEL_METHOD.ACR_RH]:
                    model += x[u, k_i] + x[v, k_i] <= 1
                else:
                    model += x[u, k_i] + x[v, k_i] <= w[k_i]
        if model_name in [MODEL_METHOD.ACR, MODEL_METHOD.ACR_R]:
            # Constraint 3
            for k_i  in range(k):
                model += w[k_i] <= lpSum(x[:, k_i])
            # Constraint 4
            for k_i in range(1, k):
                model += w[k_i - 1] >= w[k_i]
        # Constraint 5
        for v, deg in degrees.items():
            model += lpSum(q[v]) >= min(r, deg)
        # Constraint 6
        for v, n_v in adjacency_list.items():
            for k_i in range(k):
                model += lpSum(x[n_v, k_i]) >= q[v, k_i]
        # Constraint 7
        for v, n_v in adjacency_list.items():
            for u in n_v:
                for k_i in range(k):
                    model += q[v, k_i] >= x[u, k_i]

        model.solve(solver=GLPK(msg=False))
        print(f'Result: {LpStatus[model.status]}')


        self.coloring_solution = Coloring_Solution(model=model, w=w, x=x, q=q)
    

    def coloring_assignment(self, coloring_function: Union[Callable[Tuple[int, int], int], None] = None):
        if coloring_function == None:
            x = self.coloring_solution.x
            to_coordinate = self.details.code.to_other

            color_assignment_code = {v: [x_vc.varValue for x_vc in x_v].index(1) for v, x_v in enumerate(x)}
            color_assignment_coordinate = {to_coordinate[v]: [x_vc.varValue for x_vc in x_v].index(1) for v, x_v in enumerate(x)}
        else:
            color_assignment_coordinate = {v: coloring_function(v) for v in self.details.coordinate.vertices}
            color_assignment_code = {self.details.coordinate.to_other[v]: c for v, c in color_assignment_coordinate.items()}
        self.graph_colors = Graph_Colors(
            code=color_assignment_code,
            coordinate=color_assignment_coordinate,
            used_colors=max(color_assignment_code.values()) + 1
        )
        print(f"Colors used: {self.graph_colors.used_colors}")

    def graph_image(self, bw=False, label='color', output_file: str = None, output_directory: str=None):
        vertices_coordinate = [str(v) for v in self.details.coordinate.vertices]
        edges_coordinate = [[str(initial_vertex),str(final_vertex)] for (initial_vertex, final_vertex) in self.details.coordinate.edges]
        color_assignment_coordinate = list({ str(v): AVAILABLE_COLORS[c] for v, c in self.graph_colors.coordinate.items()}.values())

        positions = dict(zip(vertices_coordinate, self.details.coordinate.vertices))
        if label=='color':
            labels = { str(v): c for v, c in self.graph_colors.coordinate.items()}
        elif label=='coordinate':
            labels = { str(v): str(v) for v in self.graph_colors.coordinate.keys()}
        elif label=='code':
            labels = { str(v): str(v) for v in self.graph_colors.code.keys()}
        else:
            raise ValueError("label must be 'color', 'coordinate' or 'code'")

        G = nx.Graph()
        G.add_nodes_from(vertices_coordinate)
        G.add_edges_from(edges_coordinate)
        plt.figure(figsize=(4+self.n, 4+self.n))
        
        options = {
            "node_color": "#000000" if bw else color_assignment_coordinate,
            'edge_color': 'black',
            "node_size": 1100,
            "with_labels": True,
            "labels": labels,
            "font_color": '#ffffff' if  bw else '#000000',
            'font_size': 11,
        }

        nx.draw(G, pos=positions, **options)
        plt.axis('equal')

        if output_directory == None:
            output_directory = "graphs"

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        if output_file == None:
            output_file = f'r{self.r}_n{self.n}_k{self.graph_colors.used_colors}.png'

        output_path = f'{output_directory}/{output_file}'
        plt.savefig(output_path)
        plt.clf()
        plt.close('all')

    def coloring_table(self):
        vertices_coordinate = [str(v) for v in self.details.coordinate.vertices]
        degrees_coordinate = [deg for deg in self.details.misc.degree.values()]
        color_assignment_coordinate = list({ str(v): c for v, c in self.graph_colors.coordinate.items()}.values())
        color_adjacent_coordinate = {str(v): [str(u) for u in self.details.coordinate.adjacency_list[v]] for v in self.details.coordinate.adjacency_list.keys()}
        print(vertices_coordinate)
        print(degrees_coordinate)
        print(color_assignment_coordinate)
        print(color_adjacent_coordinate)

    def export_solution(self):
        if not os.path.exists("graphs"):
            os.makedirs("graphs")
        
        x_values_matrix = pd.DataFrame([ [x_vc.varValue for x_vc in x_v] for x_v in self.coloring_solution.x])
        x_values_matrix.to_csv(f"graphs/r{self.r}_x.csv", index=False, header=False)
        q_values_matrix = pd.DataFrame([ [q_vc.varValue for q_vc in q_v] for q_v in self.coloring_solution.q])
        q_values_matrix.to_csv(f"graphs/r{self.r}_q.csv", index=False, header=False)
        w_values_matrix = pd.DataFrame([ [w_vc.varValue for w_vc in self.coloring_solution.w]])
        w_values_matrix.to_csv(f"graphs/r{self.r}_w.csv", index=False, header=False)

""" 
X_6_function = lambda v: (v[0]+5*v[1])%7
def X_4_function(v):
    i = v[0]
    j = v[1]
    if j==0:
        return i%6
    elif i==0 and j > 0:
        return (4-j)%6
    else:
        return (5+i-j)%6

class Use_Cases():
    def __init__(self, K: int, N: int, R: int):
        self.K = K
        self.N = N
        self.R = R

    def Graph_Only(n_min: int, n_max: int, skip):
        for n in range(n_min, n_max + 1, skip):
            T_n = T_Grid_Graph(n=n, r=R, k=K)

            

K = 8
N = 4
R = 5

# Use a for loop
T_nm1_coloring_solution = None
for n in range(N, N+1, 1):
    T_n = T_Grid_Graph(n=n, r=R, k=K)
    T_n.define_graph()
    # T_n.linear_programming_model(model_name='ACR-R',previous_variables=T_nm1_coloring_solution)
    T_n.coloring_assignment(coloring_function=lambda x: 0)
    T_n.graph_image(bw=True, label='coordinate')
    # T_n.export_solution()
    # T_n.coloring_table()
    # T_nm1_coloring_solution = T_n.coloring_solution

def build_experiment_table(r_min, r_max, n_min, n_max):
    results = {
        'r': [r for r in range(r_min, r_max+1)],
    }
    for n in range(n_min, n_max+1):
        results[f'T_{n}'] =  [] 
    for r in range(r_min, r_max+1):
        previous_solution = None
        for n in range(n_min, n_max+1):
            T_n = T_Grid_Graph(n=n, r=r, k=K)
            T_n.define_graph()
            T_n.linear_programming_model(previous_variables=previous_solution)
            T_n.coloring_assignment(coloring_function=None)
            previous_solution = T_n.coloring_solution
            results[f'T_{n}'].append(T_n.graph_colors.used_colors)
    experiment_table = pd.DataFrame(results)
    return experiment_table

# print(build_experiment_table(r_min=2, r_max=6, n_min=1, n_max=10).to_latex(index=False)) """