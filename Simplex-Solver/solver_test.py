from LPsolver import LPSolver
import numpy as np


## test:
a = np.array([[1,0,1,0,0],
              [0,2,0,1,0],
              [1,1,0,0,1]])
b = np.array([100,200,150]).reshape(-1, 1)
c = np.array([-1, -2, 0, 0, 0]).reshape(-1, 1)
solver = LPSolver(a, b, c)
solver.solve(verbose=True)


a = np.array([[1,2,3,0],
              [0,-4,-9,0],
              [0,0,3,1]])
b = np.array([3,-5,1]).reshape(-1, 1)
c = np.array([1,1,1,0]).reshape(-1, 1)

solver = LPSolver(a, b, c)
solver.solve(verbose=True)

a = np.array([[-2, -9, 1, 9, 1, 0],
              [1/3, 1, -1/3, -2, 0, 1]])
b = np.array([0,0]).reshape(-1, 1)
c = np.array([-2,-3,1,12,0,0]).reshape(-1, 1)

solver = LPSolver(a, b, c)
solver.solve()


a = np.array([[1,3,0,4,1],
              [1,2,0,-3,1],
              [-1,-4,3,0,0]])
b = np.array([2, 2, 1]).reshape(-1, 1)
c = np.array([2, 3, 3, 1, -2]).reshape(-1, 1)

solver = LPSolver(a, b, c)
solver.solve()



a = np.array([[1,3,0,1,1,0,0],
              [2,1,0,0,0,1,0],
              [0,1,4,1,0,0,1]])
b = np.array([4,3,3]).reshape(-1, 1)
c = np.array([-2,-4-9/4+0.0005,-1,-1,0,0,0]).reshape(-1, 1)

solver = LPSolver(a, b, c)
# solver.solve(verbose=True)
solver.solve()


a = np.array([[1,1,1,0,0],
              [0,0,-1,1,0],
              [1,0,2,-1,1]])
b = np.array([1,5,0]).reshape(-1, 1)
c = np.array([0,1,-0.5,1,0]).reshape(-1, 1)

solver = LPSolver(a, b, c)
solver.solve(verbose=True)



a = np.array([[2,1,1,1,0,0],
              [3,1,2,0,1,0],
              [1,2,4,0,0,1]])
b = np.array([240,150,180]).reshape(-1, 1)
c = np.array([-500,-250,-600,0,0,0]).reshape(-1, 1)

solver = LPSolver(a, b, c)
solver.solve(verbose=True)
solver.cp_solve()
exit()

