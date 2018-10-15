
#

import pandas as pd
import numpy as np
from tqdm import tqdm
from tqdm import tnrange, tqdm_notebook
from time import sleep
import difflib
import scipy
import operator
import difflib
try:
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle
    
import unicodedata
    
 

def main():

    number_rows="All" # or 1000000


    path_cluster='/home/julia/Dropbox_collaborations/Data/WoS_data/Disambiguated_authors/'
    #path_redbox='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/WoS_data/Disambiguated_authors/'

    string_num_rows=""
    if  number_rows=="All":

        df_disamb_wos_test=pd.read_csv(path_cluster+'wos_author_disambiguated_2000-2015_USA_processed.tsv', sep="\t")

    else:
        string_num_rows="_"+str(number_rows)
        df_disamb_wos_test=pd.read_csv(path_cluster+'wos_author_disambiguated_2000-2015_USA_processed.tsv', sep="\t",nrows= number_rows)


    print "done reading wos file"


# In[38]:

# In[39]:


    df_disamb_wos_test['full_name'] = df_disamb_wos_test.full_name.apply(convert_unicode_to_string)
    df_disamb_wos_test['firstname'] = df_disamb_wos_test.firstname.apply(convert_unicode_to_string)
    df_disamb_wos_test['middle'] = df_disamb_wos_test.middle.apply(convert_unicode_to_string)
    df_disamb_wos_test['lastname'] = df_disamb_wos_test.lastname.apply(convert_unicode_to_string)


    df_disamb_wos_test['University'] = df_disamb_wos_test.apply(lambda row: row.University.replace(", ",",").replace("[","").replace("]","").split(","), axis=1)
    df_disamb_wos_test['Department'] = df_disamb_wos_test.Department.apply(create_list_dept)



# example:  [University Michigan, University Michigan Hlth Syst]


# In[19]:

# df_disamb_wos_test['Department'].iloc[112]


# In[42]:

#    path_linkedin_redbox='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Vinu_University_Sheets/Improved_3Feb_and_more_emails_27Feb/'

    path_linkedin_cluster='/home/julia/Dropbox_collaborations/Data/Vinu_University_Sheets/Improved_3Feb_and_more_emails_27Feb/'
 
    df_linkedin_test=pd.read_pickle(path_linkedin_cluster+'All_linkedIn.pickle')


    print "done reading linkedin file"

    df_linkedin_test = df_linkedin_test.rename(columns={'Department(s)': 'Department', 'School/college': 'School_college'})




    df_linkedin_test['full_name'] = df_linkedin_test.full_name.apply(convert_unicode_to_string)
    df_linkedin_test['firstname'] = df_linkedin_test.firstname.apply(convert_unicode_to_string)
    df_linkedin_test['middle'] = df_linkedin_test.middle.apply(convert_unicode_to_string)
    df_linkedin_test['lastname'] = df_linkedin_test.lastname.apply(convert_unicode_to_string)
    df_linkedin_test['dirty_firstname'] = df_linkedin_test.dirty_firstname.apply(convert_unicode_to_string)
    df_linkedin_test['dirty_lastname'] = df_linkedin_test.dirty_lastname.apply(convert_unicode_to_string)

    df_linkedin_test['University'] = df_linkedin_test.University.apply(convert_unicode_to_string)
    df_linkedin_test['Department'] = df_linkedin_test.Department.apply(convert_unicode_to_string)
    df_linkedin_test['School_college'] = df_linkedin_test.School_college.apply(convert_unicode_to_string)



    print "WoS: ",df_disamb_wos_test.shape
    print "LinkedIn: ",df_linkedin_test.shape



# In[110]:

    df_linkedin_test['Department'].fillna("NAN", inplace=True)
    df_disamb_wos_test['Department'].fillna("NAN", inplace=True)



    df_linkedin_test['middle'].fillna("NAN", inplace=True)
    df_disamb_wos_test['middle'].fillna("NAN", inplace=True)




# In[116]:

    path_merge_linux='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'


    string_fuzzy='NO'


    if string_fuzzy == "YES":
# filename_pickle=path_merge_linux+"master_dict_linkedin_index_wos_index.pickle"
        filename_pickle=path_merge_linux+"master_dict_linkedin_index_wos_index_fuzzy_matching_name_and_univ_threshlod0.95.pickle"
    else:
         filename_pickle=path_merge_linux+"master_dict_linkedin_index_wos_index_exact_match_name_lastname.pickle"



    master_dict_linkedin_index_wos_index=pd.read_pickle(filename_pickle)
    print len(master_dict_linkedin_index_wos_index)




######## i go over the dict again, refining the matches using middle name and department info

    threshold_dept=0.5


    corrections_to_master_dict={}

    cont_disamb_found =0
    cont_disamb =0


    for linkedin_idx in master_dict_linkedin_index_wos_index:
    
    
        corrections_to_master_dict[linkedin_idx]=master_dict_linkedin_index_wos_index[linkedin_idx]
                    
    
        if len(master_dict_linkedin_index_wos_index[linkedin_idx]) > 1:
        
            cont_disamb +=1
            dept_linkedin=df_linkedin_test.iloc[linkedin_idx].Department
            middle_linkedin=df_linkedin_test.iloc[linkedin_idx].middle
        
            try:
                for wos_indx in master_dict_linkedin_index_wos_index[linkedin_idx]:


                    list_dept_wos=df_disamb_wos_test.iloc[wos_indx].Department
                    middle_wos=df_disamb_wos_test.iloc[wos_indx].middle

                    flag_diff_middle=0                                                 
                    if middle_wos != np.nan and  middle_wos != "NAN" and middle_wos != "":
                         if middle_linkedin != np.nan and  middle_linkedin != "NAN" and middle_linkedin != "":                
                            if middle_linkedin != middle_wos:
                                flag_diff_middle=1
                           
                            
                           
                        
                        
                            ####### for examples like:      stylianos <type 'str'>       s <type 'str'>
                            if len(middle_wos)== 1    and    len(middle_linkedin) > 1:
                                    if middle_wos[0] == middle_linkedin[0]:
                                        flag_diff_middle=0     
                                    
                            elif len(middle_linkedin)== 1    and    len(middle_wos) > 1:
                                    if middle_wos[0] == middle_linkedin[0]:
                                        flag_diff_middle=0        
                                    
#                             if flag_diff_middle ==1:
#                                  print middle_linkedin, type(middle_linkedin),"     ", middle_wos ,type(middle_wos)
                
                         
                
                    if flag_diff_middle ==0:
                
                        match, score = find_closest_match(dept_linkedin, list_dept_wos)

                        if score >= threshold_dept:
                           # print "\n\n\n",linkedin_idx, master_dict_linkedin_index_wos_index[linkedin_idx]
                            #print "LINKEDIN:   ",df_linkedin_test.iloc[linkedin_idx].full_name, " ", df_linkedin_test.iloc[linkedin_idx].Department, " ", df_linkedin_test.iloc[linkedin_idx].University,"\n"
                            #print "----", wos_indx, df_disamb_wos_test.iloc[wos_indx].full_name, " ",df_disamb_wos_test.iloc[wos_indx].Department, " ",df_disamb_wos_test.iloc[wos_indx].University


                            #print dept_linkedin,"    ", match
                            #raw_input()


                            corrections_to_master_dict[linkedin_idx]=[wos_indx]                                                            
                            cont_disamb_found +=1
            
            except  IndexError:  # for when i use the full masterr dict but only a sample of Wos
                pass

    print "# matches found:"        , cont_disamb_found, "  out of:", cont_disamb, float(cont_disamb_found)/cont_disamb
      


# In[ ]:

#path_merge_win='C:\\Users\\julietta\\Work\\Dropbox_studies\\Data\\Merged_LinkedIn_WoS\\'
    #path_merge_redbox='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/'

    path_merge_cluster='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'


    filename_pickle=path_merge_cluster+"corrected_master_dict_linkedin_index_wos_index"+string_num_rows+".pickle"    
    pickle.dump(corrections_to_master_dict, open(filename_pickle, 'wb'))
    print "written:",filename_pickle
    
    

# In[83]:

    master_dict_linkedin_index_wos_index=corrections_to_master_dict


    print "linkedin_idx  wos_idx"
    cont_found=0
    cont_ambiguedad=0
    cont_no_match=0
    for llave in master_dict_linkedin_index_wos_index:
        if len(master_dict_linkedin_index_wos_index[llave]) >0:
            print llave, master_dict_linkedin_index_wos_index[llave]
            cont_found +=1
            if len(master_dict_linkedin_index_wos_index[llave]) >1:
                cont_ambiguedad +=1 
        else:
            cont_no_match +=1

    print "numb linkedin names: ",len(master_dict_linkedin_index_wos_index)
    print "  numb. linkedin authors found: ", cont_found
    print "      numb. linkedin authors found but with ambiguity: ", cont_ambiguedad
    print "  numb. linkedin authors NOT found: ", cont_no_match
    print 
    #print "size list linkedin idx",len(lista_linkedin_idx), "  unique:", len(set(lista_linkedin_idx))
    print "size master dict:",len(master_dict_linkedin_index_wos_index)





    list_not_found_linkedin_lastnames=[]
    list_found_linkedin_lastnames=[]
    for linkedin_idx in master_dict_linkedin_index_wos_index:
#print linkedin_idx, pickled_master_dict_linkedin_index_wos_index[linkedin_idx]
        if len(master_dict_linkedin_index_wos_index[linkedin_idx]) == 0:
            list_not_found_linkedin_lastnames.append(df_linkedin_test.iloc[linkedin_idx].lastname)
        else:
            list_found_linkedin_lastnames.append(df_linkedin_test.iloc[linkedin_idx].lastname)


    print "tot # names on linkedin", len(master_dict_linkedin_index_wos_index)   # 81444
    print "# linkedin lastnmes NOT found on wos:",len(list_not_found_linkedin_lastnames), "  unique:",len(set(list_not_found_linkedin_lastnames))  #    48840   unique: 29070  
    print "# linkedin lastnames found on wos:",len(list_found_linkedin_lastnames), "  unique:",len(set(list_found_linkedin_lastnames))   #  32604   unique: 18840 




    list_lastnames_in_wos=list(df_disamb_wos_test.lastname.values)



    print "# wos lastnames:",len(list_lastnames_in_wos), "  unique:",len(set(list_lastnames_in_wos))



    print "\noverlap between all wos lastnames and linkedin lastnames not found on wos:", len(list( set(list_lastnames_in_wos)  &   set(list_not_found_linkedin_lastnames)   ))   #  20104    




# In[ ]:


#filename_output='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/checking_fuzzy_matcht_LinkedIn_WoS_with_repetitions.dat'
    #filename_output_redbox='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/checking_matcht_LinkedIn_WoS'+string_num_rows+'_ONE_name_0.9.dat'
    filename_output_cluster='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/checking_matcht_LinkedIn_WoS_'+string_num_rows+'_corrected_dict'+string_num_rows+'.dat'
    output=open(filename_output_cluster,'wt')

    for linkedin_idx in master_dict_linkedin_index_wos_index:

   
    #if len(master_dict_linkedin_index_wos_index[linkedin_idx])==1:        
            try:
                print >> output, "\n\nLINKEDIN idx:",linkedin_idx, "  ",df_linkedin_test.iloc[linkedin_idx].full_name.title() ," || ", df_linkedin_test.iloc[linkedin_idx].Current_Title," || ", df_linkedin_test.iloc[linkedin_idx].University," || ", df_linkedin_test.iloc[linkedin_idx].Department
        
                print >> output ,""


                for wos_indx in master_dict_linkedin_index_wos_index[linkedin_idx]:
   
                    print >> output , "  ---wos_idx:", wos_indx
                    print >> output ,"  ", df_disamb_wos_test.iloc[wos_indx].full_name
                    print >> output ,"  ",df_disamb_wos_test.iloc[wos_indx].University
                    print >> output ,"  ", df_disamb_wos_test.iloc[wos_indx].Department
                    print >> output ,"  ",df_disamb_wos_test.iloc[wos_indx].total_pubs , "publ"
                    print >> output ,"  ",df_disamb_wos_test.iloc[wos_indx].year
            
            except :
                print "PROBLEMS WITH:", linkedin_idx#df_linkedin_test.iloc[linkedin_idx]
            
            
            
            
    output.close()
    print "written:",filename_output_cluster







# In[ ]:






################

def convert_unicode_to_string(old_cadena):
    
    
    try:
        
        new_cadena=unicodedata.normalize('NFKD', old_cadena).encode('ascii','ignore')
#         print old_cadena,type(old_cadena)
#         print new_cadena,type(new_cadena)
#         raw_input()
        return new_cadena
    except TypeError:  # if it is a string already
#         print type(old_cadena)
#         print old_cadena
#         raw_input()
        return old_cadena



############################

def find_closest_match(cadena, lista):
      #difflib.get_close_matches(a,b,3)   # this one gets you as many close matches as you want, in descending order of matching
    ###   difflib.get_close_print "wos univ:", df_disamb_wos_test.University.unique()matches?   #### to read the manual of sth   
        
#     print cadena, lista    
#     print type(cadena), type(lista)
#     raw_input()


    score=0.
    match=None
    
    try:  # except when there is a NAN (which does not have a len())
        
        a=cadena
        dict_index_score={}
        
        for i in range(len(lista)):    
            b=lista[i]
            score = difflib.SequenceMatcher(None,a, b).ratio()  
            dict_index_score[i]=score

  
        sorted_dict = sorted(dict_index_score.items(), key=lambda x: x[1],reverse=True) # SORT DICT BY VALUE, IN DESCENDING ORDER     print "sorted dictsorted_dict",sorted_dict ## [(3, 0.9285714285714286), (6, 0.7586206896551724), (0, 0.6896551724137931), (5, 0.37037037037037035), (2, 0.35714285714285715), (4, 0.35714285714285715), (1, 0.23076923076923078)]

        match=lista[sorted_dict[0][0]]
        index=sorted_dict[0][0]
        score=sorted_dict[0][1]                                                                        

#         print "\nbest matching for ", cadena,"is:", match, ",   score:"    , score
#         raw_input()
        
    except TypeError:
        pass

    return match, score
        
        
######################



def create_list_dept(string):
    
    new_string=None
    try:
        
        new_string=string.replace(", ",",").replace("[","").replace("]","").split(",")
    except AttributeError:  # except for nan 
        pass
    
    return new_string



# In[37]:



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

