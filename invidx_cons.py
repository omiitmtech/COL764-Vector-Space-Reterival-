#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import os
import sys
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import collections
import pickle
from tqdm import tqdm


# In[ ]:


#file paths
# file_path = 'assignment1_data/test_data/'
# file_path = 'assignment1_data/training_files/'
file_path  = sys.argv[1] #collection Path coll-path
index_file = sys.argv[2] #indexfile 


# In[ ]:


#global variables
# global_docno_mapping_dict = {}
# global_term_mapping_dict = {}
# term_id_sequence = 1
# doc_id_sequence  = 1
# global_doc_no=0
no_of_docs = 0

temp_tag_freq_dict = {};
temp_term_freq_dict = {};
inverted_index = {}
indexfile_dict = {}
# sorted_inverted_index = sorted(inverted_index.keys())


# In[ ]:


#dictionary : term -> posting lists
# inverted_ndex : [term]:[(docno,frequency)]->[(docno,frequency)]
def build_invert_index(temp_dict, docno):
    for term in temp_dict:
        if term in inverted_index:
            inverted_index[term][0] +=1
            inverted_index[term][1].append((docno,temp_dict[term]))
        else:
            inverted_index[term] = [1,[(docno,temp_dict[term])]]


# In[ ]:


#Total text inside a <Text> </Text> will be processed here
# we tokenize the whole text data here, tokeninze and build a frequency dictionary here.
stop_words = stopwords.words('english')
def process_text(text):
    words = word_tokenize(text)
    words=[word.lower() for word in words if word.isalpha()]
    # words=[word for word in words if word.isalpha()]
    clean_text = [w for w in words if not w in stop_words]
    
    for term in clean_text:
        term = term.strip()
        
        if term in temp_term_freq_dict:
            temp_term_freq_dict[term] +=1;
        else :
            temp_term_freq_dict[term] = 1;
        


# In[ ]:


# #process text and update the inverted_index
# def process_tags(tag_text):
    
#     rootx = ET.fromstring(str(tag_text))
# #     print(rootx.text)
#     cur_tag = "";
#     cur_term = "";
#     flag = 0
#     for child in rootx:
        
#         if flag == 0:
#             cur_tag = child.tag
#             flag = 1
# #         print( 'child tag :', child.tag)
#         if(child.tag == cur_tag):
#             cur_term = cur_term+" "+child.text.strip()
#         else:
#             if cur_tag == 'organization':
#                 cur_term = 'O:'+cur_term.strip()
# #                 term_id_entry(cur_term,doc_no.text)
#             elif cur_tag == 'location':
#                 cur_term = 'L:'+cur_term.strip()
# #                 term_id_entry(cur_term,doc_no.text)
#             elif cur_tag == 'person':
#                 cur_term = 'P:'+cur_term.strip()
# #                 term_id_entry(cur_term,doc_no.text)
            
#             # do tag entry in the frequency table
#             if cur_term in temp_tag_freq_dict:
#                 temp_tag_freq_dict[cur_term] +=1;
#             else :
#                 temp_tag_freq_dict[cur_term] = 1;
            
#             #preparing to recieve next tag
#             cur_tag = child.tag  #new tag taken care
#             cur_term = child.text.strip() #New text taken care
            
#     # do the last tag entry in the frequency table
    
#     if cur_tag == 'organization':
#         cur_term = 'O:'+cur_term.strip()
#     elif cur_tag == 'location':
#         cur_term = 'L:'+cur_term.strip()
#     elif cur_tag == 'person':
#         cur_term = 'P:'+cur_term.strip()
    
#     if cur_term in temp_tag_freq_dict:
#         temp_tag_freq_dict[cur_term] +=1;
#     else :
#         temp_tag_freq_dict[cur_term] = 1;

#process text and update the inverted_index
def process_tags(tag_text):
    rootx = ET.fromstring(str(tag_text))
    cur_term = "";
    for child in rootx:
        if child.tag == 'organization':
            cur_term = 'O:'+child.text.strip()
        elif child.tag == 'location':
            cur_term = 'L:'+child.text.strip()
        elif child.tag == 'person':
            cur_term = 'P:'+child.text.strip()

        # cur_term = cur_term.lower()
        if cur_term in temp_tag_freq_dict:
            temp_tag_freq_dict[cur_term] +=1;
        else :
            temp_tag_freq_dict[cur_term] = 1;

# In[ ]:


data_files = os.listdir(file_path)
for file in tqdm(data_files):
    with open(file_path+file,"r") as f:
        soup = BeautifulSoup(f, "lxml")
        for doc_all_content in  soup.find_all('doc'):
#  ---------------Single document processing ----------------------------
            doc_no = doc_all_content.find('docno')
            #no. of doccuments in the collection
            no_of_docs +=1
            #we get doc number
            #mapping is done from from docno to an integer
#             if doc_no in global_docno_mapping_dict:
#                 term_id = global_docno_mapping_dict[doc_no.text]
#             else:
#                 global_docno_mapping_dict[doc_no.text]=doc_id_sequence
#                 term_id = doc_id_sequence
#                 doc_id_sequence += 1

#  ------------------All texts processing ------------------------------------
            for doc_text in doc_all_content.find_all('text'):
                #we get text here
                pure_text = doc_text.text
                #process text and update inverted index
                process_text(pure_text)
#                 print("---new doc ----")
                #process tags and update inverted index
                process_tags(doc_text)
                flag = "olddoc"
            
            #build inverted index here
            build_invert_index(temp_tag_freq_dict,doc_no.text.strip())
            temp_tag_freq_dict.clear()
            
            #build inverted index here
            build_invert_index(temp_term_freq_dict,doc_no.text.strip())
            temp_term_freq_dict.clear()
            
#   -----------------------Single document processing end---------------------
                    




# In[ ]:

def save_posting_Lists(dict_to_save, pickle_dict_name):
    with open(pickle_dict_name, 'wb') as f:
        offset = 0
        df = 0
        for key, value in dict_to_save.items():
            pkldata = pickle.dumps(value,-1)
            size = len(pkldata)
            df = value[0]
            indexfile_dict[key] = {'offset': offset,'df':df, 'size': size}
            f.write(pkldata)
            offset += size



# In[ ]:


def save_dictionary(dict_to_save,pickle_dict_name):
    dict_to_save['toal_docs_in_collection'] = {'offset': no_of_docs, 'df': 0, 'size': 0} 
    c_file = open(pickle_dict_name, "wb")
    pickle.dump(dict_to_save, c_file,-1)
    c_file.close()

# In[ ]:


# def read_dictionary(term):
#     offset = indexfile_dict[term]['offset']
#     size   = indexfile_dict[term]['size']
#     with open('indexfile.idx', 'rb') as f:
#         f.seek(offset)
#         pkldata = f.read(size)
#         posting_list = pickle.loads(pkldata)
#     print((term, posting_list))


# In[ ]:
#Write posting lists to the disk
save_posting_Lists(inverted_index,index_file+'.idx')

#write dictionary to the disk
save_dictionary(indexfile_dict,index_file+'.dict')