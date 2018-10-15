
import pandas as pd
import numpy as np
import scipy
import operator
import difflib
import itertools


try:
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle
    
import unicodedata
    
 

def main():

    path_merge_cluster='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'
     
#path_merge_linux='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/'
    filename="Merged_linkedin-WoS_GS_extra70univ.pickle"
    df_merged = pd.read_pickle(path_merge_cluster+filename)



    aux=df_merged['author_disambig_id_wos'].dropna().tolist()
    lista_authors_merge = [int(x) for x in aux] 
    print "# wos authors in merged file", len(lista_authors_merge) #   79948


    file_pickle = open(path_merge_cluster+"list_involved_papers_all_lines.pickle",'rb')        ### num papers:  2674932
    list_involved_papers  = pickle.load(file_pickle)
    set_list_involved_papers  =  set(list_involved_papers )


    print "# involved papers:", len(list_involved_papers), len(set_list_involved_papers)



 
    #### input file (ALL disambiguated WoS)
    path_wos_cluster='/home/julia/Dropbox_collaborations/Data/WoS_data/Disambiguated_authors/'
    filename='final.tsv'
    #### tot  number of lines:    34556437



    nun_lines_testing=500000000000000



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
    with open(path_wos_cluster+filename) as f:
        for line in  f:  # line is a str  #### one line per WOS author      
            line=line.strip("\n")  #author_id	uid	seq	year	author_name	affiliation	total_pubs
        #print "\n",line
            if cont >0:

                flag_write=0
            
#example:   879592	WOS:000355773000004|WOS:000340362000001	1|1	2015|2014	Barker, J. G.|Barker, John G.	NIST, NIST Ctr Neutron Res, Gaithersburg, MD 20899 USA||NIST, Gaithersburg, MD 20899 USA	2
            
#                if cont == nun_lines_testing:   
 #                     break    
         

                author_id=int(line.split("\t")[0] )
            
                list_uid=line.split("\t")[1].replace("WOS:","").split("|")  
                    #list_uid=[x.replace("WOS:","") for x in uid]
           
            
            
            
            
            
            
                if   len(set_list_involved_papers & set(list_uid)) >0   :     # i need to take into account also authors not from Linkedin but who are their co-authors!!   
            
                    cont_included +=1
                #print cont_included
            
                
                
                
                    seq=line.split("\t")[2].split("|")
                    list_seq=[int(x) for x in seq]       # o-index, also, if -1 means ranking unknown for that particular paper               
 
               
#                 if -1 in list_seq:
#                     print list_seq
#                     raw_input()
    
                
                
                    total_pub=float(line.split("\t")[6])

                
                       
                
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


             
                   
                
                    ##### to be calculated later on:
                    master_dict_author_id_att[author_id]['papers_1st']=0.
                    master_dict_author_id_att[author_id]['papers_last']=0.   
                    master_dict_author_id_att[author_id]['papers_solo_author']=0.
                    master_dict_author_id_att[author_id]['coauthors']=[]   # OJO!!!! i also need to include as coauthors those outside the LinkedIn dataset!!!
                   
                    
             
          #  print cont, 34556437

            cont +=1
        


    print "# lines read (# authors in WoS file):", cont, "   included (found from merged file):", len(master_dict_author_id_att), cont_included
    print "# papers involved:",len(dict_paper_list_authors)

    print "# wos authors from merged file:",len(lista_authors_merge), "  # authors in dict:", len(master_dict_author_id_att)

#>>> list(itertools.combinations('ABC', 2))
#[('A', 'B'), ('A', 'C'), ('B', 'C')]



    list_too_many=[]   
    for paper in dict_paper_list_authors:
        if len(dict_paper_list_authors[paper])>200:
           # print paper, dict_paper_list_authors[paper]
            #raw_input()
            
            list_too_many.append(paper)

    print  "# papers with more than 200 coauthors:", len(list_too_many)



  #  raw_input()

    
    #cont=1
    #tot=len(dict_paper_list_authors)
    print "adding coauthors....."   
    for paper_id in dict_paper_list_authors:
#        list_coathors_current_paper=dict_paper_list_authors[paper_id]



        if paper_id not in list_too_many:   # a few papers (2544)  have more than 500 authors and make the combinatorial problem too hard!
            lista_tuplas=list(itertools.combinations(dict_paper_list_authors[paper_id], 2)) # combinations of 2 authors without repetition
            
            #print cont, tot, paper_id,len(dict_paper_list_authors[paper_id]),len(lista_tuplas)
            #cont +=1
            for tupla in lista_tuplas:
                author1=tupla[0]
                author2=tupla[1]
                if author1 not in master_dict_author_id_att[author2]['coauthors']:
                    master_dict_author_id_att[author2]['coauthors'].append(author1)
                if author2 not in master_dict_author_id_att[author1]['coauthors']:
                    master_dict_author_id_att[author1]['coauthors'].append(author2)
        
    print "     done"
    







   # print "removing redundancy in list of coauthors......"
# i remove redundancy in list of coauthors     
    #for author_id in master_dict_author_id_att:             
       # HOW TO REMOVE ELEMENTS FROM A LIST BY VALUE (WHEN THERE MAY BE REPETITIONS):
        #     a = [1, 2, 3, 4, 2, 3, 4, 2, 7, 2]
        # >>> a = [x for x in a if x != 2]
        
        # I REMOVE THE AUTHOR HERSELF FROM THE LIST OF COAUTHORS
     #       master_dict_author_id_att[author_id]['coauthors']=[ x for x in list(set(master_dict_author_id_att[author_id]['coauthors'])) if x != author_id ]  

    #print "     done"





    filename_pickle=path_merge_cluster+"master_dict_author_id_att"+string_lines+".pickle"    
    pickle.dump(master_dict_author_id_att, open(filename_pickle, 'wb'))
    print "written:",filename_pickle  
    print len(master_dict_author_id_att)
    
     
    
    filename_pickle=path_merge_cluster+"dict_paper_list_authors"+string_lines+".pickle"        
    pickle.dump(dict_paper_list_authors, open(filename_pickle, 'wb'))
    print "written:",filename_pickle  
    print len(dict_paper_list_authors)
    
    
    filename_pickle=path_merge_cluster+"dict_paper_dict_author_seq"+string_lines+".pickle"        
    pickle.dump(dict_paper_dict_author_seq, open(filename_pickle, 'wb'))
    print "written:",filename_pickle  
    print len(dict_paper_dict_author_seq)
    
    
    filename_pickle=path_merge_cluster+"dict_author_dict_paper_seq"+string_lines+".pickle"        
    pickle.dump(dict_author_dict_paper_seq, open(filename_pickle, 'wb'))
    print "written:",filename_pickle  
    print len(dict_author_dict_paper_seq)


# In[25]:

  #  for author in master_dict_author_id_att:
   #     if len(master_dict_author_id_att[author]['coauthors'])>0:
    #        print author, master_dict_author_id_att[author]
     #       print "author-paper seq",dict_author_dict_paper_seq[author]
      #      for paper in dict_author_dict_paper_seq[author]:
       #         print paper, dict_paper_dict_author_seq[paper]
        #    raw_input()







######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "



#####################################
####################################
