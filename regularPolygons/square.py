import numpy as np
import matplotlib.pyplot as plt
from dataStructure import Data

def buildToric(L : int) :
    NB_QUBITS = 2*L**2

    stabs_z = [] # Faces : (TOP, RIGHT,  BOTTOM, LEFT)
    stabs_x = [] # Vertices : (TOP, RIGHT,  BOTTOM, LEFT)
    qubits = np.zeros((NB_QUBITS,2), dtype=int) # Edges 

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

    data = Data(qubits, stabs_x, stabs_z)

    return data

def plotToric(L : int, DATA : Data):
    NB_QUBITS = len(DATA.qubits)

    # Draw lines
    for i in range (0,L):
        plt.axvline(x=i, color="black")
        plt.axvline(x=i + 1/2, linestyle=':', color="black")
        plt.axhline(y= (L-i)*2, color="black")
        plt.axhline(y= (L-i - 1/2)*2 , linestyle=':', color="black")

    stabsX, stabsZ = ([], []), ([], [])
    qubits_0m, qubits_0p = ([], []), ([], [])
    qubits_1m, qubits_1p = ([], []), ([], [])

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
        if not DATA.qubits[i][0] and not DATA.qubits[i][1]:
            qubits_0m[0].append(x)
            qubits_0m[1].append(y)
        elif not DATA.qubits[i][0] and DATA.qubits[i][1]:
            qubits_0p[0].append(x)
            qubits_0p[1].append(y)
        elif DATA.qubits[i][0] and not DATA.qubits[i][1]:
            qubits_1m[0].append(x)
            qubits_1m[1].append(y)
        else:
            qubits_1p[0].append(x)
            qubits_1p[1].append(y)

        #plt.text(x + 0.12, y - 0.27, str(i), horizontalalignment='center', verticalalignment='center', color="grey")
        plt.annotate(str(i), (x, y) , (x + 0.035, y - 0.15), color="grey")
    
    # Draw
    plt.scatter(stabsX[0], stabsX[1], marker='s', c ="black", label="Stab X", zorder=2)
    plt.scatter(stabsZ[0], stabsZ[1], marker="D", c ="black", label="Stab Z", zorder=2)

    plt.scatter(qubits_0m[0], qubits_0m[1], c = "blue", label = "Qubit [0,-]", zorder=2)
    plt.scatter(qubits_0p[0], qubits_0p[1], c = "orange", label = "Qubit [0,+]", zorder=2)
    plt.scatter(qubits_1m[0], qubits_1m[1], c = "purple", label = "Qubit [1,-]", zorder=2)
    plt.scatter(qubits_1p[0], qubits_1p[1], c = "red", label = "Qubit [1,+]", zorder=2)
