from dataStructure import Data
import numpy as np
import pymatching as pm

def applyNoise(data : Data, pBitFlip : float, pPhaseFlip : float):

    n = data.qubits.shape[0]
    pFlip = [pBitFlip, pPhaseFlip]

    for j in range(0,2):
        nbQubitsError = 0

        for i in range(0, n):
            pError = pFlip[j] * (pFlip[j]/1-pFlip[j])**nbQubitsError
            
            if(np.random.choice(np.arange(0, 2), p=[1 - pError, pError]) == 1):
                data.qubits[i][j]  = (0 if(data.qubits[i][j]) else 1)


def decode(Hx, Hz, syndromeX, syndromeZ):
    mX = pm.Matching.from_check_matrix(Hx)
    estimatedErrorX = mX.decode(syndromeX) 

    mZ = pm.Matching.from_check_matrix(Hz)
    estimatedErrorZ = mZ.decode(syndromeZ) 

    return (estimatedErrorX, estimatedErrorZ)
