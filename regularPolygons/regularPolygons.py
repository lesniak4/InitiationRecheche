import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from dataStructure import Data

from regularPolygons.hexagon import buildHexa, plotHexa
from regularPolygons.triangle import buildTriangle, plotTriangle
from regularPolygons.square import buildToric, plotToric


def buildData(L : int, r : int, s : int):

    if(r == 4 and r == s):
        data = buildToric(L)
    elif(r == 6 and r == 3): # Not implemented yet
        data = buildHexa(L)
    elif(r == 3 and r == 6): # Not implemented yet
        data = buildTriangle(L)

    return data 

def plotData(L : int, r : int, s : int, data : Data):
    plt.figure(num="Toric code")

    axes = plt.gca()
    axes.xaxis.set_major_locator(ticker.NullLocator())
    axes.yaxis.set_major_locator(ticker.NullLocator())

    if(r == 4 and r == s):
        plt.title("L = " + str(L) + "\n{r,s} = " + "{" + str(r) + "," + str(s) + "}" + "\n[n,k,d] = ["+ str(2*L**2) + ",2," + str(L) +"]\n")
        plotToric(L, data)
    elif(r == 6 and r == 3): # Not implemented yet
        plotHexa(L, data)
    elif(r == 3 and r == 6): # Not implemented yet
        plotTriangle(L, data)

    plt.legend(bbox_to_anchor=(1.01, 0.5), loc="center left", borderaxespad=0)
    plt.subplots_adjust(right=0.8, top=0.8)
    plt.ion()
    plt.show()

def cleanPlot():
    plt.ioff()
    plt.cla()
    plt.close('all')