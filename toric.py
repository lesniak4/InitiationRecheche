import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

DATA = ([], [], []) # (qubits, stabs_x, stabs_z)
L = 0

def buildToric() :
    global DATA

    NB_QUBITS = 2*L**2

    stabs_z = [] # Faces : (TOP, RIGHT,  BOTTOM, LEFT)
    stabs_x = [] # Vertices : (TOP, RIGHT,  BOTTOM, LEFT)
    qubits = np.zeros(NB_QUBITS, dtype=int) # Edges 

    i=0
    while i < 2*L**2:
        
        if((i/L)%2 == 1): # We skip odd lines
            i += L
        else:

            # Assigning qubits to Z-Stabilizers
            exRight = ((i+1)%L == 0) # Right extremity
            exBot = (i+2*L >= NB_QUBITS)  # Bottom extremity

            if exBot and exRight: 
                stabs_z.append((i, i+1,  (i+2*L)%NB_QUBITS, i+L))
            elif exRight: 
                stabs_z.append((i, i+1, i+2*L, i+L ))
            elif exBot: 
                stabs_z.append((i, i+L+1, (i+2*L)%NB_QUBITS, i+L))
            else: 
                stabs_z.append((i, i+L+1, i+2*L, i+L ))

            # Assigning qubits to X-Stabilizers
            exLeft = (i%L == 0) # Left extremity
            exTop = (i-L < 0) # Top extremity

            if exLeft and exTop: 
                stabs_x.append((NB_QUBITS - L + i, i, i+L, i+L-1))
            elif exLeft: 
                stabs_x.append((i-L, i, i+L, i+L-1))
            elif exTop:
                stabs_x.append((NB_QUBITS - L + i, i, i+L, i-1))
            else: 
                stabs_x.append((i-L, i, i+L, i-1))

            i += 1

    DATA = (qubits, stabs_x, stabs_z)

def plotToric():
    NB_QUBITS = len(DATA[0])

    # Draw lines
    for i in range (0,L):
        plt.axvline(x=i, color="black")
        plt.axvline(x=i + 1/2, linestyle=':', color="black")
        plt.axhline(y= (L-i)*2, color="black")
        plt.axhline(y= (L-i - 1/2)*2 , linestyle=':', color="black")

    stabsX, stabsZ, qubits_0, qubits_1 = ([], []), ([], []), ([], []), ([], [])

    # Placing Stabilizers
    for i in range(0,L**2):
        stabsX[0].append(int(i%L))
        stabsX[1].append(((L - int(i/L))*2))

        stabsZ[0].append(int(i%L) + 1/2)
        stabsZ[1].append(((L - int(i/L))*2) - 1)

    # Placing Qubits
    for i in range(0,NB_QUBITS):
        x = (i%L) + (1/2 if (int(i/L))%2 == 0 else 0)
        y = (L - int(i/L)) + L
        if DATA[0][i]:
            qubits_1[0].append(x)
            qubits_1[1].append(y)
        else:
            qubits_0[0].append(x)
            qubits_0[1].append(y)

        #plt.text(x + 0.12, y - 0.27, str(i), horizontalalignment='center', verticalalignment='center', color="grey")
        plt.annotate(str(i), (x, y) , (x + 0.035, y - 0.15), color="grey")
    # Draw
    plt.scatter(stabsX[0], stabsX[1], marker='s', c ="black", label="Stab X", zorder=2)
    plt.scatter(stabsZ[0], stabsZ[1], marker="D", c ="green", label="Stab Z", zorder=2)
    plt.scatter(qubits_1[0], qubits_1[1], c = "red", label = "Qubit 1", zorder=2)
    plt.scatter(qubits_0[0], qubits_0[1], c = "blue", label = "Qubit 0", zorder=2)


def buildHexa():
    global DATA

    NB_QUBITS = 3*L**2

    stabs_z = [] # Faces : (TOP, TOP-RIGHT, BOTTOM-RIGHT, BOTTOM, BOTTOM-LEFT, TOP-LEFT)
    stabs_x = [] # Vertices : (TOP, RIGHT, LEFT)
    qubits = np.zeros(NB_QUBITS, dtype=int) # Edges 

    DATA = (qubits, stabs_x, stabs_z)

def plotHexa():
    i=0

def buildTriangle():
    global DATA

    NB_QUBITS = 3*L**2

    stabs_z = [] # Faces : (TOP, BOTTOM, LEFT)
    stabs_x = [] # Vertices : (TOP, TOP-RIGHT, BOTTOM-RIGHT, BOTTOM, BOTTOM-LEFT, TOP-LEFT)
    qubits = np.zeros(NB_QUBITS, dtype=int) # Edges 

    DATA = (qubits, stabs_x, stabs_z)

def plotTriangle():
    i=0


def buildData(r : int, s : int):
    if(r == 4 and r == s):
        buildToric()
    elif(r == 6 and r == 3):
        buildHexa()
    elif(r == 3 and r == 6):
        buildTriangle()

def plotData(r : int, s : int):
    plt.figure(num="Toric code")
    axes = plt.gca()
    axes.xaxis.set_major_locator(ticker.NullLocator())
    axes.yaxis.set_major_locator(ticker.NullLocator())

    if(r == 4 and r == s):
        plt.title("L = " + str(L) + "\n{r,s} = " + "{" + str(r) + "," + str(s) + "}" + "\n[n,k,d] = ["+ str(2*L**2) + ",2," + str(L) +"]\n")
        plotToric()
    elif(r == 6 and r == 3):
        plotHexa()
    elif(r == 3 and r == 6):
        plotTriangle()

    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
    plt.subplots_adjust(right=0.8, top=0.8)
    plt.ion()
    plt.show()
    
def generateHs():
    NB_QUBITS = len(DATA[0])

    Hx = np.zeros((L**2,NB_QUBITS), dtype=int)
    Hz = np.zeros((L**2,NB_QUBITS), dtype=int)

    for i in range (0, L**2):
        for index in DATA[1][i]:
            Hx[i][index] = DATA[0][index]

    for i in range (0, L**2):
        for index in DATA[2][i]:
            Hz[i][index] = DATA[0][index]
    return (Hx,Hz)
         
def cleanPlot():
        plt.ioff()
        plt.cla()
        plt.close('all')
        
def main(args):
    global DATA

    buildData(args.r, args.s)

    while(1):
        Hx, Hz = generateHs()
        print("(Hz@Hx.T).T = ")
        print((Hz@Hx.T).T)

        plotData(args.r, args.s)
        
        id = -1
        while(id < 0 or id >= len(DATA[0])):
            try:
                id = int(input("Which physical qubit do you want to flip ? [0,"+ str(len(DATA[0]) - 1)+ "] : "))
            except ValueError :
                id = -1
        
        DATA[0][id] = (0 if(DATA[0][id]) else 1)
        cleanPlot()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("l", help="Define the length of the toric surface code", type=int)
    parser.add_argument("r", help="Define the number of edges on each face of the r-gones", type=int)
    parser.add_argument("s", help="Define the number of r-gones on each vertex", type=int)
    args = parser.parse_args()
    L = args.l
    R = args.r
    S = args.s
    if(L < 1):
        print("Length must be > 0")
        sys.exit(1)
    if(R != 4 or S != R):
        print("R and S must be 4 for now")
        sys.exit(1)
    main(args)