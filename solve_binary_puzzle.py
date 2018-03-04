# Copyright 2017 Rick Shilling rick.shilling@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This code solves a puzzle somewhat similiar to Sudoko.
A binary puzzle is solved placing 0 & 1s on a grid.  Each row & column 
contains five 0s and five 1s.  The same number does not appear in more than 
two consecutive squares in any row or column.  Each row/column has a 
different sequence of 0s and 1s to any other row/column.  
"""

from ortools.constraint_solver import pywrapcp
from os import abort

# '2' is an uncovered variable, '1','0' are the initial conditions
grid = [
[2,2,2,2,2,2,2,1,2,2],
[1,2,2,1,1,2,2,0,2,2],
[2,2,2,2,1,2,2,2,0,2],
[2,2,2,2,2,2,2,0,2,2],
[2,2,1,1,2,2,2,2,0,2],
[2,0,2,2,2,2,2,2,0,2],
[2,2,2,2,2,2,2,2,2,1],
[2,2,2,2,2,1,2,0,0,2],
[1,1,2,2,2,2,1,2,2,2],
[2,2,1,1,2,2,2,2,2,2]]

solver = pywrapcp.Solver("binary_puzzle")

binary_digits = [i for i in range(2)]

bd = {}

for j in range(10):
    T = ''
    for i in range(10):
        string_variable = str(i)  + str(j)
        if grid[i][j] == 2:
            T = T + '-'
            bd[(i,j)] = solver.IntVar(binary_digits,string_variable)
        else:
            T = T + str(grid[i][j])
            bd[(i,j)] = solver.IntVar([grid[i][j]],string_variable)
    print(T)


for j in range(10):
    for i in range(7):
        solver.Add(solver.Max(bd[(i,j)]+bd[(i+1,j)]+bd[(i+2,j)]==1,bd[(i,j)]+bd[(i+1,j)]+bd[(i+2,j)]==2)==1)        
for j in range(7):
    for i in range(10):
        solver.Add(solver.Max(bd[(i,j)]+bd[(i,j+1)]+bd[(i,j+2)]==1,bd[(i,j)]+bd[(i,j+1)]+bd[(i,j+2)]==2)==1)
for i in range(10):
    solver.Add(bd[(i,0)]+bd[(i,1)]+bd[(i,2)]+bd[(i,3)]+bd[(i,4)]+bd[(i,5)]+bd[(i,6)]+bd[(i,7)]+bd[(i,8)]+bd[(i,9)]==5)
    solver.Add(bd[(0,i)]+bd[(1,i)]+bd[(2,i)]+bd[(3,i)]+bd[(4,i)]+bd[(5,i)]+bd[(6,i)]+bd[(7,i)]+bd[(8,i)]+bd[(9,i)]==5)

all_vars = [bd[(i, j)] for i in range(10) for j in range(10)]
  
vars_phase = solver.Phase(all_vars, solver.INT_VAR_SIMPLE, solver.INT_VALUE_SIMPLE)

solution = solver.Assignment()
solution.Add(all_vars)
collector = solver.FirstSolutionCollector(solution)
solver.Solve(vars_phase, [collector])

print(collector.SolutionCount())

if collector.SolutionCount() == 1:
    for i in range(10):
        print([int(collector.Value(0, bd[(i, j)])) for j in range(10)])
        