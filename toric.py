import sys, argparse
import numpy as np

from dataStructure import Data
from regularPolygons.regularPolygons import buildData, plotData, cleanPlot
from decode import applyNoise, decode


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

def askErrors(L, R, S, data : Data, Hx, Hz):
     while(1):
        plotData(L, R, S, data)

        stab = ""
        while(stab != "Z" and stab != "X"):
                stab = input("Select a stabilizer type {X,Z} : ")
        
        id = -1
        while(id < 0 or id >= len(data.qubits)):
            try:
                id = int(input("Which physical qubit do you want to flip ? [0,"+ str(data.qubits.shape[0] - 1)+ "] : "))
            except ValueError :
                id = -1

        if stab == "X":
            data.qubits[id][0] = (0 if(data.qubits[id][0]) else 1)
        else: 
            data.qubits[id][1] = (0 if(data.qubits[id][1]) else 1)

        print("Syndrome Z =")
        print((Hx@data.qubits[:][:, 0]) % 2)

        print("Syndrome X  =")
        print((Hz@data.qubits[:][:, 1]) % 2)
        
        cleanPlot()

def computeSyndrome(Hx, Hz, data: Data):
    syndromeZ = (Hx@data.qubits[:][:, 0]) % 2
    syndromeX = (Hz@data.qubits[:][:, 1]) % 2

    print("Syndrome Z = " + str(syndromeZ))
    print("Syndrome X  = " + str(syndromeX))

    return (syndromeX, syndromeZ)

        
def main(args):

    L = args.l
    R = args.r
    S = args.s

    pBitFlip = args.pBitFlip
    pPhaseFlip = args.pPhaseFlip

    data = buildData(L, R, S)
    applyNoise(data, pBitFlip, pPhaseFlip)

    plotData(L, R, S, data)
    input("Press enter to decode")
    cleanPlot()

    Hx, Hz = generateHs(L, data)
    print("Before Decoding : ")
    syndromeX, syndromeZ = computeSyndrome(Hx, Hz, data)

    decode(syndromeZ, syndromeX, data, R, S)

    print("\nAfter Decoding : ")
    syndromeX, syndromeZ = computeSyndrome(Hx, Hz, data)

    if(np.any(syndromeX) or np.any(syndromeZ)):
        print("Failed to decode")
    else: 
        print("Decoded successfully")

    plotData(L, R, S, data)
    input("Press enter to exit the program")
    cleanPlot()

    #askErrors(L, R, S, data, Hx, Hz)
    
   
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("l", help="Define the length of the toric surface code", type=int)
    parser.add_argument("r", help="Define the number of edges on each face of the r-gones", type=int)
    parser.add_argument("s", help="Define the number of r-gones on each vertex", type=int)
    parser.add_argument("pBitFlip", help="Define the probability of a physical bitFlip [0,1]", type=float)
    parser.add_argument("pPhaseFlip", help="Define the probability of a physical phaseFlip [0,1]", type=float)
    args = parser.parse_args()

    if(args.l < 1):
        print("Length must be > 0")
        sys.exit(1)
    if(args.r != 4 or args.s != args.r):
        print("R and S must be 4 for now")
        sys.exit(1)
    if(args.pBitFlip < 0 or args.pBitFlip > 1):
        print("Probability of a physical bitFlip must be in  [0,1]")
        sys.exit(1)
    if(args.pPhaseFlip < 0 or args.pPhaseFlip > 1):
        print("Probability of a physical phaseFlip must be in  [0,1]")
        sys.exit(1)

    main(args)
