#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import os
import sys
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math
import pickle
import operator
from tqdm import tqdm


# In[19]:


#terminal paraeters
#parameters : queryfile,k,resultfile,indexfile dictfile
#parameters : 'assignment1_data/Query/topics.51-100',10,output,indexfile.dict indexfile.idx

# queryfile = 'assignment1_data/Query/queryf.51-100'
# k = 10
# resultfile = 'output'
# index_file = 'indexfile.dict'
# dictfile   = 'indexfile.idx'

if len(sys.argv) == 5:
    queryfile = sys.argv[1]
    k = 10
    resultfile = sys.argv[2]
    index_file = sys.argv[3]
    dictfile   = sys.argv[4]                                                                                
else:
    queryfile = sys.argv[1]
    k = int(sys.argv[2])
    resultfile = sys.argv[3]
    index_file = sys.argv[4]
    dictfile   = sys.argv[5]

# In[11]:


#global dictionary
index_file = 'indexfile.dict'
def load_dictionary():
    a_file = open(index_file, "rb")
    indexfile_dict = pickle.load(a_file)
    return indexfile_dict
#load all dicitonary terms in memory
indexfile_dict = load_dictionary()
N = indexfile_dict['toal_docs_in_collection']['offset']
print('Total number of documents in the collection :',N)


# In[4]:


def read_dictionary(term):
    if term in indexfile_dict:
        offset = indexfile_dict[term]['offset']
        size   = indexfile_dict[term]['size']
        with open(dictfile, 'rb') as f:
            f.seek(offset)
            pkldata = f.read(size)
            posting_list = pickle.loads(pkldata)
        return posting_list


# In[5]:


score = {}
def cal_score(term):
    print('query :', term)
    posting_list = read_dictionary(term)
    if posting_list != None:
        #df_i is the count of documents containing term i.
        df_i = posting_list[0]
        for posting_tuple in posting_list[1]:
            doc_no = posting_tuple[0]
            f_ij = int(posting_tuple[1])
            #tf_ij = (1 + log f_ij),f_ij is the count of the term i in document j
            tf_ij = (1 + math.log2(f_ij))
            #idf_i = log(1 + N/df_i), N is the size of the document collection, df_i 
            # is the count of documents containing term i.
            idf_i = math.log2(1 + (N*1.0/df_i))
            w_ij = tf_ij*idf_i
            if doc_no in score:
                score[doc_no] += w_ij
            else:
                score[doc_no] = w_ij

# funciton to handle prefix queries
def special_cal_score(special_term):
    print('query :', special_term)
    special_term = special_term[:-1]
    all_prefix_terms = [ key for key,value in indexfile_dict.items() if key.startswith(special_term) ]
    print('all_prefix_terms :',all_prefix_terms)
    for term in all_prefix_terms:
#         print('term : ', term)
        posting_list = read_dictionary(term)
        if posting_list != None:
            #df_i is the count of documents containing term i.
            df_i = posting_list[0]
            for posting_tuple in posting_list[1]:
                doc_no = posting_tuple[0]
                f_ij = int(posting_tuple[1])
                #tf_ij = (1 + log f_ij),f_ij is the count of the term i in document j
                tf_ij = (1 + math.log2(f_ij))
                #idf_i = log(1 + N/df_i), N is the size of the document collection, df_i 
                # is the count of documents containing term i.
                idf_i = math.log2(1 + (N*1.0/df_i))
                w_ij = tf_ij*idf_i
                if doc_no in score:
                    score[doc_no] += w_ij
                else:
                    score[doc_no] = w_ij
# In[14]:


def process_query(v_queryfile):
    with open(v_queryfile,"r") as f:
        for line in f:
            if line[0]=='<' and line[1]=='n' and line[2]=='u' and line[3]=='m' and line[4]=='>':
                query_num = [word for word in line.split()]
                print('query no :',int(query_num[2]))
            if line[0]=='<' and line[1]=='t' and line[2]=='i' and line[3]=='t' and line[4]=='l' and line[5]=='e' and line[6]=='>':
                # query_title = [word.lower() for word in line.split()]
                query_title = [word for word in line.split()]
                print('Clear the previous query scores....')
                score.clear()
                print('query processing starts here...')
                print('current query :',query_title)
                for i in range(2,len(query_title)):
                    cur_query_term = query_title[i]
                    if cur_query_term[-1] == '*':
                        cur_query_term = cur_query_term.lower()
                        special_cal_score(cur_query_term)
                    elif cur_query_term[0]=='P' and cur_query_term[1]==':':
                        cal_score(cur_query_term)

                    elif cur_query_term[0]=='L' and cur_query_term[1]==':':
                        cal_score(cur_query_term)

                    elif cur_query_term[0]=='O' and cur_query_term[1]==':':
                        cal_score(cur_query_term)

                    elif cur_query_term[0]=='N' and cur_query_term[1]==':':
                        curr_term = cur_query_term
                        P_curr_term = 'P'+curr_term[1:]
                        cal_score(P_curr_term)
                        L_curr_term = 'L'+curr_term[1:]                        
                        cal_score(L_curr_term)
                        O_curr_term = 'O'+curr_term[1:] 
                        cal_score(O_curr_term)
                    else:
                        cur_query_term = cur_query_term.lower();
                        cal_score(cur_query_term)
                
                print('calculate top k score here...')
                sorted_score = dict( sorted(score.items(), key=operator.itemgetter(1),reverse=True))
                print('new query score...')
#                 print(sorted_score)
                print_topk_results(sorted_score,int(query_num[2]),k)
                
                


# In[15]:


def print_topk_results(score_dict,query_num, k_val):
    #Query id.0,Docid,Rank,Score,STANDARD
    rank = 1
    for key in score_dict.keys():
        result = str(query_num) + ' 0 '+' '+ key + ' ' + str(rank) + ' ' + str(score_dict[key]) + ' STANDARD'+'\n'
        with open(resultfile, "a") as f:
            f.write(result)
        rank +=1;
        k_val-=1;
        if k_val<=0 :
            f.close()
            break;


# In[17]:


#process the query file here
process_query(queryfile)


# In[ ]:




