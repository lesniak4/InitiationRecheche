from dataStructure import Data, constructGraphStabs
import networkx as nx
import numpy as np
import pymatching


def applyNoise(data : Data, pBitFlip : float, pPhaseFlip : float):

    n = data.qubits.shape[0]
    pFlip = [pBitFlip, pPhaseFlip]

    for j in range(0,2):
        nbQubitsError = 0

        for i in range(0, n):
            pError = pFlip[j] * (pFlip[j]/1-pFlip[j])**nbQubitsError
            
            if(np.random.choice(np.arange(0, 2), p=[1 - pError, pError]) == 1):
                data.qubits[i][j]  = (0 if(data.qubits[i][j]) else 1)

def decode(syndromeX, syndromeZ, data : Data, R : int, S : int):
    gX, gZ = constructGraphStabs(data, R, S)

    mX = pymatching.Matching.from_networkx(gX)
    matchingX = mX.decode_to_edges_array(syndromeX)

    mZ = pymatching.Matching.from_networkx(gZ)
    matchingZ = mZ.decode_to_edges_array(syndromeZ)
    
    applyCorrection(gX, gZ, data, matchingX, matchingZ)

def applyCorrection(gX : nx.Graph, gZ : nx.Graph, data : Data, matchingX, matchingZ):

    for edge in matchingX:
        qubitIndex = gX.get_edge_data(edge[0], edge[1])['qubit']
        data.qubits[qubitIndex] = (0 if(data.qubits[qubitIndex][0]) else 1)

    for edge in matchingZ:
        qubitIndex = gZ.get_edge_data(edge[0], edge[1])['qubit']
        data.qubits[qubitIndex] = (0 if(data.qubits[qubitIndex][1]) else 1)

