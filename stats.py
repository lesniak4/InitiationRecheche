import sys, argparse
import numpy as np
import copy
import matplotlib.pyplot as plt
from dataStructure import Data
from regularPolygons.regularPolygons import buildData
from decode import applyNoise, decode
from matrix import generateHs, getLogicals, computeSyndrome

def plot(results, step, max):
    fig, ax = plt.subplots(1)
    fig.suptitle("")

    pPhysical = np.arange(0, max + step, step)

    # plot the connected scatterplot
    ax.plot(pPhysical, results, linestyle='-', marker='o')

    ax.yaxis.set_ticks(np.arange(0, 1.1, 0.1))

    # x axis label
    plt.xlabel("pPhysical")

    # y axis label
    plt.ylabel('pLogical')

    # show the graph
    plt.show()

def iterate(data, matrixes, pPhysical):

    Hx, Hz, Lx, Lz =  matrixes

    applyNoise(data, pPhysical, pPhysical)

    syndromeX, syndromeZ = computeSyndrome(Hx, Hz, data)

    estErrX, estErrZ = decode(Hx, Hz, syndromeZ, syndromeX)
 
    verifX = (Lx @ (data.qubits[:,0] + estErrX)) % 2
    verifZ = (Lz @ (data.qubits[:,1] + estErrZ)) % 2

    return int(np.any(verifX) or np.any(verifZ))

def main(args):
    L = args.l
    R = args.r
    S = args.s
    N = args.n
    STEP = args.pStep
    P_MAX = args.pMax

    data = buildData(L, R, S)
    Hx, Hz = generateHs(L, data)
    Lx, Lz = getLogicals(Hx, Hz)

    results = [ 0.0 ] # proba logical = 0 when proba physical = 0
    current_p = STEP
    while (current_p < 1 and current_p < P_MAX + STEP/2):
        nb_err = 0
        for i in range(1, N):
            freshData = copy.deepcopy(data)
            nb_err += iterate(freshData, (Hx, Hz, Lx, Lz), current_p)
        current_p += STEP

        results.append(float(nb_err) / N)
    
    plot(results, STEP, P_MAX)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("l", help="Define the length of the toric surface code", type=int)
    parser.add_argument("r", help="Define the number of edges on each face of the r-gones", type=int)
    parser.add_argument("s", help="Define the number of r-gones on each vertex", type=int)
    parser.add_argument("n", help="Define the number of iteration per step", type=int)
    parser.add_argument("pStep", help="Define the analysis step of physical error probability", type=float)
    parser.add_argument("pMax", help="Define the limit of physical error probability", type=float)
    args = parser.parse_args()

    if(args.l < 1):
        print("Length must be > 0")
        sys.exit(1)
    if(args.r != 4 or args.s != args.r):
        print("R and S must be 4 for now")
        sys.exit(1)
    if(args.pStep < 0 or args.pStep > 1):
        print("Probability of a physical error must be in  [0,1]")
        sys.exit(1)
    if(args.pMax <= 0 or args.pMax > 1):
        print("Probability of a physical error must be in  [0,1]")
        sys.exit(1)

    main(args)
