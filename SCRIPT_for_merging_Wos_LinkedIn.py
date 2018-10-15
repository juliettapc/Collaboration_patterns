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


    path_wos_linux='/home/julia/Dropbox_collaborations/Data/WoS_data/Disambiguated_authors/'


    string_num_rows=""
    if  number_rows=="All":
       
        df_disamb_wos_test=pd.read_csv(path_wos_linux+'wos_author_disambiguated_2000-2015_USA_processed.tsv', sep="\t")

    else:
        string_num_rows="_"+str(number_rows)
        df_disamb_wos_test=pd.read_csv(path_wos_linux+'wos_author_disambiguated_2000-2015_USA_processed.tsv', sep="\t",nrows= number_rows)


    print "done reading wos file"

    df_disamb_wos_test['full_name'] = df_disamb_wos_test.full_name.apply(convert_unicode_to_string)
    df_disamb_wos_test['firstname'] = df_disamb_wos_test.firstname.apply(convert_unicode_to_string)
    df_disamb_wos_test['middle'] = df_disamb_wos_test.middle.apply(convert_unicode_to_string)
    df_disamb_wos_test['lastname'] = df_disamb_wos_test.lastname.apply(convert_unicode_to_string)


    df_disamb_wos_test['University'] = df_disamb_wos_test.apply(lambda row: row.University.replace(", ",",").replace("[","").replace("]","").split(","), axis=1)

# example:  [University Michigan, University Michigan Hlth Syst]


    path_linkedin_linux='/home/julia/Dropbox_collaborations/Data/Vinu_University_Sheets/Improved_3Feb_and_more_emails_27Feb/All_linkedIn.pickle'
                                                         
    df_linkedin_test=pd.read_pickle(path_linkedin_linux)


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
    #for row in df_linkedin_test.head(100).iterrows():       
        cont +=1

        linkedin_index=row[0]


        if linkedin_index ==100 or linkedin_index ==1000 or   linkedin_index ==5000 or linkedin_index ==10000 or linkedin_index == 50000 :
            print linkedin_index
    
        lista_linkedin_idx.append(linkedin_index)

        master_dict_linkedin_index_wos_index[linkedin_index]=[]
        matching_dict_univ_linkedin_univ_wos={}     


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


             for fila in  select_df_wos_one_lastname.head(5000).iterrows():  # one row per author

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
                    matching_dict_univ_linkedin_univ_wos[univ_linkedin]=(match,  wos_index, score)
                    master_dict_linkedin_index_wos_index[linkedin_index].append(wos_index)   
                
                

                    lista_posibles_wos_index.append(wos_index)   

   
             if len(lista_posibles_wos_index)>1:
                    cont_ambig +=1
        except TypeError:   # for the few empty rows (all Nan)
                pass
    
    
    print "done with the big loop\n"


    print "# of linkedin names with wos ambiguity:", cont_ambig
  
    
#path_merge_win='C:\\Users\\julietta\\Work\\Dropbox_studies\\Data\\Merged_LinkedIn_WoS\\'
    path_merge_linux='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'



 
    filename_pickle=path_merge_linux+"master_dict_linkedin_index_wos_index"+string_num_rows+".pickle"    
    pickle.dump(master_dict_linkedin_index_wos_index, open(filename_pickle, 'wb'))
    print "written:",filename_pickle
 


   

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
    print "size list linkedin idx",len(lista_linkedin_idx), "  unique:", len(set(lista_linkedin_idx))
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




    #list_lastnames_in_wos=list(df_disamb_wos_test.lastname.values)



   # print "# wos lastnames:",len(list_lastnames_in_wos), "  unique:",len(set(list_lastnames_in_wos))



    #print "\noverlap between all wos lastnames and linkedin lastnames not found on wos:", len(list( set(list_lastnames_in_wos)  &   set(list_not_found_linkedin_lastnames)   ))   #  20104    







    filename_output_cluster='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/checking_matcht_LinkedIn_WoS_with_repetitions'+string_num_rows+'.dat'
    #filename_output_redbox='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Merged_LinkedIn_WoS/'

    output=open(filename_output_cluster,'wt')
    
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
    print "written:",filename_output_cluster











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
  
        
#         print linkedin_idx, pickled_master_dict_linkedin_index_wos_index[linkedin_idx]
#         raw_input()
     
    
        cont_merging_idx +=1




    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'firstname':'firstname_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'lastname':'lastname_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'full_namename':'full_name_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'middle':'middle_linkedin'})
    
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'University':'University_linkedin'})


    print "merging dfs........"

    df_merged = pd.merge(linkedin_with_new_column, wos_with_new_column, how='left',on='merging_idx')

    print "done"



    path_merged='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'




    merged_file_name=path_merged+"Merged_linkedin_wos"+string_num_rows+".tsv"    
    df_merged.to_csv(merged_file_name, sep='\t', encoding='utf-8')#, columns = list_headers)
    print "csv done:", merged_file_name


    df_merged.to_pickle(merged_file_name.split(".tsv")[0]+".pickle")
    print "pickle done:" ,merged_file_name.split(".tsv")[0]+".pickle"





    writer = pd.ExcelWriter(path_merged+"Merged_linkedin_wos"+string_num_rows+".xlsx", engine='xlsxwriter',options={'strings_to_urls': False})

# Convert the dataframe to an XlsxWriter Excel object.
    df_merged.to_excel(writer, sheet_name='Sheet1')
# Close the Pandas Excel writer and output the Excel file.
    writer.save()

    print "xlsx done:", path_merged+"Merged_linkedin_wos"+string_num_rows+".xlsx"





    print "Number of unique idx in merged df:",len(df_merged.merging_idx.unique())

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
        
#     print type(cadena), type(lista)
#     raw_input()
     ###   difflib.get_close_print "wos univ:", df_disamb_wos_test.University.unique()matches?   #### to read the manual of sth
    score=0.
    match=None
    
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

#     print "\nbest matching for ", cadena,"is:", match, ",   score:"    , score
#     raw_input()
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
