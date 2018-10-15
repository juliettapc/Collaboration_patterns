 
import pandas as pd
import random
import numpy as np
from time import sleep
import scipy
import operator
import difflib
import math
from pandas import parser

try:
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle
    
import unicodedata
import networkx as nx
import itertools
import seaborn as sns   ### https://seaborn.pydata.org/tutorial/categorical.html
import time  







def main():



   



    # ######## load dictionaries for user: list_folders, and folder: list_users
    path="/home/julia/Dropbox_collaborations/Results/"
    pickle_name='dict_user_id_list_folders_COMPLETE.pickle'
    with open(path+pickle_name, 'rb') as handle:
        dict_user_id_list_folders = pickle.load(handle)
    print "num. users:",len(dict_user_id_list_folders)



    pickle_name='dict_folder_id_list_users_COMPLETE.pickle'
    with open(path+pickle_name, 'rb') as handle:
        dict_folder_id_list_users = pickle.load(handle)
    print "num. folders:",len(dict_folder_id_list_users)
    #######################################################













    ###### i cant read the file all at once becauase of a memory dump issue , too big, so i read by chunks
    chunksize = 1000000   # number of rows i read each time
    list_user_ids=[]
    
    
    header_names = ['folder_id','folder_creation_date','user_id','num_adds','num_edits','num_dels','date']
    
    
    
    input_file='duplicates_removed_no_header.csv'     #results_nico2.csv
    
    df_folder_user=pd.DataFrame(columns=header_names)  # i create an empty dataframe
    dict_user_basic_attr={}
    
    


    path="/home/julia/Dropbox_collaborations/Data/Dropbox/"

    for chunk_df in pd.read_csv(path+input_file, na_values=["NAN","-1","null"],header=None,  names=header_names,usecols=[0,2,4,6,7,8,11], chunksize=chunksize, sep=None ):  # ojo!!! because some rows have irregular number of separators, i specify sep=None, so python does the parsing for me and doesnt raise an error
            
            print chunk_df.shape#, len(lista)
                        
            df_folder_user=pd.concat([df_folder_user, chunk_df])  # i add new chunks of data every time, but also drop new duplicates
            
            print "building df:",df_folder_user.shape, len(df_folder_user.user_id.unique())                   
    


    print "done reading!"      
    print input_file, df_folder_user.shape   
    print len( df_folder_user.folder_id.unique()), "folders   ",len( df_folder_user.user_id.unique()),"users"















    header_names = ['folder_id','folder_creation_date','user_id','num_adds','num_edits','num_dels','date']  
    df_aggr_act = pd.DataFrame(columns=header_names)   # i create an empty dataframe


    print "working on aggregating activity........."
    cont_selection=0
    cont_tot=0
    cont=0    
    for user_id in dict_user_id_list_folders:           
    
         list_folders=dict_user_id_list_folders[user_id]
    
         pre_df_selection_user= df_folder_user[df_folder_user['user_id'] == user_id]
    
         for folder_id in list_folders:
        
             df_selection =  pre_df_selection_user[ pre_df_selection_user['folder_id'] == folder_id]
                                          
             cont_tot += len(df_selection)
           

             df_result= grouping(df_selection)
             df_aggr_act = pd.concat([df_aggr_act,df_result])
        
             cont_selection += len(df_result)
        
        
         
         cont +=1    
         if cont == 10000   or  cont == 100000    or    cont == 200000  or  cont == 300000  or cont == 400000 :               
             new_name=path+input_file.replace(".csv","")+"_only_aggr_activity_by_date_PARTIAL__faster.csv"
             df_aggr_act.to_csv(new_name, sep=',')
             print "partial file written:", new_name,"\n\n\n"
             print df_aggr_act.shape
             
        







        
        
    print "done"  
    print "original df:", df_folder_user.shape, "    aggr act by date:", df_aggr_act.shape, cont_selection




    new_name="duplicates_removed_only_activity_aggr_by_date.csv"
    df_aggr_act.to_csv(path+new_name, sep=',')
    print "written:", new_name,"\n\n\n"
   
    






###################################
########################################

#to add up all activity for a given user, folder and date (diff activity counts for diff. types of files (not majoyr_content necessarily), and i aggregate them all)

def  grouping(input_df):  # input_df is a selection of all rows for a given user_id and folder_id, sorted by date
    

    header_names = ['folder_id','folder_creation_date','user_id','num_adds','num_edits','num_dels','date']
    df_result = pd.DataFrame(columns=header_names)   

    
    user_id =  input_df.user_id.iloc[0]
    folder_id= input_df.folder_id.iloc[0]
    folder_creation_date= input_df.folder_creation_date.iloc[0]

    list_dates= list(set(input_df.date.values))  # list of unique dates for a given user and folder


    for date_act in list_dates:        
        
          
        sum_adds=np.nan
        sum_edits=np.nan
        sum_dels=np.nan

                                          
      
        if pd.isnull(date_act):
#             print date_act, "oh-oh !"
           
            pass
        else:
            


            df_date_selection= input_df[ input_df['date']== date_act]

            sum_adds=sum(list(df_date_selection.num_adds.values))
            sum_edits=sum(list(df_date_selection.num_edits.values))
            sum_dels=sum(list(df_date_selection.num_dels.values))

   
                                                                                                         
        df_one_date = pd.DataFrame({'user_id':[user_id],'folder_id':[folder_id],'folder_creation_date':[folder_creation_date],'date':[date_act],'num_adds':[sum_adds],\
                                    'num_edits':[sum_edits],'num_dels':[sum_dels]})                         
        df_result = pd.concat([df_result,df_one_date])  # i concatenate all rows for a given user and folder (one row per diff date)              
   


    return df_result.sort_values(by='date')                     


          


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



