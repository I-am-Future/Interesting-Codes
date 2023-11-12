import numpy as np
import warnings
import terminaltables
import cvxpy as cp

class LPSolver():
    ''' Class that record and solve a LP problem with 2-phases simplex tableau. '''
    def __init__(self, A: np.ndarray, b: np.ndarray, c: np.ndarray, target: str='min') -> None:
        ''' Constructor method of the Linear Programming Solver Class. 

            Note that the problem should be in the canonical form. E.g., 

            min c^T x

            s.t. Ax = b
                 x >= 0

            @param A: The coefficient matrix of the constraints.
            @param b: The right hand side of the constraints.
            @param c: The coefficient vector of the objective function.
            @param target: The target of the objective function, `min` or `max`.
        '''
        self.A = A
        self.b = b.reshape(-1, 1)
        self.c = c.reshape(-1, 1)
        self._m = A.shape[0]
        self._n = A.shape[1]
        assert b.shape[0] == self._m, "b's dimension should be equal to A's col number!"
        assert c.shape[0] == self._n, "c's dimension should be equal to A's row number!"
        self._status = 1  # 1: finite solved, 2: unbounded, 3: infeasible
        self.target = target
        if target == 'max':
            self.c = -self.c
        elif target == 'min':
            pass  # do nothing
        else: 
            raise Exception('Wrong target flag! Only `max` or `min` accepted!')

    def cp_solve(self):
        ''' An helper function to solve this LP problem using cvxpy. 
        
            Just call this function to solve the problem.

            You can use this function to check the correctness of our simplex implementation.
        '''
        print('-'*15, 'cvxpy LP problem solving started! ', '-'*15)

        x = cp.Variable(self._n)
        objective = cp.Minimize(cp.matmul(self.c.T, x))
        constraints = [cp.matmul(self.A, x) == self.b.reshape(-1), x >= 0]
        prob = cp.Problem(objective, constraints)
        prob.solve()
        print("[Status] : Status:", prob.status)
        print("[Status] : Optimal value", prob.value)
        print("[Status] : Optimal var", x.value.tolist())

        print('-'*15, 'cvxpy LP problem solving finished! ', '-'*15)

    def __inter_log(self, *msg, table):
        ''' Utility function, print the message and status if verbose is True. '''
        if self.verbose:
            print(*msg)

            # print the basis and table is a more readable way
            # round the data to 2 digits
            table = np.round(table, 2)

            data = table.tolist()
            data.insert(0, ['Basis'] + [f'x{i+1}' for i in range(table.shape[1]-1)] + ['b'])
            data[1].insert(0, '')
            for i in range(len(self.basis)):
                data[i+2].insert(0, f'{self.basis[i]+1}')

            table = terminaltables.AsciiTable(data)
            table.inner_heading_row_border = False
            table.inner_row_border = False
            table.inner_column_border = False
            print(table.table)

    def solve(self, verbose: bool = False):
        ''' call this function to solve the problem. 
            @param verbose: 
        '''
        print('>'*15, 'Solving LP problem started! ', '>'*15)
        self.verbose = verbose
        self.basis = []
        # for i in range(self._n+1, self._n+self._m+1):
        for i in range(self._n, self._n+self._m):
            self.basis.append(i)

        p1_table = self.__phase1()

        if self._status == 1:
            sol, optval = self.__phase2(p1_table)

        if self._status == 1:
            print('[Status] : The program solved successfully!')
            print('[Status] : optimal solution:', sol)
            if self.target == 'max':
                optval = -optval
            print('[Status] : optimal value:', optval)
        elif self._status == 2:
            print('[Status] : The program is unbounded!')
        elif self._status == 3:
            print('[Status] : The program is infeasible!')
        print('<'*15, 'Solving LP problem finished!', '<'*15)

    def __phase1(self):
        ''' solve (phase 1 part) '''
        # build the tableau for phase 1
        ''' T11 | T12 | T13
            T21 | T22 | T23
        '''
        T11 = np.zeros((1, self._n)) - np.ones((1, self._m)) @ self.A
        T12 = np.ones((1, self._m))
        T13 = np.array([[-np.sum(self.b)]])
        T21 = self.A.copy()
        T22 = np.identity(self._m)
        T23 = self.b.copy()
        table = np.hstack((np.vstack((T11, T21)), np.vstack((T12, T22)), np.vstack((T13, T23))))

        self.__inter_log('[INFO] : Phase 1 started!', table=table)

        # call the core() for computing
        self.__core(table, 1)
        if np.abs(table[0, -1]) >= 1e-10:
            self._status = 3
            if self.verbose:
                warnings.warn('The original problem is not solvable!')
        if self.verbose:
            print('[Status] : Phase 1 completed!')
        return table

    def __phase2(self, oldtable):
        ''' solve (phase 2 part) '''
        ''' T11 | T12 
            T21 | T22 
        '''
        # build the tableau for phase 2
        T11 = self.c.transpose() - self.c[self.basis].T @ np.linalg.inv(self.A[:, self.basis]) @ self.A
        T21 = oldtable[1:, 0:self._n]
        T22 = oldtable[1:, -1].reshape(-1, 1)
        T12 = -(self.c[self.basis].transpose() @ T22).reshape(1, 1)
        table = np.hstack((np.vstack((T11, T21)), np.vstack((T12, T22))))

        self.__inter_log('[INFO] : Phase 2 started!', table=table)

        self.__core(table, 2)
        sol = np.zeros(self._n)
        for i in range(self._m):
            sol[self.basis[i]] = table[i+1, -1]
        optval = -table[0, -1]
        return (sol, optval)

    def __core(self, table: np.ndarray, mode: int):
        ''' Core of the solver. Iterate the procedure to solve the problem. 
            @param table: 
            @param mode: 
        '''
        step = 0
        while (table[0, 0:-1] < 0).any():  # there are col reduced cost < 0
            # find pivot col
            for i in range(len(table[0, 0:-1])):
                if table[0, i] < 0:  # reduced cost < 0
                    pivot_col = i
                    break
            # find pivot row
            pivot_row = -1
            min_quotient = float('inf')
            for i in range(self._m):
                if table[i+1, pivot_col] > 0:
                    if table[i+1, -1] / table[i+1, pivot_col] < min_quotient:
                        pivot_row = i+1
                        min_quotient = table[i+1, -1] / table[i+1, pivot_col]
            if pivot_row == -1:
                self._status = 2
                if self.verbose:
                    warnings.warn('The original problem is not solvable!')
                break
            # update table
            self.__update_tableau(table, pivot_row, pivot_col)
            self.basis[pivot_row-1] = pivot_col
            step += 1
            self.__inter_log(f'\nStep {step} of phase {mode}', table=table)
        # clear self.basis in y cols
        if mode == 1:
            for j in range(len(self.basis)):
                if self.basis[j] > self._n:  # b is at y cols
                    for i in range(self._n):
                        if i not in self.basis:
                            self.__update_tableau(table, j+1, i)
                            self.basis[j] = i
                            self.__inter_log('', table=table)
                            break
                            
        
    def __update_tableau(self, table: np.ndarray, pivot_row: int, pivot_col: int):
        ''' Utility function, update the tableau. 
            1. pivot row normalize to 1
            2. other row updates to 0
            @param table: 
            @param pivot_row: 
            @param pivot_col: 
        '''
        table[pivot_row, :] = table[pivot_row, :] / table[pivot_row, pivot_col]
        for i in range(table.shape[0]):
            if i == pivot_row:
                continue
            table[i, :] = table[i, :] + table[pivot_row, :] * (-table[i, pivot_col])

