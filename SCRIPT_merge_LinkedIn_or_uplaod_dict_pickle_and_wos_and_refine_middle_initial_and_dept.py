import pandas as pd
import numpy as np
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
    extra_70univ="yes"   #"yes"



    path_cluster='/home/julia/Dropbox_collaborations/Data/WoS_data/Disambiguated_authors/'
    #path_redbox='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/WoS_data/Disambiguated_authors/'

    string_num_rows=""
    if  number_rows=="All":

        df_disamb_wos_test=pd.read_csv(path_cluster+'wos_author_disambiguated_2000-2015_USA_processed.tsv', sep="\t")

    else:
        string_num_rows="_"+str(number_rows)
        df_disamb_wos_test=pd.read_csv(path_cluster+'wos_author_disambiguated_2000-2015_USA_processed.tsv', sep="\t",nrows= number_rows)

    print "done reading wos file"





    df_disamb_wos_test['full_name'] = df_disamb_wos_test.full_name.apply(convert_unicode_to_string)
    df_disamb_wos_test['firstname'] = df_disamb_wos_test.firstname.apply(convert_unicode_to_string)
    df_disamb_wos_test['middle'] = df_disamb_wos_test.middle.apply(convert_unicode_to_string)
    df_disamb_wos_test['lastname'] = df_disamb_wos_test.lastname.apply(convert_unicode_to_string)


    df_disamb_wos_test['University'] = df_disamb_wos_test.apply(lambda row: row.University.replace(", ",",").replace("[","").replace("]","").split(","), axis=1)
    df_disamb_wos_test['Department'] = df_disamb_wos_test.Department.apply(create_list_dept)





#    path_linkedin_redbox='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Vinu_University_Sheets/Improved_3Feb_and_more_emails_27Feb/'

    path_linkedin_cluster='/home/julia/Dropbox_collaborations/Data/Vinu_University_Sheets/Improved_3Feb_and_more_emails_27Feb/'
 
 
    if extra_70univ=="yes":
        df_linkedin_test=pd.read_pickle(path_linkedin_cluster+'All_linkedIn_complete_plus70univ_without_linkedin.pickle')
    else:
        df_linkedin_test=pd.read_pickle(path_linkedin_cluster+'All_linkedIn_complete.pickle')



    print "done reading linkedin file"

    print "WoS: ",df_disamb_wos_test.shape
    print "LinkedIn: ",df_linkedin_test.shape



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





    df_linkedin_test['School_college'].fillna("NAN", inplace=True)
    df_linkedin_test['Department'].fillna("NAN", inplace=True)  
    df_linkedin_test['middle'].fillna("NAN", inplace=True)

    df_disamb_wos_test['middle'].fillna("NAN", inplace=True)
    df_disamb_wos_test['Department'].fillna("NAN", inplace=True)  





######################  if i already have a dict:
   # path_merge_linux='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'

    #string_fuzzy='NO'

    #if string_fuzzy == "YES":
# filename_pickle=path_merge_linux+"master_dict_linkedin_index_wos_index.pickle"
     #   filename_pickle=path_merge_linux+"master_dict_linkedin_index_wos_index_fuzzy_matching_name_and_univ_threshlod0.95.pickle"
    #else:
     #   filename_pickle=path_merge_linux+"corrected_master_dict_linkedin_index_wos_index_extra_70univ.pickle"



    #master_dict_linkedin_index_wos_index=pd.read_pickle(filename_pickle)
    #print "master dict pickle loaded", len(master_dict_linkedin_index_wos_index)

#############################






    threshold  = 0.9  # to accept a matching of two university names


# given two dataframes, i go over all names in one (linkedin)   and find  matches from the other

    master_dict_linkedin_index_wos_index={}
    cont=0
    print "entering a loop of",len(df_linkedin_test), "iters (linkedin rows)......\n"


    cont_ambig=0
# for row in tqdm_nofull_nametebook(df_linkedin_test.head(5000).iterrows()):       
#for row in df_linkedin_test.head(1000).iterrows():       
    lista_linkedin_idx=[]    
    for row in df_linkedin_test.iterrows():       
        cont +=1

        linkedin_index=row[0]


        if linkedin_index ==100 or linkedin_index ==500 or linkedin_index ==1000 or   linkedin_index ==5000 or linkedin_index ==10000 or linkedin_index == 50000 or linkedin_index ==100000 or linkedin_index == 135000          :
            print linkedin_index

        lista_linkedin_idx.append(linkedin_index)

        master_dict_linkedin_index_wos_index[linkedin_index]=[]


        univ_linkedin=row[1].University    
        lastname_linkedin=row[1].lastname    
        full_name_linkedin=row[1].full_name


        lista_posibles_wos_index=[] 


        try:   # if the whole row is not just NANs    

    #LINKEDIN:   dirty_firstname	dirty_lastname	full_name	firstname	middle	lastname
    #WOS:      firstname	firstname_initial	middle	lastname	list_author_names	University	list_years	full_name


             first_name_linkedin=row[1].firstname


             perfect_selection=df_disamb_wos_test[df_disamb_wos_test.full_name == full_name_linkedin]
             if len( perfect_selection ) ==1:
        #print "perfect match on full name for linkedin_idx", linkedin_index,"  and wos_idx:", perfect_selection.index
        #raw_input()
                select_df_wos_one_lastname = perfect_selection

             else:                      

         ### for a given last name, i only look at the wos rows with the same lastname
                pre_select_df_wos_one_lastname=df_disamb_wos_test[df_disamb_wos_test.lastname == lastname_linkedin]

                if len(pre_select_df_wos_one_lastname)>0:        
                    select_df_wos_one_lastname = pre_select_df_wos_one_lastname[pre_select_df_wos_one_lastname.firstname ==  first_name_linkedin]

            # the selected df keeps the same indices from de original df !!!!!           
            #print "linkedin:", linkedin_index, first_name_linkedin, lastname_linkedin, univ_linkedin


                else:
                    select_df_wos_one_lastname = pre_select_df_wos_one_lastname


#             print "size pre-selection:", len(pre_select_df_wos_one_lastname),  "   size selection:", len(select_df_wos_one_lastname)

#             if len(select_df_wos_one_lastname)>0:
#                 raw_input()


             for fila in  select_df_wos_one_lastname.iterrows():  # one row per author
    
                list_univ_wos=fila[1].University                           
                wos_index=fila[0]



#             print type(univ_linkedin), univ_linkedin
#             print type(list_univ_wos), list_univ_wos
#             raw_input()


                match, score= find_closest_match(univ_linkedin, list_univ_wos)

#             print univ_linkedin, list_univ_wos
#             print score
#             raw_input()


                if score > threshold:  #if the result of the matching is worth considering
                    
                    master_dict_linkedin_index_wos_index[linkedin_index].append(wos_index)   



                    lista_posibles_wos_index.append(wos_index)   


             if len(lista_posibles_wos_index)>1:
                    cont_ambig +=1
        except TypeError:   # for the few empty rows (all Nan)
                pass


    print "done with the big loop\n"


    print "# of linkedin names with wos ambiguity:", cont_ambig





    print "size of the master dict:", len(master_dict_linkedin_index_wos_index)











   




######## i go over the dict again, refining the matches using middle name and department info
    print "going over the dict again, refining the matches using middle name and department info.........."

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
        
            if dept_linkedin == "NAN":
                dept_linkedin=df_linkedin_test.iloc[linkedin_idx].School_college


            try:
                for wos_indx in master_dict_linkedin_index_wos_index[linkedin_idx]:

                    list_dept_wos=df_disamb_wos_test.iloc[wos_indx].Department
                    middle_wos=df_disamb_wos_test.iloc[wos_indx].middle

                    flag_diff_middle=0                                                 
                    if middle_wos is not np.nan   and  middle_wos != "NAN"   and middle_wos != "":
                         if middle_linkedin is not np.nan   and  middle_linkedin != "NAN"    and middle_linkedin != "": 
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

                            corrections_to_master_dict[linkedin_idx]=[wos_indx]        
                            cont_disamb_found +=1
            
            except  IndexError:  # for when i use the full masterr dict but only a sample of Wos
                pass


    try:
        print "# disambig. found:"        , cont_disamb_found, "  out of:", cont_disamb, float(cont_disamb_found)/cont_disamb
    except ZeroDivisionError:
        print "# disambig found:"        , cont_disamb_found, "  out of:", cont_disamb
      


# In[ ]:

#path_merge_win='C:\\Users\\julietta\\Work\\Dropbox_studies\\Data\\Merged_LinkedIn_WoS\\'
    #path_merge_redbox='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/'

    path_merge_cluster='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'

   

    if extra_70univ=="yes":
        filename_pickle=path_merge_cluster+"corrected_master_dict_linkedin_index_wos_index"+string_num_rows+"_extra_70univ.pickle" 
    else:
        filename_pickle=path_merge_cluster+"corrected_master_dict_linkedin_index_wos_index"+string_num_rows+".pickle" 


    pickle.dump(corrections_to_master_dict, open(filename_pickle, 'wb'))
    print "written:",filename_pickle
    
    





    ##### i reasign
    master_dict_linkedin_index_wos_index=corrections_to_master_dict


    #print "linkedin_idx  wos_idx"
    cont_found=0
    cont_ambiguedad=0
    cont_no_match=0
    for llave in master_dict_linkedin_index_wos_index:
        if len(master_dict_linkedin_index_wos_index[llave]) >0:
            #print llave, master_dict_linkedin_index_wos_index[llave]
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
 

    if extra_70univ=="yes":
        filename_output_cluster='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/checking_matcht_LinkedIn_WoS'+string_num_rows+'_corrected_dict'+string_num_rows+'_extra70_univ_.dat'
    else:
        filename_output_cluster='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/checking_matcht_LinkedIn_WoS'+string_num_rows+'_corrected_dict'+string_num_rows+'.dat'

    output=open(filename_output_cluster,'wt')

    for linkedin_idx in master_dict_linkedin_index_wos_index:

   
        if len(master_dict_linkedin_index_wos_index[linkedin_idx])>=1:        
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
                print "PROBLEMS printing out :", linkedin_idx, "for checking"#df_linkedin_test.iloc[linkedin_idx],""
            
            
            
            
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

