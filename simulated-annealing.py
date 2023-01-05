import numpy
import random
import math
import numpy as np
import copy
#parameters
piece_type = [1,2,3,4,5] #you can add pieces here 
piece_number = 4
T = 1000 #initial temp
coefficient = 0.98
total_systems = 14
iteration = 700 #coef 0.97 iteration 500 ceff 0.98 iteration 700 else throws an overflow error
sub_iteration = 5
cost_cons = 300 #constraints
weight_cons = 200
#piece data
pieces_data = {1:{'r':0.85,'c':10,'w':12}, #data for each piece
2:{'r':0.75,'c':5,'w':10},
3:{'r':0.95,'c':20,'w':18},
4:{'r':0.90,'c':15,'w':15},
5:{'r':0.99,'c':25,'w':20}}
#var
sol=[]
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
