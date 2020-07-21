#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Using repo
Created on Sun Feb  3 21:37:17 2019

@author: zahra
Submitted code for nips19

abstraction nn code
just execute this file, automatically encoding.py would be run

"""

# complete version
import sys
import os
import csv
import decimal 
import networkx as nx
import matplotlib.pyplot as plt
import time

def gen_exception(funname):
	"""
	input: funname: function name in which error has occurred
	"""
	try:
		exception_type, exception_obj, exception_tb = sys.exc_info()
		fname = exception_tb.tb_frame.f_code.co_filename
		disp = "Error in the function "+ str(funname)+" at line " + str(exception_tb.tb_lineno)
		print disp
	except:
		print "Error in the function gen_exception"

################################################# reading the neural network's information from the text file

def read_file (file_directory):
    
    with open(file_directory, 'rb') as f:
        reader = csv.reader(f)
        data_str = list(reader)
        
        data = []                                            ### converting string data to a integer list format in this section
        sub_lst = []
        for j in data_str[0]:
            sub_lst_elment = int(j)
            sub_lst.append(sub_lst_elment)
        data.append(sub_lst)
            
        for i in data_str[1:]:
            sub_lst = []
            for j in i:
                sub_lst_elment = float(j)
                sub_lst.append(sub_lst_elment)
            data.append(sub_lst)
    return data

################################################# creating nodes of a graph using Networkx  

def graph_nodes (data):
    try:
        G1 = nx.DiGraph()
        N_vertices = 0
        for s in range(len(data[0])):
            N_vertices += int(data[0][s])                    ### N_vertices: number of neurons (nodes) in a neural network (graph)  
        bias_pointr = N_vertices-data[0][-1]+1               ### bias_pointr: biases are started from this row of the data because except first row, we have all outgoing weights corresponding to all neurons except output (there is no outgoing weights for output neurons) neurons 
        for l in range(len(data[0])):                        ### l: number of layers which starts from 0
            for j in range (1,data[0][l]+1):                 ### j: number of neurons in each layer which starts from 1
                if l == 0:
                    G1.add_node('L'+str(l)+':'+str(j))       ### The format for first node in layer 0 will be L0:1  
                else:
                    G1.add_node('L'+str(l)+':'+str(j), bias = [data[bias_pointr][0], data[bias_pointr][1]])      #print G1.nodes['L3:1']['bias'][0]      #x = G1.nodes['L3:1'] 
                    bias_pointr += 1                         ### bias: interval bias for each neuron which is defined as an attitude of graph's node 
        return N_vertices, bias_pointr, G1
    except:
        gen_exception("graphnodes")

################################################# creating edges of a graph using Networkx

def graph_edges (G1, data):
        lc = 1                                           
        for l in range (0, len(data[0])-1):                  ### for adding edges between 2 layers, I need the layer number, but the point is I do not consider the output number because arbitrarily it is considered by l+1   
            for k in range (data[0][l]):                     ### k for reaching layer l 
                for z in range (data[0][l+1]):               ### z for reaching layer l+1 
                    G1.add_edge('L'+str(l)+':'+str(k+1),'L'+str(l+1)+':'+str(z+1), Rweight = [data[lc][z*2], data[lc][z*2+1]])  ### print (G1.edges['L0:1','L1:1']['Rweight'])
                lc += 1                                                                                                         ### I used k+1 instead of k, and z+1 instead of z to start number of nodes from 1 not 0 (L0:1 not L0:0)   
##      print (G1.edges['L1:1','L2:1']['Rweight'])
        return  G1

################################################# printing graph using Networkx functions

def graph_print (G1, color):
        
        pos = nx.spring_layout(G1)
        nx.draw_networkx_nodes(G1, pos, cmap = plt.get_cmap('jet'),
                               node_color = color , node_size = 500)
        nx.draw_networkx_edges(G1, pos, edgelist = G1.edges, arrows = True)
        nx.draw_networkx_labels(G1, pos)
        #nx.draw_networkx_edges(G1, pos, edgelist=red_edges, edge_color='r', arrows=True)
        #nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
        #nx.draw_networkx_edge_labels(G1,pos,edge_labels=G1)
        plt.show()
        
        return

################################################# reading the node combination information from the text file

def read_node_combination_file (file_path):
        
        f = open(file_path, "r")
        data_str = f.read()
        data_lst_str = data_str.strip("\n").split("\n")

        N_combin_str = []                                    ### converting string data to a integer list format in this section 
        for i in data_lst_str:
            N_combin_str.append(i.split(';'))
            
        N_combin = []    
        for k in N_combin_str:
            N_combin_each_layer = []
            for j in k:
                N_combin_each_node = []
                for i in j.split(','):
                    N_combin_each_node.append(int(i))
                N_combin_each_layer.append(N_combin_each_node)
            N_combin.append(N_combin_each_layer)   

        return N_combin

################################################# creating nodes of an abstraction graph using Networkx 

def abstraction_graph_nodes (G1, N_combin, data):
    G2 = nx.DiGraph()
    # assigning input nodes seperately because there is no bias for input layer
    for i in range(1,data[0][0]+1):                      ### there is no combination for input nodes, so all input nodes are in abstraction graph 
        G2.add_node('C'+str(0)+':'+str(i))               ### because I wanted to have this format for combination nodes C0:1 therefore the range starts 1 instead of 0, and add 1 to data[0][0]
                                                         ### N_combin[l-1] is corresponding to nodes of layer l. Its first row is corresponding to node combination of layer 1
    G2_N_nodes = [data[0][0]]                                                     
    for l in range (1,len(data[0])-1):                   ### l: number of layers which starts from 1 not 0 (input nodes are considered before)
        G2_N_nodes.append(len(N_combin[l-1]))
        for n in range (len(N_combin[l-1])):             ### n: number of combination nodes in each layer l    
            C_Nodes = []
            lower_bound_biases = []
            upper_bound_biases = []
            for i in N_combin[l-1][n]:

                node = 'L'+str(l)+':'+str(i)
                bias = G1.nodes['L'+str(l)+':'+str(i)]['bias']
                lower_bound_biases.append(bias[0])
                upper_bound_biases.append(bias[1])
                C_Nodes.append(node)
            
            min_bias = min(lower_bound_biases)
            max_bias = max(upper_bound_biases)
            C_bias = [min_bias, max_bias]
            G2.add_node('C'+str(l)+':'+str(n+1), Nodes = C_Nodes, bias = C_bias)
            
    # assigning output nodes seperately because there is no change in their biases for output layer
    for i in range(1,data[0][-1]+1):
        G2.add_node('C'+str(len(data[0])-1)+':'+str(i), bias = G1.nodes['L'+str(len(data[0])-1)+':'+str(i)]['bias'])
    # Number of neuron in each layer for abstraction graph G2   
    G2_N_nodes.append(data[0][-1])
    
    return G2, G2_N_nodes

################################################# creating first layer edges of a abstraction graph using Networkx

def abstraction_graph_firstlayer_edges (G1, N_combin, data):
    # assigning input edges seperately because there is no bias for input layer
    for n1 in range (data[0][0]):
        for k1 in range (len(N_combin[0])):
            lower_bound_weights1 = []
            upper_bound_weights1 = []
            for f11 in N_combin[0][k1]:
                    weight1 = G1['L'+str(0)+':'+str(n1+1)]['L'+str(1)+':'+str(f11)]['Rweight']
                    lower_bound_weights1.append(weight1[0])
                    upper_bound_weights1.append(weight1[1])
            min_weight1 = min(lower_bound_weights1)           
            max_weight1 = max(upper_bound_weights1)
            G2.add_edge('C'+str(0)+':'+str(n1+1),'C'+str(1)+':'+str(k1+1), C_weight = [min_weight1, max_weight1])
            #print 'G2', G2.edges['C0:1','C1:1']['C_weight']
    return G2

################################################# creating hidden layer edges of a abstraction graph using Networkx 

def abstraction_graph_hiddenlayer_edges (G1, N_combin, data):
    #other layers
    for l in range (1,len(data[0])-2):
        for n in range (len(N_combin[l-1])):
            for k in range (len(N_combin[l])):
                lower_bound_weights = []
                upper_bound_weights = []
                for f1 in N_combin[l-1][n]:
                    for f2 in N_combin[l][k]:
                        weight = G1['L'+str(l)+':'+str(f1)]['L'+str(l+1)+':'+str(f2)]['Rweight']
                        lower_bound_weights.append(weight[0])
                        upper_bound_weights.append(weight[1])
                min_weight = len(N_combin[l-1][n]) * min(lower_bound_weights)           
                max_weight = len(N_combin[l-1][n]) * max(upper_bound_weights)
                G2.add_edge('C'+str(l)+':'+str(n+1),'C'+str(l+1)+':'+str(k+1), C_weight = [min_weight, max_weight])
    return G2

################################################# creating output layer edges of a abstraction graph using Networkx 

def abstraction_graph_outputlayer_edges (G1, N_combin, data):
    #output layer
    for k2 in range (len(N_combin[-1])):
        for n2 in range (data[0][-1]):
            lower_bound_weights2 = []
            upper_bound_weights2 = []
            for f22 in N_combin[-1][k2]:
                weight2 = G1['L'+str(len(data[0])-2)+':'+str(f22)]['L'+str(len(data[0])-1)+':'+str(n2+1)]['Rweight']
                lower_bound_weights2.append(weight2[0])
                upper_bound_weights2.append(weight2[1])
            min_weight2 = len(N_combin[-1][k2])* min(lower_bound_weights2)           
            max_weight2 = len(N_combin[-1][k2]) * max(upper_bound_weights2)
            G2.add_edge('C'+str(len(data[0])-2)+':'+str(k2+1),'C'+str(len(data[0])-1)+':'+str(n2+1), C_weight = [min_weight2, max_weight2])
            #print 'G2', G2.edges['C2:1','C3:1']['C_weight'] 
    return G2

################################################# reading the input information from the text file

def read_input_file (file_path):
        
        f = open(file_path, "r")
        data_str = f.read()
        data_lst_str = data_str.strip("\n").split("\n")

        N_combin_str = []                                    ### converting string data to a integer list format in this section 
        for i in data_lst_str:
            N_combin_str.append(i.split(';'))
            
        N_combin = []    
        for k in N_combin_str:
            N_combin_each_layer = []
            for j in k:
                N_combin_each_node = []
                for i in j.split(','):
                    N_combin_each_node.append(float(i))
                N_combin_each_layer.append(N_combin_each_node)
            N_combin.append(N_combin_each_layer)   

        return N_combin
#%%
################################################# Main
     
data = read_file ('/Users/zahra/Documents/Projects/Neural Network coding files/Important Neural network script/main/Final/Converted_ACASXU_run2a_1_7_batch_2000.txt')
N_vertices, bias_pointr, G1 = graph_nodes(data)
G1 = graph_edges (G1, data)

#graph_print (G1, 'r')

Input_param = read_input_file('/Users/zahra/Documents/Projects/Neural Network coding files/Important Neural network script/main/Final/Experiment/main/Input_coeficient/Input_coeficient.txt')

import os
import glob 
import numpy as np
import xlwt 
from xlwt import Workbook 

# Workbook is created 
wb = Workbook() 
      
# add_sheet is used to create sheet. 
sheet1 = wb.add_sheet('Sheet 1') 
# Sheet header, first row
columns = ['Partition', 'Abstract_time', 'Encoding_time', 'Gurobi_time', 'min_output1','max_output1', 'min_output2', 'max_output2', 'min_output3','max_output3', 'min_output4', 'max_output4']

row_num = 0

for col_num in range(len(columns)):
    sheet1.write(row_num, col_num, columns[col_num])


first_col=[]
path = '/Users/zahra/Documents/Projects/Neural Network coding files/Important Neural network script/main/Final/Experiment/main/Random composition/8/*.txt'   
files = sorted(glob.glob(path))   
#'/Users/zahra/Documents/Projects/Neural Network coding files/Important Neural network script/main/Final/Experiment/main/Random composition/8/*.txt
for file in files:       
    
    N_combin = read_node_combination_file(file)
    
    start_time_converting2abstract = time.time()
    
    G2, G2_N_nodes = abstraction_graph_nodes (G1, N_combin, data)
    G2 = abstraction_graph_firstlayer_edges (G1, N_combin, data)
    G2 = abstraction_graph_hiddenlayer_edges (G1, N_combin, data)
    G2 = abstraction_graph_outputlayer_edges (G1, N_combin, data)
    
    converting2abstract_time = (time.time() - start_time_converting2abstract)    
    #graph_print (G2, 'b')
    
    
    #seprating the name of the file from path and extension
    path = file
    root = os.path.splitext(path)[0] 
    file_name = os.path.basename(root)
    first_col.append(file_name)
    #first_col = np.transpose(first_Rcol)

#Output = open("abstraction_neuralnet.txt","w+")

    execfile('encoding.py')
    row = [converting2abstract_time, Encoding_time_abstract, Gurobi_time_abstract, min(outputs_range[0]), max(outputs_range[0]), min(outputs_range[1]), max(outputs_range[1]), min(outputs_range[2]), max(outputs_range[2]), min(outputs_range[3]), max(outputs_range[3])]

#%%
########################################
# Writing to an excel  
# sheet using Python 
 
  
    #for row in rows:
    row_num += 1
       
    sheet1.write(row_num, 0, first_col[row_num-1])
    
    for col_num in range(len(row)):
        sheet1.write(row_num, col_num+1, row[col_num])
        
    #rows = User.objects.all().values_list('divided', 'converting2abstract_time', 'Encoding_time_abstract', 'Gurobi_time_abstract')
    
    wb.save('composition1_32.xls')         
  
