import numpy as np
import flinalg as fl


def logicals(hmatx, hmatz):
    """Finds and returns logical operators
    from the import X and Z checks in hmatx and hmatz
    """
    uintmatx = np.array(hmatx, dtype='uint8')
    uintmatz = np.array(hmatz, dtype='uint8')
    kerx = fl.kernel(np.transpose(uintmatx))
    kerz = fl.kernel(np.transpose(uintmatz))
    logicalxspace, _ = fl.quotient_basis(kerz, uintmatx)
    logicalzspace, _ = fl.quotient_basis(kerx, uintmatz)
    return (np.array(logicalxspace), np.array(logicalzspace))


HX = [[1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
      [1,1,1,1,0,0,0,0,1,1,1,1,0,0,0],
      [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0],
      [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]]
HZ = [[1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
      [1,1,1,1,0,0,0,0,1,1,1,1,0,0,0],
      [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0],
      [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
      [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
      [1,1,0,0,1,1,0,0,0,0,0,0,0,0,0],
      [1,0,1,0,1,0,1,0,0,0,0,0,0,0,0],
      [1,1,0,0,0,0,0,0,1,1,0,0,0,0,0],
      [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0],
      [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0]]

LX, LZ = logicals(HX, HZ)
print(LX)
print(LZ)
