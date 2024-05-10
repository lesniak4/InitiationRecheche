from dataStructure import Data
import numpy as np
import flinalg as fl

def generateHs(DATA : Data):
    NB_QUBITS = len(DATA.qubits)
    NB_STABS_X = len(DATA.stabs_x)
    NB_STABS_Z = len(DATA.stabs_z)
    
    Hx = np.zeros((NB_STABS_X,NB_QUBITS), dtype=int)
    Hz = np.zeros((NB_STABS_Z,NB_QUBITS), dtype=int)

    # Each line is representing a stabilizer, each column is a physical qubit
    # We put ones if the physical qubit is linked with the stabilizer otherwise 0
    for stabIndex in range (0, NB_STABS_X):
        for QubitIndex in DATA.stabs_x[stabIndex]:
            Hx[stabIndex][QubitIndex] = 1
    for stabIndex in range (0, NB_STABS_Z):   
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
    # each line represents a stabilizer, its value is 1 if it has an odd number of qubits that are in error
    syndromeZ = (Hx@data.qubits[:][:, 0]) % 2
    syndromeX = (Hz@data.qubits[:][:, 1]) % 2

    return (syndromeX, syndromeZ)