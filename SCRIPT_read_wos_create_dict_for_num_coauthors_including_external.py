
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from tqdm import tnrange, tqdm_notebook
import scipy
import operator
import difflib
from IPython.core.display import display,HTML
try:
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle
    
import unicodedata
    
 
    
display(HTML("<style>.container { width:100% !important; }</style>"))  # to make the notebook use the entire width of the browser


# In[2]:

path_merge_linux='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/'
filename="Merged_linkedin-WoS_GS_extra70univ.pickle"
get_ipython().magic(u'time df_merged = pd.read_pickle(path_merge_linux+filename)')



# In[3]:

for item in df_merged.columns:
    print item


# In[5]:

aux=df_merged['author_disambig_id_wos'].dropna().tolist()
lista_authors_merge = [int(x) for x in aux] 
print len(lista_authors_merge) #   79948


# In[8]:

#file_pickle = open(path_merge_linux+"list_relevant_papers_partial.pickle",'rb') 
file_pickle = open(path_merge_linux+"list_involved_papers_all_lines.pickle",'rb')        ### num papers:  2674932
get_ipython().magic(u'time list_involved_papers  = pickle.load(file_pickle)')


print "# involved papers:", len(list_involved_papers), len(set(list_involved_papers))



# In[ ]:


#### input file (ALL disambiguated WoS)
path='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/WoS_data/Disambiguated_authors/'
filename='final.tsv'
#### tot  number of lines:    34556437

nun_lines_testing=50000



string_lines="_all_lines"
if nun_lines_testing >= 34556437:
    print "tot # lines to read: 34556437    ......."
else:
    print "tot # lines to read:", nun_lines_testing,"     ......."
    string_lines="_"+str(nun_lines_testing)+"lines"

        
        
        
master_dict_author_id_att={}

dict_paper_list_authors={}

dict_author_dict_paper_seq={}
dict_paper_dict_author_seq={}




cont=0
cont_included=0
with open(path+filename) as f:
    for line in  tqdm_notebook(f):  # line is a str  #### one line per WOS author      
        line=line.strip("\n")  #author_id	uid	seq	year	author_name	affiliation	total_pubs
        #print "\n",line
        if cont >0:

            flag_write=0
            
#example:   879592	WOS:000355773000004|WOS:000340362000001	1|1	2015|2014	Barker, J. G.|Barker, John G.	NIST, NIST Ctr Neutron Res, Gaithersburg, MD 20899 USA||NIST, Gaithersburg, MD 20899 USA	2
            
            if cont == nun_lines_testing:   
                  break    
         

            author_id=int(line.split("\t")[0] )
            
            list_uid=line.split("\t")[1].replace("WOS:","").split("|")  
                #list_uid=[x.replace("WOS:","") for x in uid]
           
            
            
            
            
            
            
            if   len(set(list_involved_papers) & set(list_uid)) >0   :     # i need to take into account also authors not from Linkedin but who are their co-authors!!   
            
                cont_included +=1
                #print cont_included
            
                
                
                
                seq=line.split("\t")[2].split("|")
                list_seq=[int(x) for x in seq]       # o-index, also, if -1 means ranking unknown for that particular paper               
 
               
#                 if -1 in list_seq:
#                     print list_seq
#                     raw_input()
    
                
                
                total_pub=float(line.split("\t")[6])

                
                cont_1st=0. # i cant know if last author here because i dont know the number of authors in the paper
                for seq in list_seq:
                    if seq==0:
                        cont_1st +=1.                     
                
                
#                 if len(list_seq)  != len(list_uid):
#                     print list_seq
#                     print list_uid
#                     raw_input()
                
                dict_author_dict_paper_seq[author_id]={}
                for i in range(len(list_uid)):
                    paper=list_uid[i]
                    rank=list_seq[i]
                    
                    dict_author_dict_paper_seq[author_id][paper]=rank
                                
                    try:
                        dict_paper_dict_author_seq[paper]
                    except KeyError:
                        dict_paper_dict_author_seq[paper]={}                                 
                                    
                    dict_paper_dict_author_seq[paper][author_id]=rank
                        
                        
                                                           
                    try:                             
                        dict_paper_list_authors[paper]
                    except KeyError:
                        dict_paper_list_authors[paper]=[]             
                        
                    dict_paper_list_authors[paper].append(author_id)
                    
                        
                        
                        
                        
                        
      
                master_dict_author_id_att[author_id]={}             
    
              
                master_dict_author_id_att[author_id]['num_papers']=total_pub                
                master_dict_author_id_att[author_id]['papers_1st']=cont_1st
                
                ##### to be calculated later on:
                master_dict_author_id_att[author_id]['papers_last']=0.   
                master_dict_author_id_att[author_id]['papers_unique_author']=0.
                master_dict_author_id_att[author_id]['coauthors']=[]   # OJO!!!! i also need to include as coauthors those outside the LinkedIn dataset!!!
                   
                    
             
                

        cont +=1
        


print "# lines read (# authors in WoS file):", cont, "   included (found from merged file):", len(master_dict_author_id_att), cont_included
print "# papers involved:",len(dict_paper_list_authors)

print "# wos authors from merged file:",len(lista_authors_merge), "  # authors in dict:", len(master_dict_author_id_att)


# In[10]:

len(master_dict_author_id_att)


# In[11]:

for paper_id in dict_paper_list_authors:
    list_coathors_current_paper=dict_paper_list_authors[paper_id]
    
    for author_id in list_coathors_current_paper:
        master_dict_author_id_att[author_id]['coauthors'].extend(list_coathors_current_paper)
    
    
# i remove redundancy in list of coauthors     
for author_id in master_dict_author_id_att:  
       
    
       # HOW TO REMOVE ELEMENTS FROM A LIST BY VALUE (WHEN THERE MAY BE REPETITIONS):
        #     a = [1, 2, 3, 4, 2, 3, 4, 2, 7, 2]
        # >>> a = [x for x in a if x != 2]
        
        # I REMOVE THE AUTHOR HERSELF FROM THE LIST OF COAUTHORS
        master_dict_author_id_att[author_id]['coauthors']=[ x for x in list(set(master_dict_author_id_att[author_id]['coauthors'])) if x != author_id ]  


# In[26]:

path_merge_linux='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/'



filename_pickle=path_merge_linux+"master_dict_author_id_att"+string_lines+".pickle"    
pickle.dump(master_dict_author_id_att, open(filename_pickle, 'wb'))
print "written:",filename_pickle  
print len(master_dict_author_id_att)


filename_pickle=path_merge_linux+"dict_paper_list_authors"+string_lines+".pickle"        
pickle.dump(dict_paper_list_authors, open(filename_pickle, 'wb'))
print "written:",filename_pickle  
print len(dict_paper_list_authors)


filename_pickle=path_merge_linux+"dict_paper_dict_author_seq"+string_lines+".pickle"        
pickle.dump(dict_paper_dict_author_seq, open(filename_pickle, 'wb'))
print "written:",filename_pickle  
print len(dict_paper_dict_author_seq)


filename_pickle=path_merge_linux+"dict_author_dict_paper_seq"+string_lines+".pickle"        
pickle.dump(dict_author_dict_paper_seq, open(filename_pickle, 'wb'))
print "written:",filename_pickle  
print len(dict_author_dict_paper_seq)




# In[25]:

for author in master_dict_author_id_att:
    if len(master_dict_author_id_att[author]['coauthors'])>0:
        print author, master_dict_author_id_att[author]
        print "author-paper seq",dict_author_dict_paper_seq[author]
        for paper in dict_author_dict_paper_seq[author]:
            print paper, dict_paper_dict_author_seq[paper]
        raw_input()


# In[16]:

dict_author_dict_paper_seq


# In[17]:

dict_paper_dict_author_seq


# In[19]:

master_dict_author_id_att


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



