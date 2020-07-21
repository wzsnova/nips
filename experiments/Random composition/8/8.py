#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 14:43:28 2019

@author: zahra
"""

N = input('Give me number of files = ')
num_partition = input('Give me the number of partition = ')
num_partition1= str (num_partition)

items = [str(j) for j in range(N)]

for i in range(N):
    
    file = open('C'+ num_partition1+ '_' +items[i]+'.txt' ,'w')
    execfile('/Users/zahra/Documents/Projects/Neural Network coding files/Important Neural network script/main/Final/rand_main.py')






