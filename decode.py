from dataStructure import Data
import numpy as np
import pymatching as pm

def applyNoise(data : Data, pBitFlip : float, pPhaseFlip : float):

    n = data.qubits.shape[0]
    pFlip = [pBitFlip, pPhaseFlip]

    # For the two error types
    for j in range(0,2):
        # For each qubit
        for i in range(0, n):
            # Apply independent error probability
            pError = pFlip[j]
           
            if(np.random.choice(np.arange(0, 2), p=[1 - pError, pError]) == 1):
                data.qubits[i][j]  = (0 if(data.qubits[i][j]) else 1)


def decode(Hx, Hz, syndromeX, syndromeZ):
    """
    Constructs a graph where stabilizers are vertices and edges are weighted by the distance
    (number of qubits) that it takes to go from one stabilizer to another
    """
    mX = pm.Matching.from_check_matrix(Hx)
    mZ = pm.Matching.from_check_matrix(Hz)

    """
    Apply Minimum Weigth Perfect Matching (Blossom V) algorithm, to find the shortest paths that 
    link two stabilizers with an odd number of qubits in error
    """
    estimatedErrorX = mX.decode(syndromeX) 
    estimatedErrorZ = mZ.decode(syndromeZ) 

    return (estimatedErrorX, estimatedErrorZ)
