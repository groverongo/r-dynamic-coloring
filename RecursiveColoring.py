from numpy import array
from pulp import LpVariable, LpMinimize, LpStatus, LpProblem, lpSum, GLPK

class T_Grid_Graph():

    def __init__(self, n, r, k):
        self.n = n
        self.r = r
        self.k = k

    def define_graph(self):
        n = self.n
        manhattan_distance = lambda tuple_1, tuple_2: abs(tuple_1[0] - tuple_2[0]) + abs(tuple_1[1] - tuple_2[1])
        x_difference = lambda tuple_1, tuple_2: tuple_1[0] - tuple_2[0]
        y_difference = lambda tuple_1, tuple_2: tuple_1[1] - tuple_2[1]

        condition_1 = lambda tuple_1, tuple_2: manhattan_distance(tuple_1, tuple_2) == 1
        condition_2 = lambda tuple_1, tuple_2: manhattan_distance(tuple_1, tuple_2) == 2 and x_difference(tuple_1, tuple_2) != y_difference(tuple_1, tuple_2) and abs(y_difference(tuple_1, tuple_2)) == abs(x_difference(tuple_1, tuple_2)) == 1
        edge_condition = lambda tuple_1, tuple_2: condition_1(tuple_1, tuple_2) or condition_2(tuple_1, tuple_2)

        vertices_coordinate = [(x, n_i - x) for n_i in range(n+1) for x in range(n_i +1) ]
        vertices_code = list(range(len(vertices_coordinate)))
        code_to_coordinate = dict(zip(vertices_code, vertices_coordinate))
        coordinate_to_code = dict(zip(vertices_coordinate, vertices_code))

        adjacency_list_coordinate = {initial_vertex: [final_vertex for final_vertex in vertices_coordinate if edge_condition(initial_vertex, final_vertex)] for initial_vertex in vertices_coordinate}
        adjacency_list_code = {coordinate_to_code[initial_vertex]: [coordinate_to_code[final_vertex] for final_vertex in adjacency_list_coordinate[initial_vertex] ] for initial_vertex in adjacency_list_coordinate}

        edges_code = list(set([tuple(sorted([initial_vertex, final_vertex])) for initial_vertex in adjacency_list_code for final_vertex in adjacency_list_code[initial_vertex]]))
        edges_coordinate = [(code_to_coordinate[edge[0]], code_to_coordinate[edge[1]]) for edge in edges_code]

        degrees = {vertex: len(adjacency_list_code[vertex]) for vertex in adjacency_list_code}

        self.details =  {
            "miscelaneous": {
                "degree": degrees,
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
   
    def linear_programming_model(self, previous_variables=None):
        adjacency_list = self.details["code"]["adjacency_list"]
        edges = self.details["code"]["edges"]
        degrees = self.details["miscelaneous"]["degree"]
        k = self.k
        n = self.n
        r = self.r

        w = array([LpVariable(f"w({k_i})", 0, 1, cat="Binary") for k_i in range(k)])
        x = array([[LpVariable(name=f"x({v},{k_i})", lowBound=0, upBound=1, cat="Binary") for k_i in range(k)] for v in range(len(adjacency_list)) ])
        q = array([[LpVariable(name=f"q({v},{k_i})", lowBound=0, upBound=1, cat="Binary") for k_i in range(k)] for v in range(len(adjacency_list)) ])

        model = LpProblem(name=f'Coloring_T{n}', sense=LpMinimize)
        model += lpSum(w)


        if previous_variables:
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
                model += x[u, k_i] + x[v, k_i] <= w[k_i]
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
        print(LpStatus[model.status])


        self.coloring_solution = {
            "model": model,
            "w": w,
            "x": x,
            "q": q
        }
    

    def coloring_assignment(self):
        x = self.coloring_solution["x"]
        to_coordinate = self.details["code"]["to_coordinate"]

        color_assignment_code =  {v: [x_vc.varValue for x_vc in x_v].index(1) for v, x_v in enumerate(x)}
        color_assignment_coordinate =  {to_coordinate[v]: [x_vc.varValue for x_vc in x_v].index(1) for v, x_v in enumerate(x)}
        self.graph_colors = {
            "code": color_assignment_code,
            "coordinate": color_assignment_coordinate,
        }
        self.colors_used = max(color_assignment_code.values()) + 1
        print(f"Colors used: {self.colors_used}")

    def graph_image(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        color_map = ["#FFC0CB", "#90EE90", "#ADD8E6", "#FFFFE0", "#E6E6FA", "#FFD700", "#F0E68C", "#98FB98", "#F5DEB3", "#B0E0E6"]


        vertices_coordinate = [str(v) for v in self.details["coordinate"]["vertices"]]
        edges_coordinate = [[str(initial_vertex),str(final_vertex)] for (initial_vertex, final_vertex) in self.details["coordinate"]["edges"]]
        color_assignment_coordinate = list({ str(v): color_map[c] for v, c in self.graph_colors["coordinate"].items()}.values())

        positions = dict(zip(vertices_coordinate, self.details["coordinate"]["vertices"]))
        labels = { str(v): c for v, c in self.graph_colors["coordinate"].items()}

        G = nx.Graph()
        G.add_nodes_from(vertices_coordinate)
        G.add_edges_from(edges_coordinate)
        plt.figure(figsize=(4+self.n, 4+self.n))
        nx.draw(G, pos=positions, node_color=color_assignment_coordinate,  edge_color='black', node_size=1100, with_labels=True, labels=labels)
        plt.axis('equal')
        # plt.savefig(f"graphs/r{self.r}_n{self.n}_k{self.colors_used}.png")
        plt.savefig(f"graphs/r{self.r}.png")
        plt.clf()
        plt.close('all')

    def export_solution(self):
        import pandas as pd
        x_values_matrix = pd.DataFrame([ [x_vc.varValue for x_vc in x_v] for x_v in self.coloring_solution["x"]])
        x_values_matrix.to_csv(f"graphs/r{self.r}_x.csv", index=False, header=False)
        q_values_matrix = pd.DataFrame([ [q_vc.varValue for q_vc in q_v] for q_v in self.coloring_solution["q"]])
        q_values_matrix.to_csv(f"graphs/r{self.r}_q.csv", index=False, header=False)
        w_values_matrix = pd.DataFrame([ [w_vc.varValue for w_vc in self.coloring_solution["w"]]])
        w_values_matrix.to_csv(f"graphs/r{self.r}_w.csv", index=False, header=False)

K = 10
N = 3
R = 6


# Use a for loop
T_nm1_coloring_solution = None
for n in range(N, 40+1,2):
    T_n = T_Grid_Graph(n=n, r=R, k=K)
    T_n.define_graph()
    T_n.linear_programming_model(previous_variables=T_nm1_coloring_solution)
    T_n.coloring_assignment()
    T_n.graph_image()
    T_n.export_solution()
    T_nm1_coloring_solution = T_n.coloring_solution
