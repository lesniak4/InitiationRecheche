import sys, argparse
import numpy as np

from dataStructure import Data
from regularPolygons.regularPolygons import buildData, plotData, cleanPlot
from decode import applyNoise, decode
from matrix import generateHs, getLogicals, computeSyndrome

def askErrors(L, R, S, data : Data, Hx, Hz):
    """
    Function to add manual errors to the qubits 
    """


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

    # Collecting arguments

    L = args.L
    R = 4
    S = 4
    VERBOSE = args.V
    PLOTTING = args.P
    MANUAL = args.M

    pBitFlip = args.pErrorX
    pPhaseFlip = args.pErrorZ

    # Setup our data
    data = buildData(L, R, S)

    # Generate parity matrices
    Hx, Hz = generateHs(data)
    if VERBOSE :
        print("Hx = " + str(Hx) + "\n")
        print("Hz = " + str(Hz) + "\n")

    # Generate logical operators
    Lx, Lz = getLogicals(Hx, Hz)
    if VERBOSE :
        print("Lx = " + str(Lx))
        print("Lz = " + str(Lz) + "\n")

    if PLOTTING : 
        plotData(L, R, S, data)
        input("Press enter to apply noise")
        cleanPlot()
        print("\n") 

    # Apply noise
    if MANUAL : 
        askErrors(L, R, S, data, Hx, Hz)
    else : 
        applyNoise(data, pBitFlip, pPhaseFlip)

    if VERBOSE :
        print("Qubits value : " + str(data.qubits[:,0]))
        print("Qubits phase : " + str(data.qubits[:,1]) + "\n")

    # Determine which stabilizers are affected by computing syndrome for each type of error
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
    # Check arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("L", help="Define the length of the toric surface code", type=int)
    parser.add_argument("pErrorX", help="Define the probability of a physical error X [0,1]", type=float)
    parser.add_argument("pErrorZ", help="Define the probability of a physical error Z [0,1]", type=float)
    parser.add_argument("-P", help="Enable plot printing", action='store_true')
    parser.add_argument("-V", help="Enable verbose", action='store_true')
    parser.add_argument("-M", help="Manual setup of qubits error (pBitFlip = pPhaseFlip = 0)", action='store_true')
    args = parser.parse_args()

    if(args.L < 1):
        print("Length must be > 0")
        sys.exit(1)
    if(args.pErrorX < 0 or args.pErrorX > 1):
        print("Probability of a physical error X must be in  [0,1]")
        sys.exit(1)
    if(args.pErrorZ < 0 or args.pErrorZ > 1):
        print("Probability of a physical error Z must be in  [0,1]")
        sys.exit(1)

    # Go to main
    main(args)
