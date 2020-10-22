#!/usr/bin/env python
# coding: utf-8

# In[79]:


import os
import sys
import pickle
from tqdm import tqdm


# In[82]:

n = "0"
index_file = ""
if len(sys.argv) < 3:
	index_file = sys.argv[1]
else :
	index_file = sys.argv[1]
	n = sys.argv[2]
# index_file = 'indexfile.dict'


# In[74]:


def printdict(index_file_name, no_of_items=-1):
    print('<term> : <df> : <offset>')
    a_file = open(index_file_name, "rb")
    output = pickle.load(a_file)
    
    for key in output.keys():
        print(key +' : '+str(output[key]['df'])+' : '+str(output[key]['offset']))
        if no_of_items > 0:
            no_of_items -=1
            if no_of_items == 0:
                break


# In[81]:


#print the dictionary, n = # of terms to be printed (optional)
printdict(index_file,int(n))