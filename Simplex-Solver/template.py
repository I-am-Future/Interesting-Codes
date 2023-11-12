import numpy as np
from LPsolver import LPSolver

# min c^T x
# s.t. Ax = b
#      x >= 0

a = np.array([[2,1,1,1,0,0],
              [3,1,2,0,1,0],
              [1,2,4,0,0,1]])

b = np.array([240,150,180])

c = np.array([-500,-250,-600,0,0,0])

solver = LPSolver(a, b, c)

solver.solve(verbose=True)

solver.cp_solve()