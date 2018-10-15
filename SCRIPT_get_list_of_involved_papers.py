

import pandas as pd
import numpy as np
import scipy
import operator
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
    print "number of involved authors:", len(lista_authors_merge) #   79948



    ####### input file (ALL disambiguated WoS)
    path='/home/julia/Dropbox_collaborations/Data/WoS_data/Disambiguated_authors/'
    filename='final.tsv'
    ####### tot  number of lines:    34556437



    nun_lines_testing=500000000000000




    string_lines="_all_lines"
    if nun_lines_testing >= 34556437:
        print "tot # lines to read: 34556437    ......."
    else:
         print "tot # lines to read:", nun_lines_testing,"     ......."
         string_lines="_"+str(nun_lines_testing)+"lines"

        
        
    list_involved_papers=[]

    cont=0
    cont_included=0
    with open(path+filename) as f:
        for line in f:  # line is a str  #### one line per WOS author      
        
            line=line.strip("\n")  #author_id	uid	seq	year	author_name	affiliation	total_pubs
        #print "\n",line
            if cont >0:

                flag_write=0
            
#example:   879592	WOS:000355773000004|WOS:000340362000001	1|1	2015|2014	Barker, J. G.|Barker, John G.	NIST, NIST Ctr Neutron Res, Gaithersburg, MD 20899 USA||NIST, Gaithersburg, MD 20899 USA	2
            
               # if cont == nun_lines_testing:   
                #      break    
         

                author_id=int(line.split("\t")[0] )
            
            
                if author_id in lista_authors_merge:                                               
            
                    cont_included +=1
              
            
                    list_uid=line.split("\t")[1].replace("WOS:","").split("|")  
               
                    list_involved_papers.extend(list_uid)
                
               

            cont +=1



    list_involved_papers=list(set(list_involved_papers))


    print "# involved papers:", len(list_involved_papers)


    filename_pickle=path_merge_cluster+"list_involved_papers"+string_lines+".pickle"    
    pickle.dump(list_involved_papers, open(filename_pickle, 'wb'))
    print "written:",path_merge_cluster+"list_involved_papers"+string_lines+".pickle"



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



