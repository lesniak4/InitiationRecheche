from dataclasses import dataclass
import networkx as nx

@dataclass
class Data:
    qubits: list
    stabs_x: list
    stabs_z: list 

def constructGraphStabs(data: Data, R : int, S : int):
    gX = graphStabsX(data, S)
    gZ = graphStabsZ(data, R)
    
    return (gX, gZ)

def graphStabsX(data: Data, S : int):
    G = nx.Graph()

    for i in range(0,len(data.stabs_x)):
        G.add_node(i)

    for i in range(0, len(data.stabs_x)):
        for j in range(i + 1, len(data.stabs_x)):
            for k in range(0, S):
                for l in range(0, S):
                    if data.stabs_x[i][k] == data.stabs_x[j][l]:
                        G.add_edge(i, j, qubit = data.stabs_x[i][k])
        
    return G

def graphStabsZ(data: Data,  R : int):
    G = nx.Graph()

    for i in range(0,len(data.stabs_z)):
        G.add_node(i)

    for i in range(0, len(data.stabs_z)):
        for j in range(i + 1,len(data.stabs_z)):
            for k in range(0, R):
                for l in range(0, R):
                    if data.stabs_z[i][k] == data.stabs_z[j][l]:
                        G.add_edge(i, j, qubit = data.stabs_z[i][k] )
        
    return G
