
import pandas as pd
import numpy as np

import scipy
import operator


try:
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle
 
 

def main():




    nun_lines_testing=50000000000000000


    string_lines="_all_lines"
    if nun_lines_testing >= 34556437:
        print "tot # lines to read: 34556437    ......."
    else:
         print "tot # lines to read:", nun_lines_testing,"     ......."
         string_lines="_"+str(nun_lines_testing)+"lines"
   




    path_merge_cluster='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'
    filename="Merged_linkedin-WoS_GS_extra70univ.pickle"
    df_merged = pd.read_pickle(path_merge_cluster+filename)

    print "   done reading"

    aux=df_merged['author_disambig_id_wos'].dropna().tolist()
    lista_authors_merge = [int(x) for x in aux] 



    print "# authors involved:  ",len(lista_authors_merge)



    #### input file (ALL disambiguated WoS)
    path='/home/julia/Dropbox_collaborations/Data/WoS_data/Disambiguated_authors/'
    filename='final.tsv'
    #### tot  number of lines:    34556437
      
        
        
    master_dict_author_id_att={}
    dict_paper_list_authors={}
    dict_author_dict_paper_seq={}
    dict_paper_dict_author_seq={}


    cont=0
    cont_included=0
    with open(path+filename) as f:
        for line in  f: 
#        for line in  tqdm_notebook(f):  # line is a str  #### one line per WOS author      
            line=line.strip("\n")  #author_id	uid	seq	year	author_name	affiliation	total_pubs
    
            if cont >0:
             
               #example:   879592	WOS:000355773000004|WOS:000340362000001	1|1	2015|2014	Barker, J. G.|Barker, John G.	NIST, NIST Ctr Neutron Res, Gaithersburg, MD 20899 USA||NIST, Gaithersburg, MD 20899 USA	2

            
              #  if cont == nun_lines_testing:   
               #       break    
         


                author_id=int(line.split("\t")[0] )
            
            
                if author_id in lista_authors_merge:                                               
            
                    cont_included +=1              
            
                    list_uid=line.split("\t")[1].replace("WOS:","").split("|")  
                              
                
                    seq=line.split("\t")[2].split("|")
                    list_seq=[int(x) for x in seq]       # o-index, also, if -1 means ranking unknown for that particular paper               
 
               
                  #  if -1 in list_seq:
                   #     print list_seq
                    #    raw_input()
    
                
                
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
                    master_dict_author_id_att[author_id]['coauthors']=[]
                   
                    
             
                

            cont +=1
        


    print "# lines read (# authors in WoS file):", cont, "   included (found from merged file):", len(master_dict_author_id_att), cont_included
    print "# papers involved:",len(dict_paper_list_authors)




    for paper_id in dict_paper_list_authors:
        list_coathors_current_paper=dict_paper_list_authors[paper_id]
    
        for author_id in list_coathors_current_paper:
            master_dict_author_id_att[author_id]['coauthors'].extend(list_coathors_current_paper)
    
    
    # i remove redundancy in list of coauthors     
    for author_id in master_dict_author_id_att:             
        master_dict_author_id_att[author_id]['coauthors']=[ x for x in list(set(master_dict_author_id_att[author_id]['coauthors'])) if x != author_id ]  # I REMOVE THE AUTHOR HERSELF FROM THE LIST OF COAUTHORS





    filename_pickle=path_merge_cluster+"master_dict_author_id_att"+string_lines+".pickle"    
    pickle.dump(master_dict_author_id_att, open(filename_pickle, 'wb'))
    print "written:",filename_pickle  



    filename_pickle=path_merge_cluster+"dict_paper_list_authors"+string_lines+".pickle"        
    pickle.dump(dict_paper_list_authors, open(filename_pickle, 'wb'))
    print "written:",filename_pickle  



    filename_pickle=path_merge_cluster+"dict_paper_dict_author_seq"+string_lines+".pickle"        
    pickle.dump(dict_paper_dict_author_seq, open(filename_pickle, 'wb'))
    print "written:",filename_pickle  



    filename_pickle=path_merge_cluster+"dict_author_dict_paper_seq"+string_lines+".pickle"        
    pickle.dump(dict_author_dict_paper_seq, open(filename_pickle, 'wb'))
    print "written:",filename_pickle  
    






    
    
    ######## i create the new field (and i will run it again after refining the dict)
    df_merged['num_coauthors'] = df_merged['author_disambig_id_wos'].fillna('').apply(add_num_coathors,args=[master_dict_author_id_att])
  



    filename_merged="Merged_linkedin-WoS_GS_extra70univ.pickle"

    df_merged.to_pickle(path_merge_cluster+filename_merged.split(".pickle")[0] +"_added_num_coauth"+string_lines+".pickle" )
    print "pickle done:", path_merge_cluster+filename_merged.split(".pickle")[0] +"_added_num_coauth"+string_lines+".pickle"        



    writer = pd.ExcelWriter(path_merge_cluster+filename_merged.split(".pickle")[0] +"_added_num_coauth"+string_lines+".xlsx", engine='xlsxwriter',options={'strings_to_urls': False})
# Convert the dataframe to an XlsxWriter Excel object.
    df_merged.to_excel(writer, sheet_name='Sheet1')
## OJO! hay url muy largas que hacen que el sistema se cuelgue (solucion: no permitirle que las considere url, sino simplemente str)

# Close the Pandas Excel writer and output the Excel file.
    writer.save()

    print "xlsx done",path_merge_cluster+filename_merged.split(".pickle")[0] +"_added_num_coauth"+string_lines+".xlsx"




#########################################
#######################################




def add_num_coathors(wos_id,dicc):    
    
   # print "wos id:",wos_id
   
    num_coathors=np.nan    
   
      
    try:  
        
        wos_id=int(wos_id)
        num_coathors= dicc[wos_id]['coauthors']                  
        return num_coathors
                    
    except:  pass
        
        
        
###############################




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

