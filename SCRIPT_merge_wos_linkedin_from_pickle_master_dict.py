
# coding: utf-8

# In[2]:

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


    flag_extra_70="yes"   


    path_wos_linux='/home/julia/Dropbox_collaborations/Data/WoS_data/Disambiguated_authors/'
    df_disamb_wos_test=pd.read_csv(path_wos_linux+'wos_author_disambiguated_2000-2015_USA_processed.tsv', sep="\t")
    print "done reading Wos file"


    df_disamb_wos_test['full_name'] = df_disamb_wos_test.full_name.apply(convert_unicode_to_string)
    df_disamb_wos_test['firstname'] = df_disamb_wos_test.firstname.apply(convert_unicode_to_string)
    df_disamb_wos_test['middle'] = df_disamb_wos_test.middle.apply(convert_unicode_to_string)
    df_disamb_wos_test['lastname'] = df_disamb_wos_test.lastname.apply(convert_unicode_to_string)
    df_disamb_wos_test['University'] = df_disamb_wos_test.apply(lambda row: row.University.replace(", ",",").replace("[","").replace("]","").split(","), axis=1)



    if  flag_extra_70=="yes":
        path_linkedin_linux="/home/julia/Dropbox_collaborations/Data/Vinu_University_Sheets/Improved_3Feb_and_more_emails_27Feb/All_linkedIn_complete_plus70univ_without_linkedin.pickle"
    else:
        path_linkedin_linux="/home/julia/Dropbox_collaborations/Data/Vinu_University_Sheets/Improved_3Feb_and_more_emails_27Feb/All_linkedIn_complete.pickle"

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



    path_merge_linux='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'
    if  flag_extra_70=="yes":
        filename_pickle=path_merge_linux+"corrected_master_dict_linkedin_index_wos_index_extra_70univ.pickle"
    else:
        filename_pickle=path_merge_linux+"corrected_master_dict_linkedin_index_wos_index.pickle"
    master_dict_linkedin_index_wos_index=pd.read_pickle(filename_pickle)



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
    
  






    wos_with_new_column=df_disamb_wos_test.copy()
    linkedin_with_new_column=df_linkedin_test.copy()




    wos_with_new_column=wos_with_new_column.assign(merging_idx=np.nan)

    linkedin_with_new_column=linkedin_with_new_column.assign(merging_idx=np.nan)





    print "searching for merging_indices...."


    cont_merging_idx=0
    for linkedin_idx in master_dict_linkedin_index_wos_index:
    
        try:
            wos_idx=master_dict_linkedin_index_wos_index[linkedin_idx][0] # OJO!!! for now i only consider one of the potentialy multiple wos_idx associated to a given linkedin idx
            wos_with_new_column.set_value(wos_idx, 'merging_idx',int(cont_merging_idx) )
    #     df.set_value('C', 'x', 10)     where:   index=['A','B','C']  and columns=['x','y']
            linkedin_with_new_column.set_value(linkedin_idx, 'merging_idx', int(cont_merging_idx) )
  
        
        
        except IndexError:
            linkedin_with_new_column.set_value(linkedin_idx, 'merging_idx', 999999999 )
    
    
        cont_merging_idx +=1

    
    
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'firstname':'firstname_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'lastname':'lastname_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'full_namename':'full_name_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'middle':'middle_linkedin'})
    linkedin_with_new_column=linkedin_with_new_column.rename(columns = {'University':'University_linkedin'})




    print "merging dataframes....."

    df_merged = pd.merge(linkedin_with_new_column, wos_with_new_column, how='left',on='merging_idx')





    path_merged='/home/julia/Dropbox_collaborations/Data/Merged_LinkedIn_WoS/'
    if  flag_extra_70=="yes":
        merged_file_name=path_merged+"Merged_linkedin_wos_from_corrected_dict_extra70_univ.tsv"
    else:
        merged_file_name=path_merged+"Merged_linkedin_wos_from_corrected_dict.tsv"
    df_merged.to_csv(merged_file_name, sep='\t', encoding='utf-8')#, columns = list_headers)
    print "csv done:", merged_file_name


    if  flag_extra_70=="yes":
        namefile=path_merged+"Merged_linkedin_wos_from_corrected_dict_extra70_univ.xlsx"
    else:
        namefile=path_merged+"Merged_linkedin_wos_from_corrected_dict.xlsx"
    


    writer = pd.ExcelWriter(namefile, engine='xlsxwriter',options={'strings_to_urls': False})  
# Convert the dataframe to an XlsxWriter Excel object.
    df_merged.to_excel(writer, sheet_name='Sheet1')
# Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print "xlsx done:",namefile





    df_merged.to_pickle(merged_file_name.split(".tsv")[0]+".pickle")
    print "pickle done:"  ,merged_file_name.split(".tsv")[0]




##################################
##############################



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
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "



############################3
#################################
