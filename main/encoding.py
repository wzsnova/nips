#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 19:22:48 2019

@author: zahra
Submitted code for nips19
using groubi to solve milp


"""

#The encoding for the abstract neural network
from gurobipy import *
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
import time
import re

start_time_abstract1 = time.time()

def inputbounding(Input_param, data, G2_N_nodes):
    
    m = Model()
    x = {}
    for i in range(1,G2_N_nodes[0]+1):  
        x[i] = m.addVar(name = 'x_'+ str(i))  
    
    for i in range(len(Input_param[0])): 
        m.addConstr(-Input_param[1][i][0] + quicksum(Input_param[0][i][j] * x[j+1] for j in range(0, G2_N_nodes[0]))<= 0,'cstr0'+'_'+str(i+1))
    
    for i in range(1,data[0][0]+1):   
        m.addConstr(x[i]>=0, 'cstr1'+'_'+str(i)) 
    
    m.update()
    
    vars_max = []
    for i in range(1,data[0][0]+1): 
        m.setObjective(x[i], GRB.MAXIMIZE)
        m.optimize()
        vars_max.append(m.objVal) 
        
    vars_min = []
    for i in range(1,data[0][0]+1):     
        m.setObjective(x[i], GRB.MINIMIZE)
        m.optimize() 
        vars_min.append(m.objVal)  
    
    Input_bnds = vars_max + vars_min
    max_interval_input = 0
    for i in Input_bnds:
        if abs(i) > max_interval_input:
            max_interval_input = abs(i)
            
    m.write("debug0.lp"); 
    
    return max_interval_input, Input_bnds

#//////////////////////////////////////////////////////////////////////////////

#step 1. create an empty model
m = Model()

#step 2. add variables

#1a input variables
x = {}
for i in range(1,G2_N_nodes[0]+1):  
    x[i] = m.addVar(name = 'x_'+ str(i))  

#1b neurons variables
z = {}
t = {}
for l in range(1,len(G2_N_nodes)-1):
    for i in range(1, G2_N_nodes[l]+1):
        z[l,i] = m.addVar(name = 'z_'+ str(l) + '_'+ str(i))
        t[l,i] = m.addVar(vtype = GRB.BINARY, name = 't_'+ str(l) + '_'+ str(i))
        
#1c output variables
y = {}
l = len(G2_N_nodes)-1
for i in range(1,G2_N_nodes[-1]+1):  
    y[i] = m.addVar(name = 'y_'+ str(i))
    
#step 3. commit these changes to the model
m.update()
    
#print z
#print x   

#finding predecessors of each neurons for achieving corresponding weight of each neuron 
W_l_layers = []
W_u_layers = []
for l in range(1,len(G2_N_nodes)):   #I need all the weights of each layer except input layer (l=0) (len(G2_N_nodes)=4 start from 1, therefore we search through 1, 2, 3 layer)
    W_l_1layer = []
    W_u_1layer = []
    for i in range(1, G2_N_nodes[l]+1):
        w_l_1neuron = []
        w_u_1neuron = []
        for j in range(1, G2_N_nodes[l-1]+1):
            w_l_1neuron.append(G2.pred['C' + str(l) + ':' + str(i)]['C' + str(l-1) + ':' + str(j)]['C_weight'][0])
            w_u_1neuron.append(G2.pred['C' + str(l) + ':' + str(i)]['C' + str(l-1) + ':' + str(j)]['C_weight'][1])
        W_l_1layer.append(w_l_1neuron) 
        W_u_1layer.append(w_u_1neuron) 
    W_l_layers.append(W_l_1layer) 
    W_u_layers.append(W_u_1layer) 

#finding M, that is achieving by multiplynig ther infinity norm of each layer
# finding the norm of the whole weight upper bound matrix 
Norm_uppr_bnd = 1
for i in range(len(W_u_layers)):
    Norm_uppr_bnd *= LA.norm(W_u_layers[i], np.inf)
      
# finding the norm of the whole weight lower bound matrix (it is not important because we want the maximum amount of output)    
Norm_lowr_bnd = 1
for i in range(len(W_l_layers)):
    Norm_lowr_bnd *= LA.norm(W_l_layers[i], np.inf)
 
Max_norm_weight= max(abs(Norm_uppr_bnd), abs(Norm_lowr_bnd))
    
#step 5a. Add constraints for input layer 
for i in range(len(Input_param[0])): 
    m.addConstr(-Input_param[1][i][0] + quicksum(Input_param[0][i][j] * x[j+1] for j in range(0, G2_N_nodes[0]))<= 0,'cstr0'+'_'+str(i+1))

for i in range(1,data[0][0]+1):   
    m.addConstr(x[i]>=0, 'cstr1'+'_'+str(i)) 

m.update()
  
max_interval_input, Input_bnds = inputbounding(Input_param, data, G2_N_nodes)

M = max_interval_input * Max_norm_weight    
    
#step 5b. Add constraints for layer one
for i in range(1, G2_N_nodes[1]+1):  
    m.addConstr(z[1,i]- G2.nodes['C1:'+ str(i)]['bias'][0]-quicksum(W_l_layers[0][i-1][j]*x[j+1] for j in range(0, G2_N_nodes[0]))>=0, 'cstr1_'+str(1)+str(i))
    m.addConstr(z[1,i]- M*t[1,i]-G2.nodes['C1:'+ str(i)]['bias'][1]-quicksum(W_u_layers[0][i-1][j]*x[j+1]  for j in range(0, G2_N_nodes[0]))<=0, 'cstr2_'+str(1)+str(i))
    m.addConstr(z[1,i]>=0, 'cstr3_'+str(1)+str(i))
    m.addConstr(z[1,i]- M*(1-t[1,i])<=0, 'cstr4_'+str(1)+str(i))

#step 5c. Add constraints for other layers
for l in range(2, len(G2_N_nodes)-1):    
    for i in range(1, G2_N_nodes[l]+1):  
        m.addConstr(z[l,i]- G2.nodes['C'+str(l)+':'+ str(i)]['bias'][0]-quicksum(W_l_layers[l-1][i-1][j]* z[l-1,j+1]  for j in range(0, G2_N_nodes[l-1]))>=0, 'cstr1_'+str(l)+str(i))
        m.addConstr(z[l,i]- M*t[l,i]-G2.nodes['C'+str(l)+':'+ str(i)]['bias'][1]-quicksum(W_u_layers[l-1][i-1][j]*z[l-1,j+1]  for j in range(0, G2_N_nodes[l-1]))<=0, 'cstr2_'+str(l)+str(i))
        m.addConstr(z[l,i]>=0, 'cstr3_'+str(l)+str(i))
        m.addConstr(z[l,i]- M*(1-t[l,i])<=0, 'cstr4_'+str(l)+str(i))

#step 5d. Add constraints for last layer 
l = len(G2_N_nodes)-1      
for i in range(1, G2_N_nodes[l]+1):  
    m.addConstr(y[i]- G2.nodes['C'+str(l)+':'+ str(i)]['bias'][0]-quicksum(W_l_layers[l-1][i-1][j]* z[l-1,j+1]  for j in range(0, G2_N_nodes[l-1]))>=0, 'cstr1_'+str(l)+str(i))
    m.addConstr(y[i]- G2.nodes['C'+str(l)+':'+ str(i)]['bias'][1]-quicksum(W_u_layers[l-1][i-1][j]* z[l-1,j+1]  for j in range(0, G2_N_nodes[l-1]))<=0, 'cstr2_'+str(l)+str(i))

# commit these changes to the model
m.update()

#print("--- %s seconds ---" % (time.time() - start_time_abstract1))
Encoding_time_abstract = (time.time() - start_time_abstract1)

#step 4. set objective function
start_time_abstract2 = time.time()

output_max = []
s1=0
for i in range(2,data[0][-1]+1): 
    m.setObjective(y[i], GRB.MAXIMIZE)
    m.optimize() 
    s1+=m.Runtime    
    try:                         #step 6. solve model
        output_max.append(m.objVal) 
    except:
    # infeasible
        output_max.append('NC')
    
#print 'runtime is', m.Runtime  
s2=0 
output_min = []
for i in range(2,data[0][-1]+1): 
    m.setObjective(y[i], GRB.MINIMIZE)
    m.optimize()
    s2+=m.Runtime        
    try:                  #step 6. solve model
        output_min.append(m.objVal)
    except:
    # infeasible
        output_min.append('NC')
    
s3=s1+s2

Gurobi_time_abstract = (time.time() - start_time_abstract2)

outputs_range = []    
for i in range(0, data[0][-1]-1):
        output1_range = [output_min[i], output_max[i]]
        outputs_range.append(output1_range)
    
        
    
#print("--- %s seconds ---" % (time.time() - start_time_abstract2))
#Gurobi_time = (time.time() - start_time2)
#print 'runtime is', m.Runtime 
m.write("debug3.lp");
#m.write('model.sol')

