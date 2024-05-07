import sys, argparse
import numpy as np

from dataStructure import Data
from regularPolygons.regularPolygons import buildData, plotData, cleanPlot
from decode import applyNoise, decode
from matrix import generateHs, getLogicals, computeSyndrome

def askErrors(L, R, S, data : Data, Hx, Hz):
    print("Type 'stop' anytime to finish") 

    while(1):
        plotData(L, R, S, data)
        response = ""

        stab = ""
        while(stab != "Z" and stab != "X"):
            response = input("Select a stabilizer type {X,Z} : ")
            stab = response
            if response == "stop":
                return
        
        id = -1
        while(id < 0 or id >= len(data.qubits)):
            try:
                response = input("Which physical qubit do you want to flip ? [0,"+ str(data.qubits.shape[0] - 1)+ "] : ")
                if response == "stop":
                    return
                id = int(response)
            except ValueError :
                id = -1

        if stab == "X":
            data.qubits[id][0] = (0 if(data.qubits[id][0]) else 1)
        else: 
            data.qubits[id][1] = (0 if(data.qubits[id][1]) else 1)


        syndromeX, syndromeZ = computeSyndrome(Hx, Hz, data)
        print("\n" + "Syndrome Z = " + str(syndromeX))
        print("Syndrome X = " + str(syndromeZ) + "\n")
        cleanPlot()
        
def main(args):
    L = args.l
    R = args.r
    S = args.s
    VERBOSE = args.v
    PLOTTING = args.p
    MANUAL = args.m

    # Setup our data
    data = buildData(L, R, S)

    Hx, Hz = generateHs(data)
    if VERBOSE :
        print("Hx = " + str(Hx) + "\n")
        print("Hz = " + str(Hz) + "\n")

    Lx, Lz = getLogicals(Hx, Hz)
    if VERBOSE :
        print("Lx = " + str(Lx))
        print("Lz = " + str(Lz) + "\n")

    pBitFlip = args.pBitFlip
    pPhaseFlip = args.pPhaseFlip

    if PLOTTING : 
        plotData(L, R, S, data)
        input("Press enter to apply noise")
        cleanPlot()
        print("\n") 

    # Apply errors to be corrected
    if MANUAL : 
        askErrors(L, R, S, data, Hx, Hz)
    else : 
        applyNoise(data, pBitFlip, pPhaseFlip)

    if VERBOSE :
        print("Qubits value : " + str(data.qubits[:,0]))
        print("Qubits phase : " + str(data.qubits[:,1]) + "\n")

    # Determine which stabilizers are affected
    syndromeX, syndromeZ = computeSyndrome(Hx, Hz, data)
    if VERBOSE :
        print("Syndrome X = " + str(syndromeX))
        print("Syndrome Z = " + str(syndromeZ) + "\n") 

    if PLOTTING : 
        plotData(L, R, S, data)
        input("Press enter to decode")
        cleanPlot()
        print("\n") 

    # Try decoding errors with PyMatching MWPM
    estErrX, estErrZ = decode(Hx, Hz, syndromeZ, syndromeX)
    if VERBOSE :
        print("Estimated error X (êx) = " + str(estErrX))
        print("Estimated error Z (êz) = " + str(estErrZ) + "\n") 

    # Check if there is any logical qubit error 
    verifX = (Lx @ (data.qubits[:,0] + estErrX)) % 2
    verifZ = (Lz @ (data.qubits[:,1] + estErrZ)) % 2
    if VERBOSE :
        print("Lx(ex + êx) = " + str(verifX))
        print("Lz(ez + êz) =  " + str(verifZ) + "\n") 

    if(np.any(verifX) or np.any(verifZ)):
        print("Failed to decode" + "\n")
    else: 
        print("Decoded successfully" + "\n")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("l", help="Define the length of the toric surface code", type=int)
    parser.add_argument("r", help="Define the number of edges on each face of the r-gones", type=int)
    parser.add_argument("s", help="Define the number of r-gones on each vertex", type=int)
    parser.add_argument("pBitFlip", help="Define the probability of a physical bitFlip [0,1]", type=float)
    parser.add_argument("pPhaseFlip", help="Define the probability of a physical phaseFlip [0,1]", type=float)
    parser.add_argument("-p", help="Enable plot printing", action='store_true')
    parser.add_argument("-v", help="Enable verbose", action='store_true')
    parser.add_argument("-m", help="Manual setup of qubits error (pBitFlip = pPhaseFlip = 0)", action='store_true')
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
