#!/usr/bin/env python

'''
Created by Julia Poncela, on Oct. 2017

'''

import matplotlib.pyplot as plt   
import pandas as pd
import random
import numpy as np
import scipy
import operator
import difflib
import math
try:
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle
    
import unicodedata
import networkx as nx
import itertools






def main():


    ###############################


    path = "/home/julia/Dropbox_collaborations/Data/Dropbox/"
    input_file = 'DROPBOX_duplicates_removed_only_activity_aggr_by_date.csv'  # one line per user, folder, and date of activity

    df = pd.read_csv(path+input_file, sep=',',na_values=["NAN","-1","null"],low_memory=False, parse_dates=['folder_creation_date','date']) # set header=0 if i wanna pass it my own list of header names
    df.drop('Unnamed: 0', axis=1, inplace=True)

    print df.shape






    ######## load dictionary aggregated info by user  
    pickle_name='/home/julia/Dropbox_collaborations/Results/new_dict_user_id_user_attr.pickle'
    with open(pickle_name, 'rb') as handle:
        dict_user_id_user_attr = pickle.load(handle)
    print len(dict_user_id_user_attr.keys())

    df_users = pd.DataFrame.from_dict(dict_user_id_user_attr,orient='index')
    df_users['user_id'] = df_users.index
    print df_users.shape   # 440353, 11







    pickle_name='/home/julia/Dropbox_collaborations/Results/dict_folder_id_list_users_COMPLETE.pickle'
    with open(pickle_name, 'rb') as handle:
            dict_folder_list_users = pickle.load(handle)
    print "read:", pickle_name, len(dict_folder_list_users)

    pickle_name='/home/julia/Dropbox_collaborations/Results/dict_user_id_list_folders_COMPLETE.pickle'
    with open(pickle_name, 'rb') as handle:
            dict_user_list_folders = pickle.load(handle)
    print "read:",pickle_name,  len(dict_user_list_folders)












    dict_folder_dict_user_act_in_folder={}

    for folder_id in dict_folder_list_users:  

            list_users_in_folder=dict_folder_list_users[folder_id]

            for user_id in list_users_in_folder:


                df_select = df[(df['folder_id'] == folder_id )  & (df['user_id']==user_id )]



                num_adds=sum(remove_nans_replace_by_zeros(list(df_select.num_adds))) # for activity records, NAN = 0
                num_edits=sum(remove_nans_replace_by_zeros(list(df_select.num_edits)))
                num_deletes=sum(remove_nans_replace_by_zeros(list(df_select.num_dels)))
                user_act=num_adds+num_edits+num_deletes


            try: 
                dict_folder_dict_user_act_in_folder[folder_id]
            except KeyError:
                dict_folder_dict_user_act_in_folder[folder_id]={}            

            dict_folder_dict_user_act_in_folder[folder_id][user_id]=user_act


    print "done with the dicts., size:",len(dict_folder_list_users),len(dict_folder_dict_user_act_in_folder)






    path="/home/julia/Dropbox_collaborations/Results/"
    filename="dict_folder_dict_user_act_in_folder.pickle"
    with open(path+filename,'wb') as f:
        pickle.dump(dict_folder_dict_user_act_in_folder, f)
    print "written:",path+filename







    ####################
    ######## unweighted network:
    list_missing_nodes=[]
    G=nx.Graph()
    for folder_id in dict_folder_list_users:           

            lista=dict_folder_list_users[folder_id]

            if len(lista)>1:

                lista_pares=itertools.combinations(lista, 2)        

                for item in lista_pares:
                    e1=item[0]
                    e2=item[1]
                    G.add_edge(e1,e2)

                    try: 
                        G.edge[e1][e2]["num_common_projects"] +=1
                    except KeyError:
                        G.edge[e1][e2]["num_common_projects"] =1


            else:

                n=lista[0]
                G.add_node(n)
                try:  # because of the partial dict of user's attributes 
                    G.node[n]["tot_act"]=dict_user_id_user_attr[n]['user_tot_act']
                except KeyError:
                    G.node[n]["tot_act"]=np.nan
                    list_missing_nodes.append(n)



    print "  N:", len(G.nodes()),"  L:", len(G.edges())       
    GC = max(nx.connected_component_subgraphs(G), key=len)
    print "\n  GC:     N:", len(GC.nodes()), "  L:", len(GC.edges())




    path="/home/julia/Dropbox_collaborations/Results/Networks/"
    filename="network_all_new.pickle"
    with open(path+filename,'wb') as f:
        pickle.dump(G, f)
    print "written:",path+filename






   










    print df_users.user_tot_act.mean(), df_users.user_tot_act.quantile(q=0.6)
    act_threshold=1. #  28 is the 60% ,  56 is the 65%  ,   168 is the 70% percentile (50% percentile is 0 and 55% is also 0)

    print "thershold for activity",act_threshold

    ##############################
    ####### weighted network:

    G_weighted=nx.Graph()
    for folder_id in dict_folder_list_users:


            lista_users=dict_folder_list_users[folder_id]

            weighted_list_users=[]
            for user_id in lista_users:

                try:
                    user_act_in_folder=dict_folder_dict_user_act_in_folder[folder_id][user_id]
                    if float(user_act_in_folder) >= act_threshold:
                        weighted_list_users.append(user_id)
                except KeyError:
                    list_missing_nodes.append(user_id)
                   
               

            if len(weighted_list_users)>1:  # ignore nodes that havent done any work in a particular folder (they will only count as isolated)

                lista_pares=itertools.combinations(weighted_list_users, 2)        

                for item in lista_pares:
                    e1=item[0]
                    e2=item[1]
                    G_weighted.add_edge(e1,e2)               

                    try: 
                        G_weighted.edge[e1][e2]["num_common_projects"] +=1
                    except KeyError:
                        G_weighted.edge[e1][e2]["num_common_projects"] =1




            for n in lista_users:
                G_weighted.add_node(n)
                try: 
                    G_weighted.node[n]["tot_act"]=dict_user_id_user_attr[n]['user_tot_act']
                except KeyError:
                    G_weighted.node[n]["tot_act"]= np.nan






    print "  N:", len(G_weighted.nodes()),"  L:", len(G_weighted.edges())       
    GC = max(nx.connected_component_subgraphs(G_weighted), key=len)
    print "\n  GC:     N:", len(GC.nodes()), "  L:", len(GC.edges())





    path="/home/julia/Dropbox_collaborations/Results/Networks/"
    filename="network_all_weighted_by_act_thresh"+str(act_threshold)+"_new.pickle"
    with open(path+filename,'wb') as f:
        pickle.dump(G_weighted, f)
    print "written:",path+filename



    print "num. missing nodes:", len(set(list_missing_nodes))






############################################
############################################
############################################
############################################



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
