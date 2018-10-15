


import pandas as pd
import numpy as np
import gzip

import scipy
import operator
import difflib

try:
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle
    
import unicodedata
    
 

def main():

    path_merge_linux='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'

    filename="Merged_linkedin-WoS_GS_extra70univ.pickle"
    df_merged = pd.read_pickle(path_merge_linux+filename)


    aux=df_merged['author_disambig_id_wos'].dropna().tolist()



    lista_authors_merge = [int(x) for x in aux] 
#print lista_authors_merge[0],type(lista_authors_merge[0])   INT
    print "# authors involved",len(lista_authors_merge)






    file_pickle = open(path_merge_linux+"list_involved_papers_all_lines.pickle",'rb')        ### num papers:  2674932
    list_involved_papers  = pickle.load(file_pickle)
    set_list_involved_papers=set(list_involved_papers)

    print "# involved papers:", len(list_involved_papers), len(set_list_involved_papers)



    string_lines= "_all_lines"

# written: /home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/master_dict_author_id_att_all_lines.pickle
# written: /home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/dict_paper_list_authors_all_lines.pickle
# written: /home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/dict_paper_dict_author_seq_all_lines.pickle
# written: /home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/dict_author_dict_paper_seq_all_lines.pickle

#/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/dict_paper_id_list_papers_that_cite_it_all_lines.pickle




#file_pickle = open(path_merge_linux+"dict_paper_dict_author_seq_all_lines.pickle",'rb')
    file_pickle = open(path_merge_linux+"dict_paper_dict_author_seq"+string_lines+".pickle",'rb')
    dict_paper_dict_author_seq  = pickle.load(file_pickle)
    print "# papers in dict",len(dict_paper_dict_author_seq)
    
#file_pickle = open(path_merge_linux+"master_dict_author_id_att_all_lines.pickle",'rb')
    file_pickle = open(path_merge_linux+"master_dict_author_id_att"+string_lines+".pickle",'rb')
    master_dict_author_id_att = pickle.load(file_pickle)
    print "# authors in dict",len(master_dict_author_id_att)
    
#file_pickle = open(path_merge_linux+"dict_paper_id_list_papers_that_cite_it"+string_lines+".pickle",'rb')
#file_pickle = open(path_merge_linux+"dict_paper_id_list_papers_that_cite_it_all_lines.pickle",'rb')
    file_pickle = open(path_merge_linux+"dict_paper_id_list_papers_that_cite_it_all_lines.pickle",'rb')
    dict_paper_id_list_papers_that_cite_it = pickle.load(file_pickle)
    print "# papers in dict",len(dict_paper_id_list_papers_that_cite_it)





    file_pickle = open(path_merge_linux+"dict_author_dict_paper_seq_all_lines.pickle",'rb')
    dict_author_dict_paper_seq  = pickle.load(file_pickle)
    print "# authors in dict",len(dict_author_dict_paper_seq)









    for author in master_dict_author_id_att:
    
       
        try:            
            master_dict_author_id_att[author]['publications']=dict_author_dict_paper_seq[author].keys()                                                                  
        except:
            master_dict_author_id_att[author]['publications']=[]
       
       
        try:
            master_dict_author_id_att[author]['publications_seq']=dict_author_dict_paper_seq[author]
        except:
            master_dict_author_id_att[author]['publications_seq']={}
            
       #print author, master_dict_author_id_att[author]
       #raw_input()
       
       



  
    for paper in dict_paper_dict_author_seq:
        #print paper, dict_paper_dict_author_seq[paper]
        
        num_author_in_paper=max(dict_paper_dict_author_seq[paper].values())+1

        list_current_authors=dict_paper_dict_author_seq[paper]


        for author in list_current_authors:                  
           
            if dict_paper_dict_author_seq[paper][author]== (num_author_in_paper-1):
                master_dict_author_id_att[author]['papers_last'] +=1
            
            if dict_paper_dict_author_seq[paper][author]==0:
                master_dict_author_id_att[author]['papers_1st'] +=1    
                        
            
                if len(dict_paper_dict_author_seq[paper]) ==1:
                    master_dict_author_id_att[author]['papers_solo_author'] +=1
         
        
      



   
    #### i collect the number of citations for the authors
    list_not_cited=[]
    for author in master_dict_author_id_att:

    
        list_papers=master_dict_author_id_att[author]['publications_seq'].keys()
    
       
        num_cit=0
        for paper in list_papers:
            try:
                if paper in dict_paper_id_list_papers_that_cite_it[paper]:  # if self-citation of the paper, i remove all possible occurrences of it
                #print len(dict_paper_id_list_papers_that_cite_it[paper]),
                    aux_list = list(filter(lambda x: x!= paper, dict_paper_id_list_papers_that_cite_it[paper]))
                    dict_paper_id_list_papers_that_cite_it[paper]=aux_list
            
                num_cit += len(dict_paper_id_list_papers_that_cite_it[paper])
            
           
            except KeyError: pass

        master_dict_author_id_att[author]['num_citations']=num_cit

    print "citations done.   "


# In[ ]:

    filename_pickle=path_merge_linux+"master_dict_author_id_att"+string_lines+"_with_citations.pickle"    
    pickle.dump(master_dict_author_id_att, open(filename_pickle, 'wb'))
    print "written:",filename_pickle  
    print len(master_dict_author_id_att)









###############################
#example: 76924930: {'coauthors': [3840074, 67750750, 12225567],   'num_papers': 331.0,   'papers_1st': 1.0,   'papers_last': 0.0,   'papers_solo_author': 0.0}
   #master_dict_author_id_att[author]['coauthors'] 
    
    
######## i create the new fields 
    df_merged['num_coauthors'] = df_merged['author_disambig_id_wos'].fillna('').apply(add_num_coathors,args=[master_dict_author_id_att])

    df_merged['num_papers_double_check'] = df_merged['author_disambig_id_wos'].fillna('').apply(add_num_papers_to_doublecheck,args=[master_dict_author_id_att])

    
    df_merged['num_papers_1st'] = df_merged['author_disambig_id_wos'].fillna('').apply(add_papers_1st,args=[master_dict_author_id_att])
     
    df_merged['num_papers_last'] = df_merged['author_disambig_id_wos'].fillna('').apply(add_papers_last,args=[master_dict_author_id_att])
    
    df_merged['num_papers_solo'] = df_merged['author_disambig_id_wos'].fillna('').apply(add_papers_solo,args=[master_dict_author_id_att])


    df_merged['list_pub'] = df_merged['author_disambig_id_wos'].fillna('').apply(add_list_papers,args=[master_dict_author_id_att])



    df_merged['num_citations'] = df_merged['author_disambig_id_wos'].fillna('').apply(add_num_citations,args=[master_dict_author_id_att])
          
    df_merged['publ_seq'] = df_merged['author_disambig_id_wos'].fillna('').apply(add_publ_seq,args=[master_dict_author_id_att])
  







    filename_merged="Merged_linkedin-WoS_GS_extra70univ.pickle"
    df_merged.to_pickle(path_merge_linux+filename_merged.split(".pickle")[0] +"_added_num_coauth"+string_lines+".pickle" )
    print "pickle done:", path_merge_linux+filename_merged.split(".pickle")[0] +"_added_num_coauth"+string_lines+".pickle"        




    writer = pd.ExcelWriter(path_merge_linux+filename_merged.split(".pickle")[0] +"_added_num_coauth"+string_lines+".xlsx", engine='xlsxwriter',options={'strings_to_urls': False})
# Convert the dataframe to an XlsxWriter Excel object.
    df_merged.to_excel(writer, sheet_name='Sheet1')
## OJO! hay url muy largas que hacen que el sistema se cuelgue (solucion: no permitirle que las considere url, sino simplemente str)

# Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print "xlsx done",path_merge_linux+filename_merged.split(".pickle")[0] +"_added_num_coauth"+string_lines+".xlsx"






###############################################

def add_num_papers_to_doublecheck(wos_id,dicc):    
      
    num_papers=np.nan             
    try:          
        wos_id=int(wos_id)
        num_papers= dicc[wos_id]['num_papers']
        return num_papers
                    
    except:  pass
        
        
        
###############################

def add_num_coathors(wos_id,dicc):    
      
    num_coathors=np.nan             
    try:          
        wos_id=int(wos_id)
        num_coathors= len(dicc[wos_id]['coauthors'] )
        return num_coathors                    
    except:  pass
        
        
        
###############################
def add_papers_1st(wos_id,dicc):    
       
    num_papers_1st=np.nan             
    try:          
        wos_id=int(wos_id)
        num_papers_1st= dicc[wos_id]['papers_1st']
        return num_papers_1st                    
    except:  pass
        
        
        
###############################
def add_papers_last(wos_id,dicc):    
      
    num_papers_last=np.nan             
    try:          
        wos_id=int(wos_id)
        num_papers_last= dicc[wos_id]['papers_last']
        return num_papers_last                    
    except:  pass
        
                
             
###############################
def add_papers_solo(wos_id,dicc):    
      
    num_papers_solo=np.nan             
    try:          
        wos_id=int(wos_id)
        num_papers_solo= dicc[wos_id]['papers_solo_author']
        return num_papers_solo                    
    except:  pass
       
        
        
        
###############################       
def add_list_papers(wos_id,dicc):    
    
   # print "wos id:",wos_id   
    papers=np.nan             
    try:          
        wos_id=int(wos_id)
        papers= "|".join(dicc[wos_id]['publications_seq'].keys())
        return papers                    
    except:  pass
        
              
       
        
###############################       
def add_num_citations(wos_id,dicc):    
    
   # print "wos id:",wos_id   
    citations=np.nan             
    try:          
        wos_id=int(wos_id)
        citations=dicc[wos_id]['num_citations']
        return citations                    
    except:  pass
        
             

###############################       
def add_publ_seq(wos_id,dicc):    
    
   # print "wos id:",wos_id   
    public_seq=""             
    try:          
        wos_id=int(wos_id)
        public_seq=str(dicc[wos_id]['publications_seq']).replace("{","").replace("}","").replace(" ","").replace(",","|").replace("'","")
        return public_seq                    
    except:  pass
        
              
#      publications_seq': {'000326311600057': 0, '000365789100016': 5,  '000300231400005': 0, '000323103900037': 0, '000332386100011': 9, '000331417700003': 0}

# In[16]:

# %timeit lista+lista2 # 595 ns per loop


# %timeit lista.extend(lista2) #343 ns per loop



######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "



############################3
#################################



