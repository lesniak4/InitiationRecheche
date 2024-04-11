import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import copy
from math import *
        
def buildMesh(r, l):

    n = r
    
    angle = -2*pi/r
    S = [(cos(angle*i + 3*pi/r),sin(angle*i + 3*pi/r)) for i in range(r)]
    A = []
    F = []

    # Face originale
    for i in range(r):
        A.append([i, (i+1)%r])
    
    F.append([[i for i in range(r)]])

    # Si on veut garder les faces entières
    if l== 0:
        return S,A,F

    # Première division
    sCenter = n
    S.append((0,0))
    n += 1
    subF = F[0]
    # Division des arêtes
    for i in range(len(A)):
        
        # Sous-arête de droite
        A.append([n, A[i][1]])
        # Arête vers le centre
        A.append([n, sCenter])

        # Ajout du nouveau sommet
        S.append(((S[A[i][0]][0] + S[A[i][1]][0]) / 2, (S[A[i][0]][1] + S[A[i][1]][1]) / 2))

        # Sous-arête de gauche
        A[i] = [A[i][0], n]
        
        subF[0].insert(2*i+1, n)
        n += 1

    # Ajout des nouvelles faces
    for i in range(r):
        ind = 2*i
        subF.append([subF[0][ind-1], subF[0][ind], subF[0][ind+1], sCenter])

    subF.pop(0)

    F.pop(0)
    F = subF
    
    # Autres subdivisions
    prevF = copy.deepcopy(F)
    for i in range(len(A)):
        # Subdivision des arêtes principales
        for k in range(l-1):
            A[i].insert(k+1, n+k)
            S.append((S[A[i][0]][0] + (S[A[i][ len(A[i])-1 ]][0] - S[A[i][0]][0])*(k+1) / l, S[A[i][0]][1] + (S[A[i][ len(A[i])-1 ]][1] - S[A[i][0]][1])*(k+1) / l))

        # Subdivision des faces principales
        for j in range(len(F)):
            for k in range(len(F[j])):

                # Recherche des arêtes dans les faces division
                if F[j][k] == A[i][0] and F[j][(k+1)%len(F[j])] == A[i][l]:
                    for m in range(l-2, -1, -1):
                        F[j].insert(k+1, n+m)

                if F[j][k] == A[i][l] and F[j][(k+1)%len(F[j])] == A[i][0]:
                    for m in range(l-1):
                        F[j].insert(k+1, n+m)
                    
        n+=(l-1)

    newA = set()
    subF = []
    for i in range(len(F)):
        subA = []
        # Construction des arêtes intermédiaires
        for j in range(len(F[i])):
            if F[i][j] == sCenter:
                # Ajout de la première arête
                for a in A:
                    if (F[i][j-2*l] in a) and (F[i][j-l] in a): 
                        subA.append(a)
                # Construction et division des arêtes de la grille
                for k in range(l-1):

                    # Extrémité "gauche" de l'arête
                    s1 = F[i][j-2*l-(k+1)]

                    # Extrémité "droite"
                    s2 = F[i][j-((l-1)-k)]

                    a = [s1, s2]
                    # Division de l'arête
                    for m in range(l-1):
                        a.insert(1, n)
                        S.append((S[s1][0] + (S[s2][0] - S[s1][0])*(l-(m+1)) / l, S[s1][1] + (S[s2][1] - S[s1][1])*(l-(m+1)) / l))
                        n+=1
                    subA.append(a)
                # Ajout de la dernière arête
                for a in A:
                    if (F[i][j-3*l] in a) and (F[i][j] in a): 
                        subA.append(a)

        # Construction des faces à partir des arêtes divisées
        for j in range(len(subA)-1):
            for k in range(l):
                s1 = subA[j][k]
                s2 = subA[j][k+1]
                s3 = subA[j+1][k+1]
                s4 = subA[j+1][k]
                subF.append([s1, s2, s3, s4])

                # Reconstruction des arêtes (avec 2 sommets) à partir des nouvelles faces
                newA.add((s1, s2) if s1 < s2 else (s2, s1))
                newA.add((s2, s3) if s2 < s3 else (s3, s2))
                newA.add((s3, s4) if s3 < s4 else (s4, s3))
                newA.add((s4, s1) if s4 < s1 else (s1, s4))

    F = subF
    A = newA
     
    return S,A,F
   
def main(args):

    S,A,F = buildMesh(args.r, args.l)

    for a in A:
        plt.plot([S[a[0]][0], S[a[1]][0]], [S[a[0]][1], S[a[1]][1]], 'b-')

    for i in range(len(S)):
        plt.annotate(str(i), S[i] , (S[i][0], S[i][1]), color="grey")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("r", help="Define the number of edges on each face of the r-gones", type=int)
    parser.add_argument("l", help="Define the number of subdivisions of each face", type=int)
    args = parser.parse_args()
    R = args.r
    L = args.l
    if(R < 3):
        print("r must be >= 3")
        sys.exit(1)
    main(args)
