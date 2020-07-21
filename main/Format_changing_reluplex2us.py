#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 15:04:00 2019
Submitted code for nips19
converting reluplex nn format to our neural network method format

@author: zahra
"""
#converting reluplex format to our interval Neural network
# reading the file and converting to the list
import itertools

def read_file(directory):
    f = open(directory, "r")
    data_str = f.read()
    data_str = data_str.strip(" ").split("\n")[3:]
    
    data = []                                      
    for i in range(0,3):
        sub_lst = [int(j) for j in data_str[i].strip(" ").strip(",").split(",")]  ### converting string data to a integer list format in this section
        data.append(sub_lst)
    for i in range(3, len(data_str)-1):
        sub_lst = [float(j) for j in data_str[i].strip(" ").strip(",").split(",")]   ### converting string data to a float list format in this section
        data.append(sub_lst)
            
    return data

#/////////////////////////////////////////// finding weights of every neuron and bias
    
def convertedformat(data):
    pointer = 7
    bias_allayer = []    
    W_Neurons_allayers = []  
    for i in range(len(data[1])-1):
        W_Neurons_1layer =[]
        for j in range(data[1][i]):
            W_Neuron =[]
            for k in range(data[1][i+1]): 
                W_Neuron.append(data[pointer+k][j])
                #print 'pointer+k', pointer+k
            W_Neurons_1layer.append(W_Neuron) 
        W_Neurons_allayers.append(W_Neurons_1layer)
        pointer += data[1][i+1]
        print 'pointer', pointer
        bias_1layer = [data[pointer+m][0] for m in range(data[1][i+1])]
        pointer += data[1][i+1]
        bias_allayer.append(bias_1layer) 
        
    return W_Neurons_allayers, bias_allayer

#///////////////////////////////////////////converting a list to string with "," as a separator
    
def lst2str (list):
    string = ",".join(map(str, list))  
        
    return string

#/////////////////////////////////////////////main
    
#name = input ('Give me the name of Reluplex neural network = ')    
#data = read_file ('/Users/zahra/Desktop/SHARE/ReluplexCav2017-master/nnet/'+name+'.nnet')
data = read_file ('/Users/zahra/Desktop/SHARE/ReluplexCav2017-master/nnet/ACASXU_run2a_1_7_batch_2000.nnet')
W_Neurons_allayers, bias_allayer = convertedformat(data)
#print 'data', data[-1]    
file = open('Converted_ACASXU_run2a_1_7_batch_2000.txt','w')

# writing the information about neuron number in each layer in first row of output file

for item in lst2str (data[1]):
    file.write(item)
file.write('\n')              #for transfering pointer to another line after for loop
     
# writing the information about neuron weights in each layer
for i in range(len(data[1])-1): 
    for j in range(data[1][i]):
        for item in lst2str (list(itertools.chain.from_iterable(itertools.repeat(x, 2) for x in W_Neurons_allayers[i][j]))): #converting to interval
            file.write(item)
        file.write('\n') 

# writing the information about neuron biases in each layer
bias_allayer_interval = []        
for i in range(len(data[1])-1): 
    bias_allayer_interval.append(list(itertools.chain.from_iterable(itertools.repeat(x, 2) for x in bias_allayer[i])))
    for j in range(data[1][i+1]):
        file.write("%s\n" % (str(bias_allayer_interval[i][j*2])+','+str(bias_allayer_interval[i][j*2+1])))
        
#Rweight = [data[lc][z*2], data[lc][z*2+1]]
file.close()

#execfile('Model_cheking_invariant.py')
