import numpy as np
from dataStructure import Data

def buildTriangle(L : int):

    NB_QUBITS = 3*L**2

    stabs_z = [] # Faces : (TOP, BOTTOM, LEFT)
    stabs_x = [] # Vertices : (TOP, TOP-RIGHT, BOTTOM-RIGHT, BOTTOM, BOTTOM-LEFT, TOP-LEFT)
    qubits = np.zeros(NB_QUBITS, dtype=int) # Edges 

    data = Data(qubits, stabs_x, stabs_z)

    return data

def plotTriangle(L : int, data : Data):
    i=0
