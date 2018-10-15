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





    ##########  output file for master dict:
    outpute_file="../Results/Master_dict_faculty_by_name.pickle"



 
    ### Input files
    ####### HEADER:  First Name,Last Name,Title,Email,University,School/college,Department(s),Url
          #             0         1         2     3      4           5             6           7  
    
                 #Alberto,Abadie,"Professor, Economics & IDSS",..,Massachusetts Institute of Technology,"Institute for Data, Systems, and Society",IDSS,https://idss.mit.edu/people/

    ####### Number of lines in the original file:     wc -l 1987
    


    list_university_files=["100.Yeshiva_University.csv", "40.Rutgers_The_State_University_of_New_Jersey.csv", "71.University_of_Houston.csv", "10.Columbia_University.csv", "41.Stanford_University.csv", "72.University_of_Illinois_Chicago.csv", "11.Cornell_University.csv", "42.Stony_Brook_University.csv", "73.University_of_Illinois_Urbana_Champaign.csv", "12.Dartmouth_College.csv", "43.Syracuse_University.csv", "74.University_of_Iowa.csv", "13.Drexel_University.csv", "44.Temple_University.csv", "75.University_of_Kansas.csv", "14.Duke_University.csv", "45.Texas_AM_University.csv", "76.University_of_Maryland.csv", "15.Emory_University.csv", "46.The_University_of_Tennessee_Knoxville.csv", "77.University_of_Massachusetts.csv", "16.Florida_State_University.csv", "47.The_University_of_Texas_at_Austin.csv", "78.University_of_Miami.csv", "17.George_Washington_University.csv", "48.Tufts_University.csv", "79.University_of_Michigan.csv", "18.Georgetown_University.csv", "49.University_at_Buffalo.csv", "7.Case_Western_Reserve_University.csv", "19.Georgia_Institute_of_Technology.csv", "4.Brown_University.csv", "80.University_of_Minnesota.csv", "1.Arizona_State_University.csv", "50.University_of_Alabama.csv", "81.University_of_Nebraska.csv", "20.Harvard_University.csv", "51.University_of_Arizona.csv", "82.University_of_New_Hampshire.csv", "21.Indiana_University_Bloomington.csv", "52.University_of_Arkansas.csv", "83.University_of_New_Mexico.csv", "22.Iowa_State_University.csv", "53.University_of_California_Berkeley.csv", "84.University_of_North_Carolina_Chapel Hill.csv", "23.Johns_Hopkins_University.csv", "54.University_of_California_Davis.csv", "85.University_of_Notre_Dame.csv", "24.MD_Anderson_Cancer_Center_University_of_Texas.csv", "55.University_of_California_Irvine.csv", "86.University_of_Pennsylvania.csv", "25.Massachusetts_Institute_of_Technology.csv", "56.University_of_California_Los_Angeles.csv", "87.University_of_Pittsburgh.csv", "26.Michigan_State_University.csv", "57.University_of_California_Riverside.csv", "88.University_of_Rochester.csv", "27.New_York_University.csv", "58.University_of_California_San_Diego.csv", "89.University_of_South_Florida.csv", "28.North_Carolina_State_University.csv", "59.University_of_California_San_Francisco.csv", "8.City_University_of_New_York.csv", "29.Northeastern_University.csv", "5.California_Institute_of_Technology.csv", "90.University_of_Southern_California.csv", "2.Baylor_College_of_Medicine.csv", "60.University_of_California_Santa_Barbara.csv", "91.University_of_Utah.csv", "30.Northwestern_University.csv", "61.University_of_California_Santa_Cruz.csv", "92.University_of_Vermont.csv", "31.Ohio_State_University.csv", "62.University_of_Central_Florida.csv", "93.University_of_Virginia.csv", "32.Oregon_Health _ Science_University.csv", "63.University_of_Chicago.csv", "94.University_of_Washington.csv", "33.Oregon_State_University.csv", "64.University_of_Cincinnati.csv", "95.University_of_Wisconsin_Madison.csv", "34.Pennsylvania_State_University.csv", "65.University_of_Colorado.csv", "96.Vanderbilt_University.csv", "35.Princeton_University.csv", "66.University_of_Connecticut.csv", "97.Virginia_Polytechnic_Institute_and_State_University.csv", "36.Purdue_University.csv", "67.University_of_Delaware.csv", "98.Washington_University_Saint_Louis.csv", "37.Rensselaer_Polytechnic_Institute.csv", "68.University_of_Florida.csv", "99.Yale_University.csv", "38.Rice_University.csv", "69.University_of_Georgia.csv", "9.Colorado_State_University.csv", "39.Rockefeller_University.csv", "6.Carnegie_Mellon_University.csv", "3.Boston_University.csv", "70.University_of_Hawaii.csv"]


######  print out the header
for item in df:
    print item


#  list_university_files=["10.University_of_California_San_Diego_removed_duplicates.csv.xlsx","24.Ohio_State_University_removed_duplicates.csv.xlsx","11.University_of_California_Los_Angeles_removed_duplicates.csv.xlsx","25.University_of_Illinois_Urbana_Champaign_removed_duplicates.csv.xlsx","12.Columbia_University_removed_duplicates.csv.xlsx","26.University_of_North_Carolina_Chapel_Hill_removed_duplicates.csv.xlsx","13.Duke_University_removed_duplicates.csv.xlsx","27.Boston_University_removed_duplicates.csv(1).xlsx","14.University_of_Washington_removed_duplicates.csv.xlsx","27.Boston_University_removed_duplicates.csv.xlsx","15.Princeton_University_removed_duplicates.csv.xlsx","28.Georgia_Institute_of_Technology_removed_duplicates.csv.xlsx","16.Carnegie_Mellon_University_removed_duplicates.csv.xlsx","2.University_of_Chicago_removed_duplicates.csv.xlsx","17.University_of_Rochester_removed_duplicates.csv.xlsx","30.Northwestern_University_removed_duplicates.csv.xlsx","18.Arizona_State_University_removed_duplicates.csv.xlsx","3.Stanford_University_removed_duplicates.csv.xlsx","19.Pennsylvania_State_University_removed_duplicates.csv.xlsx","4.University_of_California_Berkeley_removed_duplicates.csv.xlsx","1.Harvard_University_removed_duplicates.csv.xlsx","5.Massachusetts_Institute_of_Technology_removed_duplicates.csv.xlsx","20.Cornell_University_removed_duplicates.csv.xlsx","6.Johns_Hopkins_University_removed_duplicates.csv.xlsx","21.New_York_University_removed_duplicates.csv.xlsx","7.University_of_Michigan_removed_duplicates.csv.xlsx","22.University_of_Minnesota_removed_duplicates.csv.xlsx","8.Michigan_State_University_removed_duplicates.csv.xlsx","23.Temple_University_removed_duplicates.csv.xlsx","9.Yale_University_removed_duplicates.csv.xlsx"]





                 # Arizona_State_University.csv", "George_Washington_University.csv", "Tufts_University.csv", "University_of_Illinois_Chicago.csv", "Baylor_College_of_Medicine.csv", "Georgia_Institute_of_Technology.csv", "University_at_Buffalo.csv", "University_of_Illinois_Urbana_Champaign.csv", "Boston_University.csv", "Harvard_University.csv", "University_of_Arizona.csv", "University_of_Kansas.csv", "Brown_University.csv", "Indiana_University_Bloomington.csv", "University_of_California_Berkeley.csv", "University_of_Maryland.csv", "California_Institute_of_Technology.csv", "Iowa_State_University.csv", "University_of_California_Davis.csv", "University_of_Massachusetts.csv", "Carnegie_Mellon_University.csv", "Johns_Hopkins_University.csv", "University_of_California_Irvine.csv", "University_of_Michigan.csv", "Case_Western_Reserve_University.csv", "Massachusetts_Institute_of_Technology.csv", "University_of_California_ Los_Angeles.csv", "University_of_Minnesota.csv", "City_University_of_New_York.csv", "MD_Anderson_Cancer_Center_University_of_Texas.csv", "University_of_California_Riverside.csv", "University_of_Nebraska.csv", "Colorado_State_University.csv", "Michigan_State_University.csv", "University_of_California_San_Diego.csv", "University_of_New_Hampshire.csv", "Columbia_University.csv", "New_York_University.csv", "University_of_California_San_Francisco.csv", "University_of_North_Carolina_Chapel_Hill.csv", "Cornell_University.csv", "North_Carolina_State University .csv", "University_of_California_Santa_Barbara.csv", "University_of_Notre_Dame.csv", "Dartmouth_College.csv", "Northeastern_University.csv", "University_of_California_Santa_Cruz.csv", "University_of_Pennsylvania.csv", "Drexel_University.csv", "Stony_Brook_University.csv", "University_of_Central_Florida.csv", "University_of_Pittsburgh.csv", "Duke_University.csv", "Temple_University.csv", "University_of_Chicago.csv", "University_of_Rochester.csv", "Emory_University.csv", "Texas_A&M_University.csv", "University_of_Georgia.csv", "University_of_Southern_California.csv", "Florida_State_University.csv", "The_University_of_Tennessee_Knoxville.csv", "University_of_Hawaii.csv", "University_of_South_Florida.csv", "Georgetown_University.csv", "The_University_of_Texas_at_Austin.csv", "University_of_Houston.csv", "University_of_Utah.csv"]


    print "# universities:", len(list_university_files)

    print  "","\t","University","\t","num. rows","\t", "num. emails","\t", "num. missing emails"



    master_dict_faculty_by_email={}
    master_dict_faculty_by_name={}
    
    cont_missing_emails_tot=0
    cont_tot=0
    list_emails_tot=[]
    for item in list_university_files:
        
   
        name_file="../Data/Vinu_University_Sheets/Final_List_Top_100_University/"+item
        csvfile=open(name_file, 'rb')
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')            
        next(reader, None)   ##### to skip the header
             


        list_emails=[]
        cont_missing_emails=0
        cont =0
        for list_row in reader:
             
          cont +=1
          cont_tot +=1
          if cont >1:  # i skip the header

            #  First Name	Last Name	Title	Email	University	School/college	Department(s)	Url
            #      0               1              2       3         4               5               6            7
            
            first_name = list_row[0].title() #"hello world".title() returns: 'Hello World'
            last_name = list_row[1].title()
            name = first_name + " " + last_name
            title = list_row[2]
            email = list_row[3]
            university =  list_row[4]
            school_college =  str(list_row[5])
            dept =  str(list_row[6])
            url =  list_row[7]


            tuple_title_dept_school_univ=(title,dept,school_college, university)
            
            if ".." in email :   # no email info
                cont_missing_emails_tot +=1
                cont_missing_emails +=1
             
            else:
                   
                if email not in list_emails:
                    list_emails.append(email)
                if email not in list_emails_tot:
                    list_emails_tot.append(email)



            
            try:
                master_dict_faculty_by_name[name]
            except KeyError:
                master_dict_faculty_by_name[name]={}


            master_dict_faculty_by_name[name]["first_name"]=first_name   # it will be useful for the matching to also have indep. info on this
            master_dict_faculty_by_name[name]["last_name"]=last_name
            
            master_dict_faculty_by_name[name]["university"]= university

            master_dict_faculty_by_name[name]["tuple_lastname_univ"]= (last_name,university) # it will be useful for the matching to also have indep. info on this

          

            try:
                master_dict_faculty_by_name[name]["afiliation"].append(tuple_title_dept_school_univ)
            except KeyError:
                master_dict_faculty_by_name[name]["afiliation"]=[]
                master_dict_faculty_by_name[name]["afiliation"].append(tuple_title_dept_school_univ)



            try:
                master_dict_faculty_by_name[name]["email"].append(email)
            except KeyError:
                master_dict_faculty_by_name[name]["email"]=[]
                master_dict_faculty_by_name[name]["email"].append(email)
                
            

                
            try:
                master_dict_faculty_by_name[name]["department"].append(dept)
                master_dict_faculty_by_name[name]["title"].append(title)
                master_dict_faculty_by_name[name]["school_college"].append(school_college)
                master_dict_faculty_by_name[name]["url"].append(url)

                    
            except KeyError:
                master_dict_faculty_by_name[name]["department"]=[]
                master_dict_faculty_by_name[name]["department"].append(dept)
                
                master_dict_faculty_by_name[name]["title"]=[]
                master_dict_faculty_by_name[name]["title"].append(title)
                
                master_dict_faculty_by_name[name]["school_college"]=[]
                master_dict_faculty_by_name[name]["school_college"].append(school_college)
                
                master_dict_faculty_by_name[name]["url"]=[]
                master_dict_faculty_by_name[name]["url"].append(url)
                
            



        print item, "\t",cont, "\t",len(set(list_emails)), "\t",cont_missing_emails

            


    cont_legit_diff_records=0
    cont_false_entries_multiple_entries=0 
    cont_people_with_multiple_entries=0
    for name in  master_dict_faculty_by_name:
             
        if len(master_dict_faculty_by_name[name]["afiliation"]) >1:                
            master_dict_faculty_by_name[name]["afiliation"] = list(set(master_dict_faculty_by_name[name]["afiliation"]))
                

        if len(master_dict_faculty_by_name[name]["email"]) >1:                
            master_dict_faculty_by_name[name]["email"] = list(set(master_dict_faculty_by_name[name]["email"]))
                

        if len(master_dict_faculty_by_name[name]["title"])  > 1  or len(master_dict_faculty_by_name[name]["department"]) >1   or len(master_dict_faculty_by_name[name]["school_college"]) >1  or len(master_dict_faculty_by_name[name]["url"]) >1  :
                
            cont_people_with_multiple_entries  += 1

            
            aux_list_school_college=list(set(master_dict_faculty_by_name[name]["school_college"]))
            aux_list_title=list(set(master_dict_faculty_by_name[name]["title"]))
            aux_list_department=list(set(master_dict_faculty_by_name[name]["department"]))
            
            if  len(aux_list_title)==1  and   len(aux_list_department)==1  and   len(aux_list_school_college)==1:
                cont_false_entries_multiple_entries += 1

        cont_legit_diff_records  += len(master_dict_faculty_by_name[name]["afiliation"])

        



        
    print
    print "num. rows:", cont_tot
    print "num. unique people in dict:", len(master_dict_faculty_by_name)
    print "num. people with multiple records:", cont_people_with_multiple_entries
    print "num. entries false people with multiple records:", cont_false_entries_multiple_entries,"(only difference in url field)"
    print  "num. distinct emails:",len(list_emails_tot),   float(len(list_emails_tot))/cont_tot
    print "num. legit multiple records:", cont_legit_diff_records
    print "num. records missing emails:", cont_missing_emails_tot 


    cont_people_with_missing_emails=0
    for name in master_dict_faculty_by_name:
        lista_email=master_dict_faculty_by_name[name]["email"]
        if ".." in lista_email:
            if len(lista_email) <2:
               # print master_dict_faculty_by_name[name]["email"]            
                cont_people_with_missing_emails += 1

    print "num. people without emails:", cont_people_with_missing_emails , cont_people_with_missing_emails/float(len(master_dict_faculty_by_name))


  
    pickle.dump(master_dict_faculty_by_name, open(outpute_file, 'wb'))
    print "\n written pickle file:",outpute_file
    
######################################
######################################
######################################
if __name__ == '__main__':
   # if len(sys.argv) > 1:
    #    graph_filename = sys.argv[1]
   
        main()
    #else:
     #   print "Usage: python script.py "
