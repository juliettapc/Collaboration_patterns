
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
   
    threshold  = 0.95  # to accept a matching of two university names
    



   
    path_wos_linux='/home/julia/Dropbox_collaborations/Data/WoS_data/Disambiguated_authors/'


    string_num_rows=""
    if  number_rows=="All":
       
        df_disamb_wos_test=pd.read_csv(path_wos_linux+'wos_author_disambiguated_2000-2015_USA_processed.tsv', sep="\t")

    else:
        string_num_rows="_"+str(number_rows)
        df_disamb_wos_test=pd.read_csv(path_wos_linux+'wos_author_disambiguated_2000-2015_USA_processed.tsv', sep="\t",nrows= number_rows)    

    print "done reading WoS file"




    df_disamb_wos_test['full_name'] = df_disamb_wos_test.full_name.apply(convert_unicode_to_string)
    df_disamb_wos_test['firstname'] = df_disamb_wos_test.firstname.apply(convert_unicode_to_string)
    df_disamb_wos_test['middle'] = df_disamb_wos_test.middle.apply(convert_unicode_to_string)
    df_disamb_wos_test['lastname'] = df_disamb_wos_test.lastname.apply(convert_unicode_to_string)
    df_disamb_wos_test['University'] = df_disamb_wos_test.University.apply(convert_unicode_to_string)


    df_disamb_wos_test['University'] = df_disamb_wos_test.apply(lambda row: row.University.replace(", ",",").replace("[","").replace("]","").split(","), axis=1)

  
    path_linkedin_linux='/home/julia/Dropbox_collaborations/Data/Vinu_University_Sheets/Improved_3Feb_and_more_emails_27Feb/All_linkedIn.pickle'

    df_linkedin_test=pd.read_pickle(path_linkedin_linux)


    print "done reading LinkedIn file"

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
    
    
    
    
    df_linkedin_test['Name_and_Univ'] = df_linkedin_test.apply(lambda row: row.full_name + " "+ row.University, axis=1)



    print "WoS: ",df_disamb_wos_test.shape
    print "LinkedIn: ",df_linkedin_test.shape


 
# given two dataframes, i go over all names in one (linkedin)   and find  matches from the other

    master_dict_linkedin_index_wos_index={}
    cont=0
    print "entering a loop of",len(df_linkedin_test), "iters (linkedin rows)......\n"


    cont_ambig=0
# for row in tqdm_nofull_nametebook(df_linkedin_test.head(5000).iterrows()):       
#for row in df_linkedin_test.head(1000).iterrows():       
    lista_linkedin_idx=[]
#for row in tqdm_notebook(df_linkedin_test.head(5000).iterrows()):       
    for row in df_linkedin_test.iterrows():       
        cont +=1

        linkedin_index=row[0]
       #print (cont, linkedin_index)

        if linkedin_index ==100 or linkedin_index ==1000 or   linkedin_index ==5000 or linkedin_index ==10000 or linkedin_index ==20000 or linkedin_index == 50000 or linkedin_index == 80000 :
            print linkedin_index



        lista_linkedin_idx.append(linkedin_index)

        master_dict_linkedin_index_wos_index[linkedin_index]=[]
        matching_dict_univ_linkedin_univ_wos={}     


        univ_linkedin=row[1].University    
        lastname_linkedin=row[1].lastname    
        full_name_linkedin=row[1].full_name

        name_and_univ_linkedin=row[1].Name_and_Univ
    
        lista_posibles_wos_index=[] 


        try:   # if the whole row is not just NANs    

        #LINKEDIN:   dirty_firstname	dirty_lastname	full_name	firstname	middle	lastname
        #WOS:      firstname	firstname_initial	middle	lastname	list_author_names	University	list_years	full_name
        
      
            select_df_wos_one_lastname=df_disamb_wos_test[df_disamb_wos_test.lastname == lastname_linkedin]                        

#         print name_and_univ_linkedin, "        # potential matches by lastname:",len(select_df_wos_one_lastname)
            for fila in  select_df_wos_one_lastname.iterrows():  # one row per author

                    list_univ_wos=fila[1].University
                    full_name_wos=fila[1].full_name
            
                    wos_index=fila[0]                       
            
                    match, score= find_closest_match(name_and_univ_linkedin, list_univ_wos, full_name_wos)


                    if score > threshold:  #if the result of the matching is worth considering
                
                        master_dict_linkedin_index_wos_index[linkedin_index].append(wos_index)                                   
                        lista_posibles_wos_index.append(wos_index)   
#                         print "\nbest matching for:    ", name_and_univ_linkedin,"           is:", match, "       score:"    , score
#                     raw_input()



    #      print (lista_posibles_wos_index)
            if len(lista_posibles_wos_index)>1:
                    cont_ambig +=1
        except TypeError:   # for the few empty rows (all Nan)
                pass
    
    
    print "done"
 
#     print type(cadena_name_and_univ), type(list_univ_wos), type(cadena_full_name_wos)

    print "# of linkedin names with wos ambiguity:", cont_ambig
 
    path_merge_linux='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'


    filename_pickle=path_merge_linux+"master_dict_linkedin_index_wos_index_fuzzy_matching_name_and_univ"+string_num_rows+"_threshlod"+str(threshold)+".pickle"
    pickle.dump(master_dict_linkedin_index_wos_index, open(filename_pickle, 'wb'))
    



    print "linkedin  wos"
    cont_found=0
    cont_ambiguedad=0
    cont_no_match=0
    for llave in master_dict_linkedin_index_wos_index:
       if len(master_dict_linkedin_index_wos_index[llave]) >0:
       #print (llave, master_dict_linkedin_index_wos_index[llave])
           cont_found +=1
           if len(master_dict_linkedin_index_wos_index[llave]) >1:
               cont_ambiguedad +=1
       else:
           cont_no_match +=1
       
    print "# linkedin names: ",len(master_dict_linkedin_index_wos_index)
    print "  # linkedin authors found: ", cont_found
    print "      # linkedin authors found but with ambiguity: ", cont_ambiguedad
    print "  # link.firstname_or_initialedin authors NOT found: ", cont_no_match
    print "\n"
   
    print "size list linkedin idx",len(lista_linkedin_idx), "  unique:", len(set(lista_linkedin_idx))







    filename_output='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/checking_fuzzy_matcht_LinkedIn_WoS_with_repetitions_threshold'+str(threshold)+"_nrows"+string_num_rows+'.dat'
    output=open(filename_output,'wt')

    for linkedin_idx in master_dict_linkedin_index_wos_index:

   
        if len(master_dict_linkedin_index_wos_index[linkedin_idx])>1:        
            print >> output, "\n\nLINKEDIN idx:",linkedin_idx, "  ",df_linkedin_test.iloc[linkedin_idx].full_name.title() ," || ", df_linkedin_test.iloc[linkedin_idx].Current_Title," || ", df_linkedin_test.iloc[linkedin_idx].University," || ", df_linkedin_test.iloc[linkedin_idx].Department
            print >> output ,""


            for wos_indx in master_dict_linkedin_index_wos_index[linkedin_idx]:
   
                print >> output , "  ---wos_idx:", wos_indx
                print >> output ,"  ", df_disamb_wos_test.iloc[wos_indx].full_name
                print >> output ,"  ",df_disamb_wos_test.iloc[wos_indx].University
                print >> output ,"  ", df_disamb_wos_test.iloc[wos_indx].Department
                print >> output ,"  ",df_disamb_wos_test.iloc[wos_indx].total_pubs , "publ"
                print >> output ,"  ",df_disamb_wos_test.iloc[wos_indx].year
    output.close()                    
    print "written:",filename_output       











    print len(master_dict_linkedin_index_wos_index)

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
    



 #   linkedin_idx=393




#for wos_indx in master_dict_linkedin_index_wos_index[linkedin_idx]:
 #   print "-----",df_disamb_wos_test.iloc[wos_indx]
    
    
#print 
#print df_linkedin_test.iloc[linkedin_idx]


# In[ ]:

# df_disamb_wos_test.iloc[6358]


# In[ ]:

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





    wos_with_new_column=df_disamb_wos_test.copy()
    linkedin_with_new_column=df_linkedin_test.copy()





    wos_with_new_column=wos_with_new_column.assign(merging_idx=np.nan)

    linkedin_with_new_column=linkedin_with_new_column.assign(merging_idx=np.nan)


    cont_merging_idx=0
    for linkedin_idx in master_dict_linkedin_index_wos_index:
    
        try:
            wos_idx=master_dict_linkedin_index_wos_index[linkedin_idx][0] # OJO!!! for now i only consider one of the potentialy multiple wos_idx associated to a given linkedin idx
            wos_with_new_column.set_value(wos_idx, 'merging_idx',int(cont_merging_idx) )
    # df.set_value('C', 'x', 10)     where:   index=['A','B','C']  and columns=['x','y']
            linkedin_with_new_column.set_value(linkedin_idx, 'merging_idx', int(cont_merging_idx) )
  
        
        
        except IndexError:
            linkedin_with_new_column.set_value(linkedin_idx, 'merging_idx', 999999999 )
     
        cont_merging_idx +=1



    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'firstname':'firstname_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'lastname':'lastname_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'full_namename':'full_name_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'middle':'middle_linkedin'})

    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'University':'University_linkedin'})




    df_merged = pd.merge(linkedin_with_new_column, wos_with_new_column, how='left',on='merging_idx')



    path_merged='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'

    merged_file_name=path_merged+"Merged_linkedin-wos_fuzzy_matching_name_and_univ"+string_num_rows+"_threshlod"+str(threshold)+".tsv"

    df_merged.to_csv(merged_file_name, sep='\t', encoding='utf-8')#, columns = list_headers)
    print "tsv done:", path_merged+"Merged_linkedin-wos_fuzzy_matching_name_and_univ"+string_num_rows+"_threshlod"+str(threshold)+".tsv"



    df_merged.to_pickle(merged_file_name.split(".tsv")[0]+".pickle" )
    print "pickle done ", merged_file_name.split(".tsv")[0]+".pickle" 




    writer = pd.ExcelWriter(path_merged+"Merged_linkedin-wos_fuzzy_matching_name_and_unvi"+string_num_rows+"_threshlod"+str(threshold)+".xlsx", engine='xlsxwriter',options={'strings_to_urls': False})

    # Convert the dataframe to an XlsxWriter Excel object.
    df_merged.to_excel(writer, sheet_name='Sheet1')
# Close the Pandas Excel writer and output the Excel file.
    writer.save()





    print "xlsx done:",path_merged+"Merged_linkedin-wos_fuzzy_matching_name_and_unvi"+string_num_rows+"_threshlod"+str(threshold)+".xlsx" 



######################################
######################################

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



######################################
######################################


def find_closest_match(cadena_name_and_univ, list_univ_wos, cadena_full_name_wos):    
    
    
     #difflib.get_close_matches(a,b,3)   # this one gets you as many close matches as you want, in descending order of matching
        
#     print cadena_name_and_univ, list_univ_wos, cadena_full_name_wos    
#     print type(cadena_name_and_univ), type(list_univ_wos), type(cadena_full_name_wos)
#     raw_input()
     ###   difflib.get_close_print "wos univ:", df_disamb_wos_test.University.unique()matches?   #### to read the manual of sth
    
    
    score=0.
    match=None
    
    a=cadena_name_and_univ.lower()
    lista=list_univ_wos
    dict_index_score={}
    for i in range(len(lista)):
    
        b=(cadena_full_name_wos + " " + lista[i]).lower()
        score = difflib.SequenceMatcher(None,a, b).ratio()  
        dict_index_score[i]=score

  
    sorted_dict = sorted(dict_index_score.items(), key=lambda x: x[1],reverse=True) # SORT DICT BY VALUE, IN DESCENDING ORDER     print "sorted dictsorted_dict",sorted_dict ## [(3, 0.9285714285714286), (6, 0.7586206896551724), (0, 0.6896551724137931), (5, 0.37037037037037035), (2, 0.35714285714285715), (4, 0.35714285714285715), (1, 0.23076923076923078)]

    match=(cadena_full_name_wos + " " + lista[sorted_dict[0][0]]).lower()
    index=sorted_dict[0][0]
    score=sorted_dict[0][1]

   
    return match, score



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
