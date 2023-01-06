import numpy
import random
import math
import numpy as np
import copy
#parameters
piece_type = [1,2,3,4,5,6,7,8,9,10,11,12,13,14] #you can add pieces here 
piece_number = 4
T = 1000 #initial temp
coefficient = 0.98
total_systems = 4
iteration = 700 #coef 0.97 iteration 500 ceff 0.98 iteration 700 else throws an overflow error
sub_iteration = 30
cost_cons = 130 #constraints
weight_cons = 170
#piece data
pieces_data = {1:{'r':0.85,'c':18,'w':20}, #data for each piece
2:{'r':0.90,'c':23,'w':18},
3:{'r':0.90,'c':20,'w':21},
4:{'r':0.75,'c':13,'w':13},
5:{'r':0.80,'c':16,'w':16},
6:{'r':0.85,'c':17,'w':21},
7:{'r':0.95,'c':28,'w':23},
8:{'r':0.95,'c':26,'w':26},
9:{'r':0.95,'c':33,'w':18},
10:{'r':0.99,'c':38,'w':28},
11:{'r':0.99,'c':43,'w':26},
12:{'r':0.80,'c':18,'w':18},
13:{'r':0.85,'c':18,'w':19},
14:{'r':0.90,'c':18,'w':23}
}
#var
sol=[]
#weibull
lambda_w = [0.00532, 0.00818, 0.0133, 0.00741, 0.00619, 0.00436, 0.0105, 
0.015, 0.00268, 0.0141, 0.00394, 0.00236, 0.00215, 0.011]
k = [2, 3, 3 ,2 ,1 ,3 ,3 ,3 ,2 ,3 ,2 ,1 ,2 ,3]
c = [1, 2, 2, 3, 2, 3, 4, 3, 2, 4, 3, 2, 2, 4]
w = [3, 8, 7, 5, 4, 5, 7, 4, 8, 6, 5, 4, 5, 6]
x = np.arange(1,50.)/25.
def weib(x,n,a):
    return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)
#new solution creator
def create(solutionn):
    index = np.random.choice(np.arange(0,total_systems))
    number_changer = np.random.choice(np.arange(1,piece_number+1))
    type_changer = np.random.choice(piece_type)
    solutionn[index]['number'] =number_changer
    solutionn[index]['type'] = type_changer 
    return solutionn

#fitness
def fitness(solution):
    R_for_each = []
    cost = 0
    weight = 0
    for i in range(len(solution)):#reliability
        reliability= 1-((1-pieces_data[solution[i]['type']]['r'])**solution[i]['number'])
        R_for_each.append(reliability)
        cost+=pieces_data[solution[i]['type']]['c']*solution[i]['number'] #cost
        weight+=pieces_data[solution[i]['type']]['w']*solution[i]['number']   #weight

    R = np.prod(R_for_each)
    if cost>cost_cons:#penalty section (cost)
        cost_penalty = (cost - cost_cons)/cost
        R-= cost_penalty
    if weight>weight_cons:#penalty section (weight)
        weight_penalty = (weight - weight_cons) / weight
        R-=weight_penalty
    return R
#acceptance function
def accept(newsolution,solution,t):
    delta = (solution-newsolution)
    p = 1/(math.exp((delta)/t))
    print(f'P is {p}')
    return p

#initial solution
for i in range(total_systems):
      sol.append({'number':np.random.choice(np.arange(1,piece_number)),'type':np.random.choice(piece_type)})
best_sol = sol
for i in range(iteration):
    new_sol = []
    fitness_new = []
    T =T*coefficient
    new_sol.clear()
    fitness_new.clear()
    for j in range(sub_iteration): #search for new solution
        best_copied = copy.deepcopy(best_sol)
        new = create(best_copied)
        new_sol.append(new)
        fitness_new.append(fitness(new))
    new_best = max(fitness_new)
    # print(f'new {new_best} best{fitness(best_sol)} best_sol = {best_sol}')
    if new_best>=fitness(best_sol):
        best_sol = new_sol[fitness_new.index(new_best)]
    if new_best < fitness(best_sol):
        if random.random()<=accept(new_best,fitness(best_sol),T):
            best_sol = new_sol[fitness_new.index(new_best)]
    print(f'iteration {i} reliability is {fitness(best_sol)}best sol {best_sol} temp is {T}')