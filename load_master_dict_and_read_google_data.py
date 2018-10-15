#!/usr/bin/env python

'''
Created by Julia Poncela, on Ag. 2016

I read all Universities files (Vinu) and create a master dict with all info, keys are name+last name

'''

import datetime as dt
import csv
import pickle
import operator
#import histograma_gral


def main():



    ##########  input file for master dict:
    outpute_file="../Results/Master_dict_faculty_by_name.pickle"
    master_dict_faculty_by_name = pickle.load( open( outpute_file, "rb" ) )  # dict. of dicts.

    # example of one entry of the dict: 
    ###   Ane Marinez-lora {'first_name': 'An\xc3\xa9', 'last_name': 'Mar\xc3\xad\xc3\xb1ez-lora', 'title': ['Faculty'], 'url': ['http://www.psych.uic.edu/department-of-psychiatry-faculty-list'], 'university': 'University of Illinois Chicago', 'afiliation': [('Faculty', 'Psychiatry', 'College of Medicine', 'University of Illinois Chicago')], 'tuple_lastname_univ': ('Mar\xc3\xad\xc3\xb1ez-lora', 'University of Illinois Chicago'), 'department': ['Psychiatry'], 'school_college': ['College of Medicine'], 'email': ['amarinez-lora@psych.uic.edu']}

 
    list_universities_vinu=[]
    list_tuplas=[]
    for name in master_dict_faculty_by_name:
        list_tuplas.append(master_dict_faculty_by_name[name]['tuple_lastname_univ'])
        
        list_universities_vinu.append(master_dict_faculty_by_name[name]['university'])
   
    list_universities_vinu = list(set(list_universities_vinu))



    list_overlapping_univ=['University of North Carolina Chapel Hill', 'Brown University', 'University of California Santa Barbara', 'New York University', 'Massachusetts Institute of Technology', 'University of Florida', 'Stanford University', 'University of California Berkeley', 'University of Washington', 'Harvard University', 'University of Houston', 'Ohio State University', 'California Institute of Technology', 'Northwestern University', 'Rice University', 'Purdue University', 'Rensselaer Polytechnic Institute', 'Yale University', 'Georgetown University', 'University of Maryland', 'Vanderbilt University', 'University of Connecticut', 'Georgia Institute of Technology', 'University of Illinois Urbana Champaign', 'University of Southern California', 'University of Notre Dame', 'Columbia University', 'University of Minnesota', 'University of Michigan', 'University of Pennsylvania', 'University of Miami', 'University of Chicago', 'University of California Davis', 'University of Rochester', 'Cornell University', 'Pennsylvania State University', 'University of Virginia', 'The University of Texas at Austin', 'Duke University', 'Tufts University', 'Texas A&M University', 'George Washington University', 'Case Western Reserve University', 'Princeton University', 'University of California Irvine', 'Boston University', 'Johns Hopkins University', 'Emory University', 'University of California San Diego', 'Dartmouth College', 'Northeastern University', 'Yeshiva University']  #####  i get this list by running this same code once, in preparation



        
    ######## input file google scholar
    name_file="../Data/Google_scholar/gsfaculty_dept_16-08-01.csv"
    csvfile=open(name_file, 'rb')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
    next(reader, None)   ##### to skip the header
             
    ### google_id	name	h_index	  i10index	min_year	max_year	t_citations	max_citations	num_journals	mean_IF	max_IF
    #     0              1          2       3             4               5               6               7                8              9      10
              ### num_grants	t_funding	t_deflated_funding	school	college	department	department_url	num_faculty	update_date
              #      11           12               13                      14     15      16               17              18             19





     ## OJO!!! GOOGLE SCHOLAR TB TIENE RECORDS REPETIDOS (SI EL INVESTIGADOR ESTA AFILIADO A LOS DEPT. DISTINTOS, POR EJ.)

    list_universities_google=[]
    list_matching_records=[]
    max_num_records_for_matching=0
    cont =0
    list_ids=[]
    for list_row in reader:
        
        cont +=1        
        if cont >1:  # i skip the header

            google_id=list_row[0]
          
            
            list_name_complete = list_row[1].replace("."," ").replace("-","").split(" ")
            last_name=list_name_complete[-1].replace(" ","")  
            first_name=list_name_complete[0].replace(" ","") 
            name = first_name + " " + last_name

            
            middle_name=""
            if len(list_name_complete) >2:
                middle_name=list_name_complete[1]  ## if there is a middle initial, i ignore it for now
            

            school= list_row[14]    # this is usually the University


            ######## to standarize the name of certain schools between both datasets
            if "(MIT)" in  school:  
                school="Massachusetts Institute of Technology"

            elif "University of California, " in school:               
                school=school.replace(", "," ").replace("(UCLA)","")

            elif "Carnegie Mellon, " in school:               
                school=school.replace(" (CMU)","")

            elif "Austin" in school:               
                school="The University of Texas at Austin"

            elif "Urbana" in school:               
                school=school.replace(", "," ")


            elif "University of Maryland" in school:               
                school="University of Maryland"
           
            elif "University of Michigan" in school:               
                school="University of Michigan"
           
            elif "Chapel Hill" in school:               
                 school=school.replace(", "," ")

            elif "Pennsylvania State University" in school:               
                school="Pennsylvania State University"


            elif "Ohio State University" in school:   
                school="Ohio State University"


            elif "Purdue University" in school:   
                school="Purdue University"


            elif "University of Wisconsin" in school:   
                school=school.replace(", "," ")



            school.title()


                
            list_universities_google.append(school)

            if school in list_overlapping_univ:
                max_num_records_for_matching +=1

           
            tuple_lastname_univ=(last_name, school)           

            #if name in master_dict_faculty_by_name:   # matching by first + last names is not trustworthy (many false positives)!!!!!
               # list_matching_records.append(list_row)


            if google_id not in list_ids:
                list_ids.append(google_id)
                if tuple_lastname_univ in list_tuplas:
                    list_matching_records.append(list_row)
       

              #     master_dict_faculty_by_name[name]["afiliation"].append(tuple_title_dept_school_univ)



   
   
    list_universities_google = list(set(list_universities_google))
    print "num. records in google data:", cont, " unique:",len(list_ids),  "  num. matches:",len(list_matching_records)

    print "max. num of possible record overlap",max_num_records_for_matching
    print "num. univ. vinu:", len(list_universities_vinu), "  num. univ. google:", len(list_universities_google), "overlap:", len(set(list_universities_vinu) &set(list_universities_google)), set(list_universities_vinu) &set(list_universities_google)
   


    cont_not_found=0
    for item in list_matching_records:
        
        name_list= item[1].split(" ")     # example:   Minh Q. Phan

        last=name_list[-1].replace(" ","")
        first=name_list[0].replace(" ","")
        name=first+ " "+last
        try:
              master_dict_faculty_by_name[name]
        except KeyError:
                cont_not_found +=1


    print  "num matching records not found:",     cont_not_found


######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "
