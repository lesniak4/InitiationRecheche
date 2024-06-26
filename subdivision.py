import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import copy
from math import *
from dataStructure import Data

def subdivide(code, l):

    S,A,F,centers = code
    n = len(S)

    if l==0:
        return S,A,F

    totS = copy.deepcopy(S)
    totA = set()
    totF = []
    oldF = []

    # Subdivision of each face of the code
    for p in range(len(F)):
        f = F[p]
        r = len(f)
        fS = copy.deepcopy(totS)
        fA = []
        for i in range(len(f)-1):
            fA.append((f[i], f[i+1]))
        fA.append((f[len(f)-1], f[0]))
        fF = [f]
        
        # First subdivision
        sCenter = n
        fS.append(centers[p])
        n += 1
        subF = [fF[0]]
        newS = []
        # Edges division
        for i in range(len(fA)):
            s = n
            for j in range(len(oldF)):
                # Verify if the edge is not already divided
                for k in range(len(oldF[j])):
                    if ((oldF[j][k] == fA[i][0]) and (oldF[j][(k+2*l)%len(oldF[j])] == fA[i][1])) or ((oldF[j][k] == fA[i][1]) and (oldF[j][(k+2*l)%len(oldF[j])] == fA[i][0])):
                        s = oldF[j][(k+l)%len(oldF[j])]

            # Right sub-edge
            fA.append([s, fA[i][1]])
            
            # Add the new vertice
            if s == n:
                fS.append(((fS[fA[i][0]][0] + fS[fA[i][1]][0]) / 2, (fS[fA[i][0]][1] + fS[fA[i][1]][1]) / 2))

            # Left sub-edge
            fA[i] = [fA[i][0], s]

            subF[0].insert(2*i+1, s)
            newS.append(s)

            if s == n:
                n+=1

        for s in newS:
            # Edge towards the center
            fA.append([s, sCenter])

        # Add new faces
        for i in range(r):
            ind = 2*i
            subF.append([subF[0][ind-1], subF[0][ind], subF[0][ind+1], sCenter])

        oldF.append(subF.pop(0))
        
        fF.pop(0)
        fF = subF

        # Other subdivisions
        prevF = copy.deepcopy(fF)
        for i in range(len(fA)):
            sd = [] # List of pre-existing vertices to insert
            for j in range(len(oldF)-1): # -1 because the last one is corresponding to the current face
                # Verify if the edge is not already divided
                for k in range(len(oldF[j])):
                    if (oldF[j][k] == fA[i][0]) and (oldF[j][(k+l)%len(oldF[j])] == fA[i][1]):
                         # Add the new vertices to the list
                        for d in range(1,l):
                            sd.append(oldF[j][(k+d)%len(oldF[j])])
                    if (oldF[j][k] == fA[i][1]) and (oldF[j][(k+l)%len(oldF[j])] == fA[i][0]):
                         # Add the new vertices to the list
                        for d in range(1,l):
                            sd.insert(0,oldF[j][(k+d)%len(oldF[j])])

            # Subdivision of main edges
            if len(sd) > 0:
                for k in range(len(sd)):
                    fA[i].insert(k+1, sd[k])
            else:
                for k in range(l-1):
                    fA[i].insert(k+1, n+k)
                    fS.append((fS[fA[i][0]][0] + (fS[fA[i][ len(fA[i])-1 ]][0] - fS[fA[i][0]][0])*(k+1) / l, fS[fA[i][0]][1] + (fS[fA[i][ len(fA[i])-1 ]][1] - fS[fA[i][0]][1])*(k+1) / l))

            # Subdivision of main edges
            for j in range(len(fF)):
                for k in range(len(fF[j])):

                    # Find edges in faces and divide
                    if fF[j][k] == fA[i][0] and fF[j][(k+1)%len(fF[j])] == fA[i][l]:
                        if len(sd) > 0:
                            for m in range(len(sd)):
                                fF[j].insert(k+1, sd[len(sd)-1-m])
                        else:
                            for m in range(l-2, -1, -1):
                                fF[j].insert(k+1, n+m)

                    if fF[j][k] == fA[i][l] and fF[j][(k+1)%len(fF[j])] == fA[i][0]:
                        if len(sd) > 0:
                            for m in range(len(sd)):
                                fF[j].insert(k+1, sd[m])
                        else:
                            for m in range(l-1):
                                fF[j].insert(k+1, n+m)

            # Update of the big face
            subOldF = copy.deepcopy(oldF[-1])
            for j in range(len(oldF[-1])):
                if oldF[-1][j] == fA[i][0] and oldF[-1][(j+1)%len(oldF[-1])] == fA[i][l]:
                    for d in range(1,l):
                        subOldF.insert(j+1, fA[i][l-d])
                if oldF[-1][j] == fA[i][l] and oldF[-1][(j+1)%len(oldF[-1])] == fA[i][0]:
                    for d in range(1,l):
                        subOldF.insert(j+1, fA[i][d])

            oldF[-1] = subOldF
            if len(sd) == 0:
                n+=(l-1)

        newA = set()
        subF = []

        for i in range(len(fF)):
            subA = []
            # Construction of intermediate edges
            for j in range(len(fF[i])):
                if fF[i][j] == sCenter:
                    # Adding the first edge
                    for a in fA:
                        if (fF[i][j-2*l] in a) and (fF[i][j-l] in a): 
                            subA.append(a)
                    # Edge construction and division of the grid
                    for k in range(l-1):

                        # Left extremity of the edge
                        s1 = fF[i][j-2*l-(k+1)]

                        # Right extremity of the edge
                        s2 = fF[i][j-((l-1)-k)]

                        a = [s1, s2]
                        # Edge division
                        for m in range(l-1):
                            a.insert(1, n)
                            fS.append((fS[s1][0] + (fS[s2][0] - fS[s1][0])*(l-(m+1)) / l, fS[s1][1] + (fS[s2][1] - fS[s1][1])*(l-(m+1)) / l))
                            n+=1
                        subA.append(a)
                    # Add the last edge
                    for a in fA:
                        if (fF[i][j-3*l] in a) and (fF[i][j] in a): 
                            subA.append(a)

            # Face construction from divided edges
            for j in range(len(subA)-1):
                for k in range(l):
                    s1 = subA[j][k]
                    s2 = subA[j][k+1]
                    s3 = subA[j+1][k+1]
                    s4 = subA[j+1][k]
                    subF.append([s1, s2, s3, s4])

                    # Reconstruction of edges (with 2 vertices) from new faces
                    newA.add((s1, s2) if s1 < s2 else (s2, s1))
                    newA.add((s2, s3) if s2 < s3 else (s3, s2))
                    newA.add((s3, s4) if s3 < s4 else (s4, s3))
                    newA.add((s4, s1) if s4 < s1 else (s1, s4))

        fF = subF
        fA = newA
        
        totS = fS
        totA = totA.union(fA)
        totF += fF

    return totS, list(totA), totF

def buildCodeFromGeometry(geometry):

    S,A,F = geometry

    qubits = np.zeros((len(A),2), dtype=int)
    stabs_z = [[] for f in F]
    stabs_x = [[] for s in S]

    # Stabilizers construction
    for i in range(len(A)):
        for j in range(len(F)):
            f = F[j]
            n = len(f)
            for k in range(n):
                if (A[i][0] == f[k] and A[i][1] == f[(k+1)%n]) or (A[i][1] == f[k] and A[i][0] == f[(k+1)%n]):
                    stabs_z[j].append(i)
        
        for s in range(len(S)):
            if s in A[i]:
                stabs_x[s].append(i)

    return Data(qubits, stabs_x, stabs_z)

def main(args):

    angle = -2*pi/6
    
    codeS = [(cos(angle*i + 3*pi/6),sin(angle*i + 3*pi/6)) for i in range(6)] + [(sqrt(3)*0.5+cos(angle*i + 5*pi/6),1.5+sin(angle*i + 5*pi/6)) for i in range(4)] + [(sqrt(3)+cos(angle*i + pi/6),sin(angle*i + pi/6)) for i in range(3)]
    codeS += [(sqrt(3)*0.5+cos(angle*i -pi/6),-1.5+sin(angle*i -pi/6)) for i in range(3)] + [(-sqrt(3)*0.5+cos(angle*i -3*pi/6),-1.5+sin(angle*i -3*pi/6)) for i in range(3)] + [(-sqrt(3)*0.5+cos(angle*i -5*pi/6),1.5+sin(angle*i -5*pi/6)) for i in range(3)]
    codeA = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,6), (6,7), (7,8), (8,9), (9,1), (9,10),(10,11),(11,12),(12,2),(12,13),(13,14),(14,15),(15,3),(15,16),(16,17),(17,18),(18,4), (5,19),(19,20),(20,21),(21,6)]
    codeF = [[0,1,2,3,4,5], [6,7,8,9,1,0],[9,10,11,12,2,1], [2,12,13,14,15,3],[4,3,15,16,17,18],[20,21,6,0,5,19]]
    centers = [(0,0), (sqrt(3)*0.5, 1.5), (sqrt(3), 0), (sqrt(3)*0.5, -1.5), (-sqrt(3)*0.5, -1.5), (-sqrt(3)*0.5, 1.5)]
    '''
    codeS = [(-0.5,0.5), (0.5,0.5), (0.5,-0.5), (-0.5,-0.5), (-0.5,1.5), (0.5,1.5), (1.5,0.5), (1.5,-0.5), (0.5,-1.5), (-0.5,-1.5), (-1.5,-0.5), (-1.5,0.5), (-1.5,1.5), (1.5,1.5), (1.5,-1.5), (-1.5,-1.5)]
    codeA = [(0,1), (1,2), (2,3), (3,0), (0,4), (4,5), (5,1), (1,6),(6,7),(7,2),(2,8),(8,9),(9,3),(3,10),(10,11),(11,0),(11,12),(12,4),(5,13),(6,13),(7,14),(14,8),(9,15),(15,10)]
    codeF = [[0,1,2,3], [4,5,1,0], [1,6,7,2], [3,2,8,9], [11,0,3,10], [12,4,0,11], [5,13,6,1],[2,7,14,8],[10,3,9,15]]
    centers = [(0,0), (0,1), (1,0), (0,-1), (-1, 0),(-1,1),(1,1),(1,-1),(-1,-1)]
    
    codeS = [(-0.5,0.5), (0.5,0.5), (0.5,-0.5), (-0.5,-0.5), (-0.5,1.5), (0.5,1.5), (-1.5,-0.5), (-1.5,0.5), (-1.5,1.5)]
    codeA = [(0,1), (1,2), (2,3), (3,0), (0,4), (4,5), (5,1),(3,6),(6,7),(7,0),(7,8),(8,4),(5,8),(1,7),(2,6),(8,6),(4,3),(5,2)]
    codeF = [[0,1,2,3], [4,5,1,0], [1,7,6,2], [5,8,7,1], [8,4,0,7], [7,0,3,6], [6,3,4,8],[3,2,5,4]]
    centers = [(0,0), (0,1), (1,0), (1,1), (-1, 1),(-1,0),(-1,-1),(0,-1)]
    '''
    code = (codeS,codeA,codeF,centers)
    S,A,F = subdivide(code, args.l)

    print("S ", len(S))
    print("A ", len(A))
    print("F ", len(F))

    for a in A:
        plt.plot([S[a[0]][0], S[a[1]][0]], [S[a[0]][1], S[a[1]][1]], 'b-')

    for i in range(len(S)):
        plt.annotate(str(i), S[i] , (S[i][0], S[i][1]), color="grey")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("r", help="Define the number of edges on each face of the r-gons", type=int)
    parser.add_argument("l", help="Define the number of subdivisions of each face", type=int)
    args = parser.parse_args()
    R = args.r
    L = args.l
    if(R < 3):
        print("r must be >= 3")
        sys.exit(1)
    main(args)
