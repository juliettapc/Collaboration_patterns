#!/usr/bin/env python

'''
Created by Julia Poncela, on Oct. 2017

'''

import matplotlib.pyplot as plt   
import pandas as pd
import numpy as np
import scipy
import operator
import difflib
import math

try:
    import cPickle as pickle  ##################################
   #it is faster than pickle!
except:
    import pickle


import itertools
import geopy.distance   







def main():





    ######### load dictionaries for user: list_folders, and folder: list_users
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




    pickle_name='new_dict_user_id_user_attr.pickle'
    with open(path+pickle_name, 'rb') as handle:
        dict_user_id_user_attr = pickle.load(handle)
    print "num. folders:",len(dict_user_id_user_attr)
  




    ########  csv  users basic attr
    path="/home/julia/Dropbox_collaborations/Data/Dropbox/"
    input_file = 'new_DROPBOX_basic_user_attr.csv'
    df_user_basic_attr = pd.read_csv(path+input_file, sep=';',na_values=["NAN","-1","null"]) # set header=0 if i wanna pass it my own list of header names
    #df_user_basic_attr.drop('Unnamed: 0', axis=1, inplace=True)
    print "num. users:",df_user_basic_attr.shape





    #########  csv  all act aggr by date
    path="/home/julia/Dropbox_collaborations/Data/Dropbox/"
    input_file = 'DROPBOX_duplicates_removed_only_activity_aggr_by_date.csv' #duplicates_removed_no_header_only_aggr_activity_by_date_PARTIAL__faster.csv'
    df_all_act = pd.read_csv(path+input_file, sep=',',na_values=["NAN","-1","null"], parse_dates=['folder_creation_date','date']) # set header=0 if i wanna pass it my own list of header names    
    print "num. users:",len(df_all_act.user_id.unique()),df_all_act.shape    # 200000 (3072489, 8)
                                                                                    
    df_all_act=df_all_act.replace('nan', np.nan)  ## for some reason, there are diff nomenclatures for NANs, and it is not interpreting them correctly when reading the file 
    df_all_act=df_all_act.replace('NAN', np.nan)
    df_all_act=df_all_act.replace('NaN', np.nan)
    df_all_act=df_all_act.replace('-1', np.nan)
    df_all_act=df_all_act.replace('', np.nan)
    



#convert the date columns from str to datetime    (for some reason, parsing when i read it does nothing)
    df_all_act['date'] = pd.to_datetime(df_all_act['date'], errors='coerce')
    df_all_act['folder_creation_date'] = pd.to_datetime(df_all_act['folder_creation_date'], errors='coerce')
    
   # df_all_act_no_NANs= df_all_act[df_all_act.date.notnull()]    
   # print "after removing rows without dates:\n  num. users:",len(df_all_act_no_NANs.user_id.unique()),df_all_act_no_NANs.shape    # 400000  (5141758, 7)

















#########################

    
    print "processing users......"
    
   # cont =0
    for user_id in dict_user_id_list_folders:
    
       
        list_folders=dict_user_id_list_folders[user_id]
    
        df_select_user_attr=df_user_basic_attr[df_user_basic_attr['user_id'] == user_id]         
        df_select_user_act=df_all_act[df_all_act['user_id']==user_id].sort_values(by=['folder_id', 'date'])
    
    
        grouping_user(user_id, df_select_user_act, df_select_user_attr, list_folders, dict_user_id_user_attr)    # i call this function that modifies the main dict         
                

    print "done with users",len(dict_user_id_user_attr)

    
    
    
    

    pickle_name='/home/julia/Dropbox_collaborations/Results/new_dict_user_id_user_attr_.pickle'
    with open(pickle_name, 'wb') as handle:
        pickle.dump(dict_user_id_user_attr, handle)
    print "written:", pickle_name



    df_from_dict = pd.DataFrame.from_dict(dict_user_id_user_attr,orient='index')
    #df_from_dict['user_id'] = df_from_dict.index
    df_from_dict.to_csv(pickle_name.strip("dict_").strip(".pickle")+".csv", sep=';')
    print "written:", pickle_name.strip("dict_").strip(".pickle")+".csv"





    exit()




    print "processing folders......"
#    cont=1
    dict_folder_id_folder_attr={}
    for folder_id in dict_folder_id_list_users:      
    
            list_users=dict_folder_id_list_users[folder_id]

            df_select_folder_act=df_all_act[df_all_act['folder_id']== folder_id].sort_values(by='date')        
            df_select_users_attr= df_user_basic_attr[df_user_basic_attr.user_id.isin(list_users)]        


          #  cont +=1
            grouping_folder(folder_id, dict_folder_id_folder_attr, df_select_folder_act, df_select_users_attr, list_users, dict_user_id_list_folders,dict_folder_id_list_users)
     
    
    print "done with folders", len(dict_folder_id_folder_attr)









    pickle_name='/home/julia/Dropbox_collaborations/Results/dict_folder_id_folder_attr_new.pickle'
    with open(pickle_name, 'wb') as handle:
        pickle.dump(dict_folder_id_folder_attr, handle)
    print "written:", pickle_name



    pickle_name='/home/julia/Dropbox_collaborations/Results/folder_id_folder_attr_new.csv'
    df_from_dict = pd.DataFrame.from_dict(dict_folder_id_folder_attr,orient='index')
    df_from_dict.to_csv(pickle_name, sep=';')
    print "written:", pickle_name









######################################
#####################################
#####################################
#####################################


def remove_nans(lista):
   # print "\n",lista
    aux_lista=[]
    for i in range(len(lista)):    
       # print lista[i]
        try:
            if np.isnan(lista[i]) == True:  # (when nan):   # OJO!!! NO SIRVE SI HAGO: if lista[I]== np.nan   :(   !!!
                pass#print "nan found"
            else: # (when not-nan):           
                aux_lista.append(lista[i])
            #print "no problem"
        except : ## whenever it is a STR            
            pass            
            
            
    #print aux_lista   
    return aux_lista


############################3



def remove_nans_for_strings(lista):
   # print "\n",lista
    aux_lista=[]
    for i in range(len(lista)):    
       # print lista[i]
        try:
            if np.isnan(lista[i]) == True:  # (when nan):   # OJO!!! NO SIRVE SI HAGO: if lista[I]== np.nan   :(   !!!
                pass#print "nan found"
            else: # (when not-nan):           
                aux_lista.append(lista[i])
            #print "no problem"
        except : ## whenever it is a STR            
             aux_lista.append(lista[i])#pass             
            
            
    #print aux_lista   
    return aux_lista




###############

def remove_nans_replace_by_zeros(lista):
   # print "\n",lista
    aux_lista=[]
    for i in range(len(lista)):    
       # print lista[i]
        try:
            if np.isnan(lista[i]) == True:  # (when nan):   # OJO!!! NO SIRVE SI HAGO: if lista[I]== np.nan   :(   !!!
                aux_lista.append(0.)        #pass#print "nan found"
            else: # (when not-nan):           
                aux_lista.append(float(lista[i]))
            #print "no problem"
        except : ## whenever it is a STR            
            pass             
            
            
    #print aux_lista   
    return aux_lista




###### get dict with  folder_id lifespan:
def remove_nans_replace_intervals_with_starting_value(lista):
    #print "\n",lista
    aux_lista=[]
    for i in range(len(lista)):    
       # print lista[i]
        try:
            if np.isnan(lista[i]) == True:  # (when/ nan):   # OJO!!! NO SIRVE SI HAGO: if lista[I]== np.nan   :(   !!!
                pass#print "nan found"
        except TypeError: # (when not-nan):
            #print lista[i]   
            try:  
                aux_lista.append(float(lista[i]))
                #print "no problem"
            except ValueError:  # sometimes, the ranking is 75-82
                #print "issue found"
                value=lista[i]
#                 v1=float(value.split("-")[0])
#                 v2=float(value.split("-")[1])
                
                new_value=float(value.split("-")[0])#np.median([v1,v2])  
                aux_lista.append(new_value)
            
    #print aux_lista   
    return aux_lista


#############



def gini(old_list_of_values):
    
    list_of_values=[]
    for item in old_list_of_values:
        try:
            int(item) # if it is a NAN, it with fail
            list_of_values.append(item)
        except:
            pass
    
   # print list_of_values
    sorted_list = sorted(list_of_values)
    height, area = 0, 0
    for value in sorted_list:
        height += value
        area += height - value / 2.
    fair_area = height * len(list_of_values) / 2.
    try:
        return (fair_area - area) / fair_area
    except ZeroDivisionError:
#         print "problems with:",list_of_values   # if lista=[0,0,0]  or [0]
#         raw_input()
        return np.nan


##############


def  effective_num(lista_values):  # i can use it for the effective number of members in a folder, by activity, or the effective number of folders for a user, also by activity
    
     # first, i need to remove the zeros, because i cant do the log(0), but i can remove them, they dont count as effective members
    
    
    cont_num_nonzero_items=0
    H=0.
    tot_sum=float(sum(lista_values))
    for item in lista_values:
        if item >0:
            aux= item/tot_sum * np.log2( item/tot_sum)
            H += aux
            cont_num_nonzero_items +=1
            
    H = -1.0 * H
    
    eff_number = np.power(2.0, H)
    
    if cont_num_nonzero_items ==0:   # if the list of act is [0] then i want the eff. number to be 0, not 1
        eff_number =0
    
    return eff_number
        

        

###########  i get dict for the user_id vs attr


def grouping_user(user_id, df_select_user_act, df_select_user_attr, list_folders, dict_user_id_user_attr):
    

    
    dict_user_id_user_attr[user_id]={}
    dict_user_id_user_attr[user_id]["number_folders"]=len(list_folders)
   

     
    
    
    ############ user's burstiness and avg interevent time
    if len(df_select_user_act)>2:        
        
       
        list_deltas= ( df_select_user_act.date - df_select_user_act.date.shift() ).fillna(0)
        lista_interevent_times=[x.days for x in list_deltas][1:]      # the first delta time is always zero because it comes from comparing to nan when shifting the column


       # print lista_interevent_times
        m1=np.mean(lista_interevent_times)
        s1=np.std(lista_interevent_times)

        burstiness= (s1-m1)/(s1+m1)
        dict_user_id_user_attr[user_id]["burstiness"]= burstiness
        dict_user_id_user_attr[user_id]["avg_interevent_time"]= np.mean(lista_interevent_times)
       
       
    else:
        dict_user_id_user_attr[user_id]["burstiness"]=np.nan
        dict_user_id_user_attr[user_id]["avg_interevent_time"]= np.nan

    
    
    
    





########### i get dict for the folder_id attr.
###############################
##############################
################################


def grouping_folder(folder_id, dict_folder_id_folder_attr, df_select_folder_act, df_select_users_attr, list_users, dict_user_id_list_folders,dict_folder_id_list_users):   # df_select_folder_act is sorted by user_id and then date
   
   
    
    dict_folder_id_folder_attr[folder_id]={}
    
    dict_folder_id_folder_attr[folder_id]["number_active_members"]=len(list_users)
   
    
    
    list_users_projects=[]
    for user_id in list_users:
        list_users_projects += dict_user_id_list_folders[user_id]
        
    dict_folder_id_folder_attr[folder_id]["num_unique_projects_members_work_on"]=len(list(set(list_users_projects)))  # total "experience" of the team
    
                        
    
    
    
   
  
    folder_lifespan=1          # the selected dataframe is sorted by date already       
    try:        
        folder_lifespan= (df_select_folder_act.date.iloc[-1] -  df_select_folder_act.folder_creation_date.iloc[0]).days +1       
       
    except AttributeError:  # in case the last date happens to be NAN, then i look for the last non-nan date available
    
        cont=1
        index=-2
        while cont <= len(df_select_folder_act) :
            try:
                folder_lifespan= (df_select_folder_act.date.iloc[index] -  df_select_folder_act.folder_creation_date.iloc[0]).days +1         
                cont = 10000000
            except : 
                index -=1

            cont +=1               
            
    dict_folder_id_folder_attr[folder_id]["folder_lifespan"]=folder_lifespan
   


            
    act_period=1   # because the creation date of most folders is years before our observation period        
    try:       
        act_period= (df_select_folder_act.date.iloc[-1] -  df_select_folder_act.date.iloc[0]).days +1
    except AttributeError:  # in case the last dates happen to be NAN
    
        cont=1
        index=-2
        while cont <= len(df_select_folder_act) :
            try:
                act_period= (df_select_folder_act.date.iloc[index] -  df_select_folder_act.date.iloc[0]).days +1               
                cont = 10000000
            except : 
                index -=1

            cont +=1          
                                                            
    dict_folder_id_folder_attr[folder_id]["act_period"]=act_period    
    
    
     
        
    
    old_list_univ_rankings=remove_nans_for_strings(list(df_select_users_attr.world_ranking))    #ojo!!! rankings are str!!    
    list_univ_rankings = [float(i) for i in old_list_univ_rankings]   
    dict_folder_id_folder_attr[folder_id]["folder_univ_median_ranking"]=np.median(list_univ_rankings)
    dict_folder_id_folder_attr[folder_id]["folder_univ_SD_ranking"]=np.std(list_univ_rankings)
    dict_folder_id_folder_attr[folder_id]["folder_univ_mean_ranking"]=np.mean(list_univ_rankings)

   
    
    
    try:
        most_common=max(set(list_univ_rankings), key=list_univ_rankings.count)
    except:  # when empty list
        most_common=np.nan
    dict_folder_id_folder_attr[folder_id]["most_common_univ_ranking"]=most_common
    
    
    
    
                   
    lista_univ=list(df_select_users_attr.University_name.dropna().unique())       
    dict_folder_id_folder_attr[folder_id]["num_universities"]=len(lista_univ)
    
   
    dict_folder_id_folder_attr[folder_id]["num_fields"]=np.nan    
    lista_fields=list(df_select_users_attr.field.dropna().unique())
    num_fields=len(lista_fields)
    if num_fields >0:
        dict_folder_id_folder_attr[folder_id]["num_fields"]=num_fields
    
    
        
       
    lista_countr=list(df_select_users_attr.Country.dropna().unique())       
    dict_folder_id_folder_attr[folder_id]["num_countries"]=len(lista_countr)
                
   
           
        
    
    tot_act=0   
    dict_user_id_contrib={}
    for user_id in list_users:
        
        df_select_user_act= df_select_folder_act[df_select_folder_act['user_id']==user_id]
        
        num_adds=sum(remove_nans_replace_by_zeros(list(df_select_user_act.num_adds)))  # for activity, NAN=0
        num_edits=sum(remove_nans_replace_by_zeros(list(df_select_user_act.num_edits)))
        num_dels=sum(remove_nans_replace_by_zeros(list(df_select_user_act.num_dels)))
        act=num_adds+num_edits+num_dels    
                      
            
        dict_user_id_contrib[user_id] =act      
        tot_act += act
    

    
    list_tot_act_each_user_in_folder=dict_user_id_contrib.values()
    dict_folder_id_folder_attr[folder_id]["folder_activity_GINI"]=gini(list_tot_act_each_user_in_folder)
    dict_folder_id_folder_attr[folder_id]["eff_num_members"]=effective_num(list_tot_act_each_user_in_folder)
    
    
    


    max_contr=max(list_tot_act_each_user_in_folder) # size of the maximum contribution
    max_user=max(dict_user_id_contrib.iteritems(), key=operator.itemgetter(1))[1]  # user with max contribution to the folder
    
    dict_folder_id_folder_attr[folder_id]["dominated_folder"]=0
    dict_folder_id_folder_attr[folder_id]["folder_dominator"]=np.nan
    
    if max_contr > sum(sorted(list_tot_act_each_user_in_folder)[:-1]):
        dict_folder_id_folder_attr[folder_id]["dominated_folder"]=1
        dict_folder_id_folder_attr[folder_id]["folder_dominator"]=max_user
    

    
    
    
    
    
    tot_num_adds=sum(remove_nans_replace_by_zeros(list(df_select_folder_act.num_adds)))
    dict_folder_id_folder_attr[folder_id]["folder_tot_num_adds"]=tot_num_adds
    
    
    tot_num_edits=sum(remove_nans_replace_by_zeros(list(df_select_folder_act.num_edits)))
    dict_folder_id_folder_attr[folder_id]["folder_tot_num_edits"]=tot_num_edits
    
        
    tot_num_dels=sum(remove_nans_replace_by_zeros(list(df_select_folder_act.num_dels)))
    dict_folder_id_folder_attr[folder_id]["folder_tot_num_dels"]=tot_num_dels
    
    
    num_tot_act=tot_num_adds+tot_num_edits+tot_num_dels
    dict_folder_id_folder_attr[folder_id]["folder_tot_act"]=num_tot_act
    
    
   
    
    
    
    lista_careers=remove_nans_for_strings(list(df_select_users_attr.career_stage))  
   
    try:
        most_common=max(set(lista_careers), key=lista_careers.count)
    except ValueError:  # when empty list
        most_common=np.nan
    dict_folder_id_folder_attr[folder_id]["most_common_career_stage"]=most_common
    
    
    try:    
        dict_folder_id_folder_attr[folder_id]["fraction_SR"]=lista_careers.count("sr")/float(len(lista_careers))
    except ZeroDivisionError:
        dict_folder_id_folder_attr[folder_id]["fraction_SR"]=np.nan
    
    
    
    
             
    
    sr_users=list(df_select_users_attr[df_select_users_attr['career_stage'] == "sr"].user_id.dropna().unique())
    df_select_sr_act= df_select_folder_act[df_select_folder_act.user_id.isin(sr_users)]
    
    act_sr=sum(remove_nans_replace_by_zeros(list(df_select_sr_act.num_dels))) +    sum(remove_nans_replace_by_zeros(list(df_select_sr_act.num_edits)))+     sum(remove_nans_replace_by_zeros(list(df_select_sr_act.num_adds)))
    try:
        dict_folder_id_folder_attr[folder_id]["fraction_work_by_SR"]=  act_sr/float(tot_act)
    except ZeroDivisionError:    
        dict_folder_id_folder_attr[folder_id]["fraction_work_by_SR"]= np.nan
        
        
   
    if lista_careers.count("sr")==0:
        dict_folder_id_folder_attr[folder_id]["fraction_work_by_SR"]= np.nan
    
   
    
    
    
     
        
 
    lista=remove_nans(list(df_select_users_attr.category_total_publ))
    try:
        most_common=max(set(lista), key=lista.count)
    except ValueError:  # empty list
        most_common=np.nan
    dict_folder_id_folder_attr[folder_id]["most_common_categ_num_publ"]=most_common
    
    
  
    lista=remove_nans(list(df_select_users_attr.category_total_last_auth))
    try:
        most_common=max(set(lista), key=lista.count)
    except ValueError:  # empty list
        most_courmmon=np.nan
    dict_folder_id_folder_attr[folder_id]["most_common_categ_num_last_auth"]=most_common
   
    
     
    lista=remove_nans(list(df_select_users_attr.category_total_cit))
    try:
        most_common=max(set(lista), key=lista.count)
    except ValueError:  # empty list
        most_common=np.nan
    dict_folder_id_folder_attr[folder_id]["most_common_num_cit"]=most_common

    



    ########## avg geo. distance among members of the team:                     
    lista_members=dict_folder_id_list_users[folder_id]
    
    if len(lista_members)>1:
        
        list_diff_loc=list(df_select_users_attr.geoloc.dropna().unique())
        
        if len(list_diff_loc)>1:
    
            lista_pares=itertools.combinations(lista_members, 2)        
            lista_dist_pairs=[]
            
#             print df_select_users_attr
#             print 
            dict_user_geol=pd.Series(df_select_users_attr.geoloc.values,index=df_select_users_attr.user_id).to_dict()  # i get a dict from two columns
            #print dict_user_geol
           
            for pair in lista_pares:
                user1=pair[0]
                user2=pair[1]
           
                list_coord=[]
                for user in [user1, user2]:
                    #coord=df_select_users_attr[df_select_users_attr["user_id"]== user].geoloc.iloc[0] #  Examples: '(40.4428081, -79.94301279999999) 15213'  or just: '(40.4428081, -79.94301279999999)'
                    coord=dict_user_geol[user]
#                     print "user",user, "  old:",coord, "  new:",coord_bis
#                     raw_input()
                    try:
                        coord=coord.replace("(","").replace(")","").replace(", ",",").split(" ")[0]
                        lon=float(coord.split(",")[0])
                        lat=float(coord.split(",")[1])
                        tupla=(lon, lat)
                        list_coord.append(tupla)
                    except AttributeError:  # if one user doesn't have coordenates info
                        pass
                       
    
    
    
    

                try:  # to ignore the cases when one of the users doesnt have geoloc info
                    dist_pair=geopy.distance.vincenty(list_coord[0], list_coord[1]).km            
                    lista_dist_pairs.append(dist_pair)
                except : pass

                
            dict_folder_id_folder_attr[folder_id]["avg_geo_dist_km"]=np.mean(lista_dist_pairs)
            dict_folder_id_folder_attr[folder_id]["std_geo_dist_km"]=np.std(lista_dist_pairs)
            

            
        else:  # if all users in the same geolocation
            dict_folder_id_folder_attr[folder_id]["avg_geo_dist_km"]=0.
            dict_folder_id_folder_attr[folder_id]["std_geo_dist_km"]=0.
        
        
    else:  # if only one user in the team
        dict_folder_id_folder_attr[folder_id]["avg_geo_dist_km"]=0.
        dict_folder_id_folder_attr[folder_id]["std_geo_dist_km"]=0.
    ################   
    
    
    
    
    
    ######## i count how many users in this folder are above-avg in at least one of their folders
    try:
        num_above_avg_contributors=0.
        for user_id in list_users:
            suma=sum(df_select_users_attr[user_id]["folders_above_avg"].values())  # for each user, this is a dict folder: 1 or 0 for above personal avg contributor or not ;    dict_user_id_user_attr[user_id]["folders_above_avg"]=dict_folder_id_above_avg_work
   
            if suma >0:
                num_above_avg_contributors +=1

        dict_folder_id_folder_attr[folder_id]["num_above_avg_contributors"] = num_above_avg_contributors   # i measure how many leaders i have in a team
    except:
        dict_folder_id_folder_attr[folder_id]["num_above_avg_contributors"]=np.nan

    

    try:
        dict_folder_id_folder_attr[folder_id]["fract_above_avg_contributors"]=dict_folder_id_folder_attr[folder_id]["num_above_avg_contributors"]/float(dict_folder_id_folder_attr[folder_id]["number_active_members"])
    except:
        dict_folder_id_folder_attr[folder_id]["fract_above_avg_contributors"]=np.nan

    


###########################################################
###########################################################
###########################################################  
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "



#################################################
######################################################



