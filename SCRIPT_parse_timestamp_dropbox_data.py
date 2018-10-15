import matplotlib.pyplot as plt   
import pandas as pd
import random
import numpy as np
from tqdm import tqdm
from tqdm import tnrange, tqdm_notebook
from time import sleep
import scipy
import operator
import difflib
import math


try:
    import cPickle as pickle  ##################################
   #it is faster than pickle!
except:
    import pickle
    
import unicodedata
import networkx as nx
import itertools
import seaborn as sns   ### https://seaborn.pydata.org/tutorial/categorical.html
import time  






    

def main():  
  



    
    header_names = ['folder_id','num_members','folder_creation_date','last_date_DO_NOT_TRUST','user_id','email','num_adds','num_edits','num_dels', 'major_content_type','major_file_ext','date','field','new_group_total_pubs','new_group_num_papers_last','new_group_num_citations']
    
    print "reading file .........."

    path = "/home/julia/Dropbox_collaborations/Data/Dropbox/"#/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/Dropbox/"
    input_file = 'results_nico2.csv'


    df = pd.read_csv(path+input_file, sep=',',na_values=["NAN","-1","null"],low_memory=False,header=None, names=header_names,   parse_dates=[2,]) # set header=0 if i wanna pass it my own list of header names   , usecols=[0,1,2,4,5,6,7,8,11,12,13,14,15]

    df.drop('last_date_DO_NOT_TRUST', axis=1)



    print len(df.folder_id.unique()) , "unique folders"#  128080 users,     79565  folders
    print len(df.user_id.unique()) , "unique users"    
    print df.shape   #  1403349, 38 



    df=df.drop_duplicates()  # i have dropped them from the shell already
    print "\n\nafter dropping:"
    print df.shape 

    print len(df.folder_id.unique()) , "unique folders"#  128080 users,     79565  folders
    print len(df.user_id.unique()) , "unique users"
    


    new_file=path+input_file.replace(".csv","")+"_no_duplicates.csv"
    df.to_csv(new_file, sep=',')
    print "written:", new_file,"\n\n\n"







    #to get rid of the cumulative countings and redundant rows without new info, and get actual new activity counts for each date

    
   #   df_filtered = pd.DataFrame(columns=header_names)    
   #   cont_tot=0
    #  cont_selection=0
    #  cont_users=0
 #     tot_num_users=len(df.user_id.unique())
  #    for user_id in df['user_id'].unique():   #tqdm_notebook(df['user_id'].unique()):
      
     #     df_selection_user= df[df['user_id'] == user_id]
    
    #      for folder_id in df_selection_user['folder_id'].unique():
        
         #     df_sub_selection =  df_selection_user[df_selection_user['folder_id'] == folder_id].sort_values(by='date')
                                          
         #     cont_tot += len(df_sub_selection)

   

         #     df_result= grouping(df_sub_selection)
          #    df_filtered = pd.concat([df_filtered,df_result])
         # 
         #     cont_selection += len(df_result)

       #   print cont_users, tot_num_users
       #   cont_users +=1
        
        
   #   print "done" 


  #    print "original:", df.shape, "   processed:",df_filtered.shape
   #   print cont_tot, cont_selection
  


    
    
   #   new_file_name=path+input_file.replace(".csv","")+"processed_timestaps.csv"
  #    df_filtered.to_csv(new_file_name, sep=',')
   #   print "written:", new_file_name,"\n\n\n"



############################################################
#############################################################
###########################################################


def  grouping(input_df):

   
    new_var=np.nan 
    user_id =  input_df.user_id.iloc[0]
    folder_id= input_df.folder_id.iloc[0]
    new_var= str(user_id) +"_" +str(folder_id)
    
    
    
    list_values_add=[]   # i need to create a list of actual activity values, not cumulative ones
    list_values_edit=[]
    list_values_del=[]    
        
   
        
                
    list_indeces=[]
    flag_new=1

    old_tupla_activity=(None,None,None)        

    old_value_add=0
    old_value_edit=0
    old_value_del=0

    
    cont=1
    for row in input_df.iterrows():
        index=row[0]

        num_adds=row[1].num_adds_last28days
        num_edits=row[1].num_edits_last28days
        num_dels=row[1].num_dels_last28days

        tupla_activity=(num_adds,num_edits ,num_dels)  #  num_adds_last28days','num_edits_last28days','num_dels_last28days


        if tupla_activity == old_tupla_activity:
            flag_new =0
        else:
            flag_new=1


            

        if flag_new ==1:   # OJO!!!  double check! THE RESETTING TO TAKE INTO ACCOUNT THE 28 DAY PERIOD!!!!!!!!11  


            list_indeces.append(index)


            if old_value_add  <=   num_adds: 
                actual_val_add = num_adds - old_value_add
            else:
                actual_val_add = num_adds                                                                         

            if old_value_edit <= num_edits:       
                actual_val_edits = num_edits- old_value_edit
            else:
                actual_val_edits = num_edits

            if old_value_del  <=  num_dels:
                actual_val_del = num_dels - old_value_del                
            else:
                actual_val_del = num_dels 



            list_values_add.append(actual_val_add)
            list_values_edit.append(actual_val_edits)
            list_values_del.append(actual_val_del)


            

        old_tupla_activity=tupla_activity


        old_value_add= num_adds
        old_value_edit= num_edits
        old_value_del= num_dels


        cont +=1

        selected_df=input_df.ix[list_indeces]


        selected_df['num_adds'] = pd.Series(list_values_add, index=list_indeces)
        selected_df['num_edits'] = pd.Series(list_values_edit, index=list_indeces)
        selected_df['num_dels'] = pd.Series(list_values_del, index=list_indeces)
    
 

    return selected_df
    
    







######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

