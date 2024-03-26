import numpy as np
from dataStructure import Data

def buildHexa(L : int):

    NB_QUBITS = 3*L**2

    stabs_z = [] # Faces : (TOP, TOP-RIGHT, BOTTOM-RIGHT, BOTTOM, BOTTOM-LEFT, TOP-LEFT)
    stabs_x = [] # Vertices : (TOP, RIGHT, LEFT)
    qubits = np.zeros(NB_QUBITS, dtype=int) # Edges 

    data = Data(qubits, stabs_x, stabs_z)

    return data

def plotHexa(L, data):
    i=0