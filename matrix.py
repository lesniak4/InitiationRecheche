from dataStructure import Data
import numpy as np
import flinalg as fl

def generateHs(L, DATA : Data):
    NB_QUBITS = DATA.qubits.shape[0]

    Hx = np.zeros((L**2,NB_QUBITS), dtype=int)
    Hz = np.zeros((L**2,NB_QUBITS), dtype=int)

    for stabIndex in range (0, L*L):
        for QubitIndex in DATA.stabs_x[stabIndex]:
            Hx[stabIndex][QubitIndex] = 1
        for QubitIndex in DATA.stabs_z[stabIndex]:
            Hz[stabIndex][QubitIndex] = 1

    return (Hx,Hz)

def getLogicals(Hx, Hz):
    """Finds and returns logical operators
    from the import X and Z checks in Hx and Hz
    """
    uintmatx = np.array(Hx, dtype='uint8')
    uintmatz = np.array(Hz, dtype='uint8')
    kerx = fl.kernel(np.transpose(uintmatx))
    kerz = fl.kernel(np.transpose(uintmatz))
    logicalxspace, _ = fl.quotient_basis(kerz, uintmatx)
    logicalzspace, _ = fl.quotient_basis(kerx, uintmatz)
    
    return (np.array(logicalxspace), np.array(logicalzspace))

def computeSyndrome(Hx, Hz, data: Data):
    syndromeZ = (Hx@data.qubits[:][:, 0]) % 2
    syndromeX = (Hz@data.qubits[:][:, 1]) % 2

    return (syndromeX, syndromeZ)