import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
from dataStructure import Data
from regularPolygons.regularPolygons import buildData
from decode import applyNoise, decode
from matrix import generateHs, getLogicals, computeSyndrome
from subdivision import subdivide, buildCodeFromGeometry
from writeFile import writeFile

def plot(pLogical2D, pPhysical, l):
    fig, ax = plt.subplots(1)
    fig.suptitle("")

    for i in range(0, len(pLogical2D)):
    # plot the connected scatterplot
        ax.plot(pPhysical, pLogical2D[i][:], linestyle='-', marker='o',  label= str(l+i) )
    
    plt.legend()

    ax.yaxis.set_ticks(np.arange(0, 1.1, 0.1))

    # x axis label
    plt.xlabel("pPhysical")

    # y axis label
    plt.ylabel('pLogical')

    # show the graph
    plt.show()

    return pPhysical

def iterate(data, matrixes, pPhysical):

    # Retreive our matrices
    Hx, Hz, Lx, Lz =  matrixes

    # Apply noise
    applyNoise(data, pPhysical, pPhysical)

    # Compute syndrome
    syndromeX, syndromeZ = computeSyndrome(Hx, Hz, data)

    # Decode syndrome
    estErrX, estErrZ = decode(Hx, Hz, syndromeZ, syndromeX)
 
    # Verify if there is a logical error
    verifX = (Lx @ (data.qubits[:,0] + estErrX)) % 2
    verifZ = (Lz @ (data.qubits[:,1] + estErrZ)) % 2

    return int(np.any(verifX) or np.any(verifZ))

def buildCustom(subDivNumber):
    # Build a custom surface code

    '''
    codeS = [(-0.5,0.5), (0.5,0.5), (0.5,-0.5), (-0.5,-0.5), (-0.5,1.5), (0.5,1.5), (-1.5,-0.5), (-1.5,0.5), (-1.5,1.5)]
    codeA = [(0,1), (1,2), (2,3), (3,0), (0,4), (4,5), (5,1),(3,6),(6,7),(7,0),(7,8),(8,4),(5,8),(1,7),(2,6),(8,6),(4,3),(5,2)]
    codeF = [[0,1,2,3], [4,5,1,0], [1,7,6,2], [5,8,7,1], [8,4,0,7], [7,0,3,6], [6,3,4,8],[3,2,5,4]]
    centers = [(0,0), (0,1), (1,0), (1,1), (-1, 1),(-1,0),(-1,-1),(0,-1)]
    '''

    codeS = [(0,0) for i in range(30)]
    codeA = [(16, 20), (3, 4), (26, 27), (12, 16), (16, 17), (21, 22), (22, 23), (12, 28), (8, 9), (5, 16), (5, 19), (27, 28), (9, 20), (25, 26), (8, 24), (1, 12), (13, 14), (13, 17), (13, 26), (6, 14), (4, 5), (26, 29), (5, 6), (18, 25), (20, 25), (14, 18), (21, 27), (14, 15), (0, 1), (0, 7), (9, 10), (1, 2), (0, 4), (0, 10), (10, 11), (3, 24), (17, 23), (8, 17), (11, 22), (19, 29), (6, 7), (10, 29), (24, 28), (15, 19), (18, 24), (6, 22), (20, 21), (7, 27), (3, 23), (23, 29), (4, 25), (9, 15), (2, 3), (11, 12), (1, 13), (19, 28), (11, 18), (2, 15), (2, 21), (7, 8)]
    codeF = [[0,1,2,3,4],[0,4,5,6,7],[0,7,8,9,10],[10,11,12,1,0],[1,13,14,15,2],[15,9,20,21,2],[2,21,22,23,3],[3,24,18,25,4],[4,25,20,16,5],[25,26,27,21,20]]
    codeF += [[7,6,22,21,27],[7,27,28,24,8],[8,24,3,23,17],[9,8,17,16,20],[29,10,9,15,19],[26,29,19,28,27],[22,11,10,29,23],[6,14,18,11,22],[18,24,28,12,11],[28,19,5,16,12],[12,16,17,13,1],[17,23,29,26,13],[13,26,25,18,14],[14,6,5,19,15]]
    centers = [(0,0) for i in range(24)]
    code = (codeS,codeA,codeF,centers)

    geometry = subdivide(code, subDivNumber)
    data = buildCodeFromGeometry(geometry)

    return data

def main(args):

    # Collecting arguments
    L = args.L
    N = args.n
    R = 4
    S = 4
    PLOT = args.P
    VERBOSE = args.V
    l = args.l
    SUB_DIV_MAX = args.lm
    OUTPUT = args.o
    STEP = args.pStep
    P_MAX = args.pMax
    SUBDIVIDE = args.S

    if not l:
        l=0
        
    if not SUB_DIV_MAX:
        SUB_DIV_MAX = l

    # Stored values of Logical errors probabilities for each subdivision (and for each error probability)
    stored_pLogical = []
    
    # We go from l subdivisions to SUB_DIV_MAX subdivisions
    for subDivNumber in range(l, SUB_DIV_MAX + 1):

        # Build our datas 
        if not SUBDIVIDE:
            data = buildData(L, R, S)
        else: 
            data = buildCustom(subDivNumber)

        # Total number of physical qubits
        NB_QUBITS = len(data.qubits)
        
        # Generate parity matrices
        Hx, Hz = generateHs(data)

        # Generate logical operators
        Lx, Lz = getLogicals(Hx, Hz)

        pLogical = [ 0.0 ] # proba logical = 0 when proba physical = 0 | First iteration

        # We go from STEP to P_MAX error probability
        current_p = STEP
        while (current_p < 1 and current_p < P_MAX + STEP/2):
            nb_err = 0
            # We do N-1 iterations for the same error probability
            for i in range(1, N):

                # Deep copy of our data to apply noise independently for our simulation
                freshData = Data(np.zeros((NB_QUBITS,2), dtype=int), data.stabs_x, data.stabs_z)
                
                # Launch simulation
                nb_err += iterate(freshData, (Hx, Hz, Lx, Lz), current_p)

            if(VERBOSE):
                print("Result for p = ", current_p, " : ", float(nb_err) / N)

            current_p += STEP
            # Store the error mean for this error probability
            pLogical.append(float(nb_err) / N)

        # Store the results for this subdivision
        stored_pLogical.append(pLogical)
        
# Display graph and output file if needed

    pPhysical = np.arange(0, P_MAX + STEP, STEP)

    if(OUTPUT):
        for i in range(0, len(stored_pLogical)):
            # Output the results in Tikz format in the specified file (to import in Latex)
            writeFile(stored_pLogical[i], pPhysical, OUTPUT)

    if(PLOT):
        plot(stored_pLogical, pPhysical, l)
    

if __name__ == "__main__":
    # Check arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("L", help="Define the length of the toric surface code", type=int)
    parser.add_argument("n", help="Define the number of iteration per step", type=int)
    parser.add_argument("pStep", help="Define the analysis step of physical error probability", type=float)
    parser.add_argument("pMax", help="Define the limit of physical error probability", type=float)
    parser.add_argument("-S", help="Enable subdivision (otherwise square grid toric code of size L), requires -l", action='store_true')
    parser.add_argument("-l", help="Define the number of subdivision for each face (only matters if -S is specified), l is the minimum value if -lm is specified", type=int)
    parser.add_argument("-lm", help="Define the max subdivision number for each face (only matters if -S is specified)", type=int)
    parser.add_argument("-o", help="Save results in Latex format in the file specified.")
    parser.add_argument("-P", help="Enable plotting", action='store_true')
    parser.add_argument("-V", help="Enable verbose", action='store_true')
    args = parser.parse_args()

    if(args.L < 1):
        print("Length must be > 0")
        sys.exit(1)
    if(args.pStep <= 0 or args.pStep >= 1):
        print("Probability of a physical error must be in  ]0,1[")
        sys.exit(1)
    if(args.pMax <= args.pStep or args.pMax > 1):
        print("Probability of a physical error must be in  ]pStep,1[")
        sys.exit(1)
    if args.S and args.l is None:
        print("Specify required l value")
        sys.exit(1)
    if not args.S and (args.l or args.lm):
        print("-S not specified -l and -lm ignored.")
        sys.exit(1)

    # Go to main
    main(args)
