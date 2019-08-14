import numpy as np
import numexpr as ne
from shape_gen import shape_gen
from sympy import *
from pathos.multiprocessing import ProcessingPool as Pool
import dill


sol_raw = open('sol_v5.txt', 'r')
sol_str = sol_raw.read()
sol_str_list = sol_str.split('\n')
del sol_str_list[-1]
# print(sol_str_list[0])
sol_list = []
for i in sol_str_list:
    sol_list.append(i.split(','))
sol = []
for i in sol_list:
    local = []
    for j in i:
        local.append(float(j))
    sol.append(local)

#################################
###### Now the real stuff #######
#################################

height_raw = []
for row in sol:
    height_raw.append(row[6:26])
# print(height_raw[0])
height_prime = []
for row in sol:
    height_prime.append(row[26:46])

for row in height_raw:
    row.insert(10, 0.0)
for row in height_prime:
    row.insert(10, 0.0)

height = []
for i in range(len(height_raw)):
    local =  []
    for j in height_raw[i]:
        j += sol[i][5]
        local.append(j)
    height.append(local)
# print(height[1000])   Verified

x, L = symbols('x, L')
shape_fun_raw = shape_gen(4)
shape_func = []
for i in shape_fun_raw:
    shape_func.append(i.subs({L:1}))
# print(shape_fun)

def final_func_gen(i):
    local = []
    for j in range(len(height[i])-1):
        func = height[i][j] * shape_func[0] + height_prime[i][j] * shape_func[1] + height[i][j+1] * shape_func[2] + height_prime[i][j+1] * shape_func[3] 
        local.append(lambdify(x, func, 'numexpr'))
    print(f'generated {i+1}/{len(height)} row of functions')
    return local

p = Pool(8)
R = [i for i in range(len(height)-1)]
final_func = p.map(final_func_gen, R)

func_raw = open('func_plot.pkl','wb')
dill.dump(final_func, func_raw)

# final_func = []
# for i in R:
#     final_func.append(final_func_gen(i))

