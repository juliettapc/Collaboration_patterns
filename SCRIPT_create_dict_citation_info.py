import pandas as pd
import numpy as np
import gzip
import scipy
import operator

try:
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle
    
    
 

def main():



    #string_lines= "_50000lines"     #"_all_lines"  or _50000lines 
    string_lines= "_all_lines"    ###  "_all_lines"  or _50000lines 



    path_merge_cluster='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'
  
 
    file_pickle = open(path_merge_cluster+"list_involved_papers_all_lines.pickle",'rb')
    list_involved_papers = pickle.load(file_pickle)
    set_list_involved_papers=set(list_involved_papers)
    print "# papers involved: " ,len(list_involved_papers)    #2.6 Million




    lista_files=["data_references_IDs_1963.txt.gz","data_references_IDs_1977.txt.gz","data_references_IDs_1991.txt.gz","data_references_IDs_2005.txt.gz",    "data_references_IDs_1950.txt.gz","data_references_IDs_1964.txt.gz","data_references_IDs_1978.txt.gz","data_references_IDs_1992.txt.gz","data_references_IDs_2006.txt.gz",    "data_references_IDs_1951.txt.gz","data_references_IDs_1965.txt.gz","data_references_IDs_1979.txt.gz","data_references_IDs_1993.txt.gz","data_references_IDs_2007.txt.gz",    "data_references_IDs_1952.txt.gz","data_references_IDs_1966.txt.gz","data_references_IDs_1980.txt.gz","data_references_IDs_1994.txt.gz","data_references_IDs_2008.txt.gz",    "data_references_IDs_1953.txt.gz","data_references_IDs_1967.txt.gz","data_references_IDs_1981.txt.gz","data_references_IDs_1995.txt.gz","data_references_IDs_2009.txt.gz",    "data_references_IDs_1954.txt.gz","data_references_IDs_1968.txt.gz","data_references_IDs_1982.txt.gz","data_references_IDs_1996.txt.gz","data_references_IDs_2010.txt.gz",    "data_references_IDs_1955.txt.gz","data_references_IDs_1969.txt.gz","data_references_IDs_1983.txt.gz","data_references_IDs_1997.txt.gz","data_references_IDs_2011.txt.gz",    "data_references_IDs_1956.txt.gz","data_references_IDs_1970.txt.gz","data_references_IDs_1984.txt.gz","data_references_IDs_1998.txt.gz","data_references_IDs_2012.txt.gz",    "data_references_IDs_1957.txt.gz","data_references_IDs_1971.txt.gz","data_references_IDs_1985.txt.gz","data_references_IDs_1999.txt.gz","data_references_IDs_2013.txt.gz",    "data_references_IDs_1958.txt.gz","data_references_IDs_1972.txt.gz","data_references_IDs_1986.txt.gz","data_references_IDs_2000.txt.gz","data_references_IDs_2014.txt.gz",    "data_references_IDs_1959.txt.gz","data_references_IDs_1973.txt.gz","data_references_IDs_1987.txt.gz","data_references_IDs_2001.txt.gz","data_references_IDs_2015.txt.gz",    "data_references_IDs_1960.txt.gz","data_references_IDs_1974.txt.gz","data_references_IDs_1988.txt.gz","data_references_IDs_2002.txt.gz",    "data_references_IDs_1961.txt.gz","data_references_IDs_1975.txt.gz","data_references_IDs_1989.txt.gz","data_references_IDs_2003.txt.gz",    "data_references_IDs_1962.txt.gz","data_references_IDs_1976.txt.gz","data_references_IDs_1990.txt.gz","data_references_IDs_2004.txt.gz"] 

   


    #path="/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/WoS_data/Citation_data/"
    path="/webofscience/diego/WoS_tables/references/paper_ID_ref_IDs/"


    test_lines=1000000000000000



    string_lines="_all_lines"
    if test_lines < 100000000:
         string_lines="_"+str(test_lines)+"lines"


    tot_cont=0
    tot_cont_useful_lines=0
    tot_cont_useful_lines_adding_cit =0       
    
    dict_paper_id_list_papers_that_cite_it={}          


    
        #file_citations="data_references_IDs_1950.txt.gz"   # wc -l         1095263  in 2008              1471208  in 2014  (about the largest file of all)
        
        
    # example:    WOS:000208613900218||WOS:000171098400003;WOS:000078872600001;WOS:000089084800005;WOS:000172993900077;WOS:000224947200006;WOS:000232448400002;000208613900218.2;000208613900218.7;000208613900218.8||
    # paper ||  ref1; ref2;...;refn||

      # with a ref has the form:  000208613900218.2  means that the focus paper (000208613900218) is making a ref. to a paper NOT included in WOS



    for file_citations in  sorted(lista_files):
        print "reading:", file_citations," ........."

        cont=0       
        cont_useful_lines_adding_cit =0
        with gzip.open(path+file_citations,'r') as f:        

             for line in f:            
                cont +=1
                tot_cont +=1
            
              #  if cont == test_lines:
               #     break

          
                lista_line=line.split("||")
                paper=lista_line[0].replace("WOS:","")   # papers are str            
                list_ref=lista_line[1].replace("WOS:","").split(";")

                ref_overlap=list(set(list_ref) & set_list_involved_papers)
                if   len(ref_overlap)>0:
                  
                    cont_useful_lines_adding_cit +=1
                    tot_cont_useful_lines_adding_cit +=1
                
                    for ref in ref_overlap:
                        try:
                            dict_paper_id_list_papers_that_cite_it[ref].append(paper)
                        except KeyError:
                            dict_paper_id_list_papers_that_cite_it[ref]=[]
                            dict_paper_id_list_papers_that_cite_it[ref].append(paper)



        print  "num lines read:", cont, "   with useful info:",cont_useful_lines_adding_cit

    
        filename_pickle=path_merge_cluster+"dict_paper_id_list_papers_that_cite_it"+string_lines+".pickle"      
        pickle.dump(dict_paper_id_list_papers_that_cite_it, open(filename_pickle, 'wb'))
        print "written (updated every year!):",filename_pickle  



        #if cont_useful_lines_adding_cit >0:

         #   list_useful_files.append(file_citations)
        
    print "\n\ndone!"
    print "num lines read:", tot_cont, "   with useful info:",tot_cont_useful_lines_adding_cit

    print "num papers in dict:",len(dict_paper_id_list_papers_that_cite_it)






    filename_pickle=path_merge_cluster+"dict_paper_id_list_papers_that_cite_it"+string_lines+".pickle"      
    pickle.dump(dict_paper_id_list_papers_that_cite_it, open(filename_pickle, 'wb'))
    print "written (updated every year!):",filename_pickle  


    print cont,  cont_useful_lines_adding_cit








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

