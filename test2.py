
from RecursiveColoring import T_Grid_Graph
import pandas as pd

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

# print(build_experiment_table(r_min=2, r_max=6, n_min=1, n_max=10).to_latex(index=False))