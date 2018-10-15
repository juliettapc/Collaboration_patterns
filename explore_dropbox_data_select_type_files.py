#!/usr/bin/env python

'''
Created by Julia Poncela, on Feb. 2016

'''

import datetime as dt
import csv
import pickle
import operator
import histograma_gral


def main():


    sample_size=100000000

    testing_string=""
    if 29883243 > sample_size:
        testing_string="_testing"
      


    name1="../Results/Summary_count_types_files_actions_actors_selecting_some_file_types"+testing_string+".dat"
    file1= open(name1, 'wt')
    

    list_interesting_file_types=["txt","dta","pdf","mat","docx","doc","xlsx","tex","pptx", "dat","csv","xls"]


    print "file extentions included in the analysis:"
    print list_interesting_file_types,"\n"
   



    print >> file1, "file extentions included in the analysis:"
    print >> file1, list_interesting_file_types,"\n"

    #first_day_history=dt.datetime(1985,1,1)
    #last_day_history= dt.datetime(2005,12,31)
    #mark_date_final =  mark_date_initial + dt.timedelta(days = 30)   






 

    ####### header: action_ts	action_day	action_time	actor_id	actor_domain 	actor_country	actor_activity_score	action	platform	file_ext	file_size 	sf_id 	sf_created	sf_created_human	sf_major_file_ext	sf_pattern_label	sf_file_path_id 
    
   ##### NOTES: 
    #  actor_domain (from their email)
    #  file_size (bites)
    #  sf_id (shared-folder)
    #  sf_file_path_id (for uniquely identifying  file i need:  sf_id + sf_file_path_id)  **note that if 2 files in diff have same name, then they have same sf_file_path_id


    ####### Number of lines in the original file:     wc -l Dropbox_data.csv 
    ###                                                29883243  Dropbox_data.csv  (around 30M lines)



    
  
   
    name0="../Data/Dropbox_data.csv"
    print "reading: ", name0, "......."       
    csvfile=open(name0, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   ##### to skip the header
             

    dict_types_files_count={}
    dict_types_actions_count={}

    dict_actors_num_actions={}
    
    dict_file_id_num_actions={}
    dict_file_id_list_actors={}

    dict_folder_id_num_actions={}
    dict_folder_id_list_actors={}
   
    list_all_dates=[]

    dict_folder_id_list_edit_times={}

    cont =0
    effective_cont=0
    for list_row in reader:

       try:
         cont +=1
         list_date=list_row[1].split("-")      #  2015-05-21
         list_time=list_row[2].split(":")      # 12:00:01
         
         year=int(list_date[0])        
         month=int(list_date[1])    
         day=int(list_date[2])
         
         hour=int(list_time[0])
         minute=int(list_time[1])
         sec=int(list_time[2])   
         
         date=dt.datetime(year, month, day, hour, minute, sec)
         
         actor_id=list_row[3]
         action=list_row[7]
         file_ext=list_row[9]
         
         if file_ext in list_interesting_file_types:
            effective_cont +=1
            shared_folder=list_row[11]
            sf_file_path_id=list_row[16]            
            file_unique_id= shared_folder+ sf_file_path_id
            
            
            list_all_dates.append(date)

            
            print cont #, date, actor_id, action, file_ext
            
            try:
                dict_types_files_count[file_ext] += 1
            except KeyError:
                dict_types_files_count[file_ext] =1



            try:
                dict_types_actions_count[action]  +=1
            except KeyError:
                dict_types_actions_count[action]  =1

            try:
                dict_actors_num_actions[actor_id] +=1
            except KeyError:
                dict_actors_num_actions[actor_id] =1




            try:
                if actor_id not in dict_file_id_list_actors[file_unique_id]:
                    dict_file_id_list_actors[file_unique_id].append(actor_id)

            except KeyError:
                dict_file_id_list_actors[file_unique_id]=[]               
                dict_file_id_list_actors[file_unique_id].append(actor_id)



            try:
                dict_file_id_num_actions[file_unique_id] +=1
            except KeyError:
                dict_file_id_num_actions[file_unique_id] =1




            try:
                dict_folder_id_num_actions[shared_folder] +=1
            except KeyError:
                dict_folder_id_num_actions[shared_folder] =1


  

            try:
                if actor_id not in dict_folder_id_list_actors[shared_folder]:
                    dict_folder_id_list_actors[shared_folder].append(actor_id)
            except KeyError:
                dict_folder_id_list_actors[shared_folder]=[]                
                dict_folder_id_list_actors[shared_folder].append(actor_id)





            try:
                dict_folder_id_list_edit_times[shared_folder].append(date)
            except KeyError:
                dict_folder_id_list_edit_times[shared_folder]=[]
                dict_folder_id_list_edit_times[shared_folder].append(date)



         if  cont == sample_size:
            break

            
       except IndexError: pass




     

    list_number_actors_per_file=[]  
    for key in dict_file_id_list_actors:
        num_actors=len(dict_file_id_list_actors[key])              
        list_number_actors_per_file.append(num_actors)

    path_name_h="../Results/Hist_num_actors_per_file_selecting_some_file_types"+testing_string+".dat"
    histograma_gral.histogram(list_number_actors_per_file, path_name_h)



    
    list_number_actions_per_file=[]   
    for key in dict_file_id_num_actions:
        num_actions=dict_file_id_num_actions[key]     
        list_number_actions_per_file.append(num_actions)
        
    path_name_h="../Results/Hist_num_actions_per_file_selecting_some_file_types"+testing_string+".dat"
    histograma_gral.histogram(list_number_actions_per_file, path_name_h)





    list_num_actions_per_actor=[]
    for key in dict_actors_num_actions:
        num= dict_actors_num_actions[key]
        list_num_actions_per_actor.append(num)

    path_name_h="../Results/Hist_num_actions_per_actor_selecting_some_file_types"+testing_string+".dat"
    histograma_gral.histogram(list_num_actions_per_actor, path_name_h)




    list_num_actions_per_folder=[]
    for key in  dict_folder_id_num_actions:
        num = dict_folder_id_num_actions[key]
        list_num_actions_per_folder.append(num)

    path_name_h="../Results/Hist_num_actions_per_folder_selecting_some_file_types"+testing_string+".dat"
    histograma_gral.histogram(list_num_actions_per_folder, path_name_h)


    filename_pickle="../Results/Dict_folder_id_num_actions_selecting_some_file_types.pickle"
    pickle.dump(dict_folder_id_num_actions, open(filename_pickle, 'wb'))









    list_number_actors_per_folder=[]    
    dict_folder_id_num_actions={}
    for key in dict_folder_id_list_actors:
        num=len(dict_folder_id_list_actors[key])        
        list_number_actors_per_folder.append(num)
        dict_folder_id_num_actions[key]=num

    path_name_h="../Results/Hist_num_actors_per_folder_selecting_some_file_types"+testing_string+".dat"
    histograma_gral.histogram(list_number_actors_per_folder, path_name_h)


    filename_pickle="../Results/Dict_folder_id_num_actors_selecting_some_file_types.pickle"
    pickle.dump(dict_folder_id_num_actions, open(filename_pickle, 'wb'))





    list_time_spans=[]
    list_time_intervals=[]
    for folder in  dict_folder_id_list_edit_times:

        lista_dates=sorted(dict_folder_id_list_edit_times[folder])
        first=lista_dates[0]
        last=lista_dates[-1]
       
        total_time_span=(last-first).days
        list_time_spans.append(total_time_span)


        ii=1
        while ii < len(lista_dates):

            today=lista_dates[ii]
            time_interval= (today-first).days       
            list_time_intervals.append(time_interval)
            ii +=1

      

    path_name_h="../Results/Hist_time_intervals_between_edits_folder_selecting_some_file_types"+testing_string+".dat"
    histograma_gral.histogram(list_time_intervals, path_name_h)



    path_name_h="../Results/Hist_time_spans_editing_history_folder_selecting_some_file_types"+testing_string+".dat"
    histograma_gral.histogram(list_time_spans, path_name_h)



  
   ##################

    #print  "number of unique actor_ids:", len(dict_actors_num_actions),"\n\n"
    print >> file1, "number of unique actor_ids:", len(dict_actors_num_actions),"\n\n"

    

    #print  "number of unique folder_ids:", len(dict_folder_id_num_actions),"\n\n"
    print  >> file1, "number of unique folder_ids:", len(dict_folder_id_num_actions),"\n\n"


    #print  "number of unique file_folder_ids:", len(dict_file_id_list_actors),"\n\n"
    print >> file1, "number of unique file_ids:", len(dict_file_id_list_actors),"(where file_id = unique_folder_id + unique_file_id)\n\n"
    


    #print "types of actions, number (and fraction) of occurrences:\n"
    print >> file1, "types of actions, number (and fraction) of occurrences:\n"

   
    norm=0.
    for llave in dict_types_actions_count:
        norm += dict_types_actions_count[llave]    

    sorted_list = sorted(dict_types_actions_count.items(), key=operator.itemgetter(1))
    sorted_list.reverse()

    for item in sorted_list:
       # print item[0], item[1], item[1]/norm
        print >> file1, item[0], item[1], item[1]/norm

    print >> file1,"\n\n\n"






    #print "types of files, number (and fraction) of occurrences:\n"
    print >> file1,"types of files, number (and fraction) of occurrences:\n"

    norm=0.
    for key in dict_types_files_count:        
         norm += dict_types_files_count[key]
   
    sorted_list = sorted(dict_types_files_count.items(), key=operator.itemgetter(1))
    sorted_list.reverse()

    for item in sorted_list:
        #print item[0], item[1], item[1]/norm
        print >> file1, item[0], item[1], item[1]/norm






    lista=sorted(list_all_dates)
    print "\n\nfirst date:", lista[0], " and last:",lista[-1]
      #print "  WITHOUT SORTING first date:", list_all_dates[0], " and last:",list_all_dates[-1]
    print >> file1, "first date:", lista[0], " and last:",lista[-1]

 
    ########
   
    print "final count:",cont, "total number of entries in the datafile:  29883243 "
    print >> file1, "final count:",cont, "total number of entries in the datafile:  29883243 "
    print "effective number records included (with the right type of file ext):",  effective_cont
    print >> file1, "effective number records included (with the right type of file ext):",  effective_cont



    file1.close()
    print "\nwritten:",name1



######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "

