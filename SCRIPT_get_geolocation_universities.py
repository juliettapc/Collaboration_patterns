 
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
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle
    
import unicodedata
import networkx as nx
import itertools
import seaborn as sns   ### https://seaborn.pydata.org/tutorial/categorical.html
import time  






##### for getting geolocation data  and to calculate distance between two geolocations
import requests
import json
import geopy.distance   


# Urban-Rural codes:

# Metropolitan Counties*	
# 1	In large metro area of 1+ million residents
# 2	In small metro area of less than 1 million residents

# Nonmetropolitan Counties	
# 3	Micropolitan area adjacent to large metro area
# 4	Noncore adjacent to large metro area
# 5	Micropolitan area adjacent to small metro area
# 6	Noncore adjacent to small metro area and contains a town of at least 2,500 residents
# 7	Noncore adjacent to small metro area and does not contain a town of at least 2,500 residents
# 8	Micropolitan area not adjacent to a metro area
# 9	Noncore adjacent to micro area and contains a town of at least 2,500 residents
# 10	Noncore adjacent to micro area and does not contain a town of at least 2,500 residents
# 11	Noncore not adjacent to metro or micro area and contains a town of at least 2,500 residents
# 12	Noncore not adjacent to metro or micro area and does not contain a town of at least 2,500 residents










def main():



    #waiting= "NO"




    path="/home/julia/Dropbox_collaborations/Data/Dropbox/"
    input_file='Dropbox_datafile_may22_2017_modified.csv'
    df_original=pd.read_csv(path+input_file, sep=',',na_values=["NAN","-1","null"],low_memory=False, parse_dates=['folder_creation_date','date_last_change']) # set header=0 if i wanna pass it my own list of header names
    df_original = df_original.drop('Unnamed: 0', 1)
    print df_original.shape
    df_original=df_original.drop_duplicates(subset=["folder_id","user_id"])  # i drop any duplicates by those two indeces
    print df_original.shape
    
    print len(df_original.email_domain.unique())



# Rural Urban Continuum Code



# 1	Counties in metro areas of 1 million population or more	Metro Counties
# 2	Counties in metro areas of 250,000 to 1 million population	Metro Counties
# 3	Counties in metro areas of fewer than 250,000 population	Metro Counties
# 4	Urban population of 20,000 or more, adjacent to a metro area	Nonmetro Counties
# 5	Urban population of 20,000 or more, not adjacent to a metro area	Nonmetro Counties
# 6	Urban population of 2,500 to 19,999, adjacent to a metro area	Nonmetro Counties
# 7	Urban population of 2,500 to 19,999, not adjacent to a metro area	Nonmetro Counties
# 8	Completely rural or less than 2,500 urban population, adjacent to a metro area	Nonmetro Counties
# 9	Completely rural or less than 2,500 urban population, not adjacent to a metro area	Nonmetro Counties




  #  filename_zip_code_density="/home/julia/Dropbox_collaborations/Data/Rural_Urban_zip_codes/Zipcode-ZCTA-Population-Density.csv"
   # df_zipcode_density=pd.read_csv(filename_zip_code_density, sep=',')#,usecols=["Zip-ZCTA","2010_Population","Land-Sq-Mi","Density_Per_Sq_Mile"])    #, header=None)
    #df_zipcode_density = df_zipcode_density.rename(columns={'Zip-ZCTA': 'zip'})     
    #print df_zipcode_density.shape
    #print "file read:",filename_zip_code_density




    filename_zip_rural_urban="/home/julia/Dropbox_collaborations/Data/Rural_Urban_zip_codes/2006_Complete_Excel_RUCA_file_simplified.csv"   #(41901, 3)
    df_zipcode_rural_urban=pd.read_csv(filename_zip_rural_urban, sep='\t')
    print df_zipcode_rural_urban.shape
    print "file read:",filename_zip_rural_urban




    filename_rucc_codes="/home/julia/Dropbox_collaborations/Data/Rural_Urban_zip_codes/RUCC_codes_simplified.csv"
    df_rucc_codes=pd.read_csv(filename_rucc_codes, sep='\t',usecols=["Rural_Urban_Continuum_Code","Description"])    #, header=None)
    print df_rucc_codes.shape
    print "file read:",filename_rucc_codes







    df_zip_merged_rucc = pd.merge(df_zipcode_rural_urban, df_rucc_codes, how='left',on='Rural_Urban_Continuum_Code')   
    print df_zip_merged_rucc.shape    
    print "urban rural zip files merged\n\n"
   


    name="/home/julia/Dropbox_collaborations/Data/Rural_Urban_zip_codes/merged_zip_RUCC.csv"
    df_zip_merged_rucc.to_csv(name, sep=',')
    print "written:", name








    filename_univ_new="/home/julia/Dropbox_collaborations/Data/University_rankings_and_names/merged_domains_new_clean.csv"
    df_univ_names_new=pd.read_csv(filename_univ_new, sep=',',usecols=["email_domain","simplified_domain","University_Name","Cleaned_university_name","Country"])# [email_domain,University_Name,Country] #, header=None)
    
    print df_univ_names_new.shape       
    print "read",filename_univ_new



    


######### transform the data from unicode to strings
    for c in df_univ_names_new.columns:#["email_domain","simplified_domain","University_Name","Cleaned_university_name","Country"]:
        df_univ_names_new[c] =df_univ_names_new[c].astype(str)#.str.split(',')
        print c, "done"




  

    df_merged = pd.merge(df_original, df_univ_names_new, how='left',on='email_domain')   
    print df_merged.shape   
    print "merged df original with university names file"






    #### i combine the incomplete dict and online queries:
    try:
        path="/home/julia/Dropbox_collaborations/Results/"
        filename="dict_univ_country_geolocation_incomplete.pickle"
        file = open(path+filename,'r')
        dict_univ_country_geolocation = pickle.load(file)
        len(dict_univ_country_geolocation.keys())
        
        print "partial dict found:", filename
    
    except:
        dict_univ_country_geolocation={} 
        print "dict not found, starting from scratch"





    try:
        
        path="/home/julia/Dropbox_collaborations/Results/"
        filename="list_places_with_ZERO_or_UNKNOWN_RESULTS_incomplete.pickle"
        file = open(path+filename,'r')
        list_places_with_zero_or_unknown_results = pickle.load(file)
        print "partial dict found:", filename

    except :
        list_places_with_zero_or_unknown_results=[]




    url_string="http://maps.googleapis.com/maps/api/geocode/json?address="  # this way i access the google api that gives me directly the location of any address or city etc




  #  if waiting== "YES":
   #     print "waiting........."
    #    time.sleep(54000)  # wait for 15h
     #   print "  done waiting!"





    tot_attempts=4

    list_not_found=[]




    df_merged['Geolocation'] = df_merged.apply (lambda row: get_geolocation(row, dict_univ_country_geolocation,tot_attempts,list_places_with_zero_or_unknown_results),axis=1)
   # df_merged['Geolocation'] = df_merged.apply (lambda row: get_geolocation(row),axis=1)
    print "done!\n"
    
    print "len of dict:",len(dict_univ_country_geolocation.keys())




    path="/home/julia/Dropbox_collaborations/Results/"
    filename="dict_univ_country_geolocation_YAY.pickle"
    with open(path+filename,'wb') as f:
        pickle.dump(dict_univ_country_geolocation, f)
    print "written:",path+filename, "!!"




    path="/home/julia/Dropbox_collaborations/Results/"
    filename="list_places_with_ZERO_or_UNKNOWN_RESULTS.pickle"
    with open(path+filename,'wb') as f:
        pickle.dump(list_places_with_zero_or_unknown_results, f)
    print "written:",path+filename, "!!"


   

    list_keys_to_pop=[]
    for key in dict_univ_country_geolocation:
        try:
            math.isnan(dict_univ_country_geolocation[key])
            print key,"     ", dict_univ_country_geolocation[key]
            list_keys_to_pop.append(key)
        
        except: pass
        
    print "# keys popped due to empty values in geolocation dict:",len(set(list_keys_to_pop))









    
    
    
    df_merged['zip'] = df_merged.Geolocation.apply(get_zip)
     
    df_merged['lat'] = df_merged.Geolocation.apply(get_lat)
    df_merged['long'] = df_merged.Geolocation.apply(get_long)
    
    print "i got zip, lat and long as indept. columns"
    
    




    new_merge_name="/home/julia/Dropbox_collaborations/Data/Dropbox/Dropbox_new_oct2017_added_univ_country_geolocation.xlsx"
    writer = pd.ExcelWriter(new_merge_name, engine='xlsxwriter',options={'strings_to_urls': False})
# Convert the dataframe to an XlsxWriter Excel object.
    df_merged.to_excel(writer, sheet_name='Sheet1')
## OJO! hay url muy largas que hacen que el sistema se cuelgue (solucion: no permitirle que las considere url, sino simplemente str)

# Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print "writen:", new_merge_name






    
     ################# OJOOOOOOOOOOOOOOO! NO PUEDO HACER MERGING MY ZIP CODE DIRECTLY, BECAUSE SOME INTERNATIONAL ZIP CODES GET MISTAKEN BY US ZIP CODES!!! Also, because i only have RUCC codes about the US
    
    df_US=df_merged[df_merged["Country"]=="United States"]
    df_merged_with_zip_density_rucc = pd.merge(df_US, df_zip_merged_rucc, how='left',on='zip') 
    print "merged between master file and zip urban rural file done."







   # new_merge_name="/home/julia/Dropbox_collaborations/Data/Dropbox/Dropbox_datafile_may22_2017_modified_added_univ_country_geolocation_RUCC_only_US_YAY.csv"
    new_merge_name="/home/julia/Dropbox_collaborations/Data/Dropbox/Dropbox_new_oct2017_added_univ_country_geolocation_RUCC_only_US_YAY.csv"
    df_merged_with_zip_density_rucc.to_csv(new_merge_name, sep=',', encoding='utf-8')
    print "written:", new_merge_name



#    name="/home/julia/Dropbox_collaborations/Data/Dropbox/Dropbox_datafile_may22_2017_modified_added_univ_country_geolocation_RUCC_only_US_YAY.pickle"    
    name="/home/julia/Dropbox_collaborations/Data/Dropbox/Dropbox_new_oct2017_added_univ_country_geolocation_RUCC_only_US_YAY.pickle"
    with open(name,'wb') as f:
        pickle.dump(df_merged_with_zip_density_rucc, f)

    print "written:", name









    print df_merged_with_zip_density_rucc.ru2003.value_counts()
    #print df_merged_with_zip_density_rucc.zip.value_counts()
    print df_merged_with_zip_density_rucc.shape




    for key in sorted(dict_univ_country_geolocation.keys()):
        print key, "     ------",dict_univ_country_geolocation[key]








###################################
########################################




def get_geolocation (input_df, dict_univ_country_geolocation,tot_attempts,list_places_with_zero_or_unknown_results):


    url_string="http://maps.googleapis.com/maps/api/geocode/json?address="  # this way i access the google api that gives me directly the location of any address or city etc


        #string_location=input_df.University_Country
    string_location=str(input_df.Cleaned_university_name)+ ", " + str(input_df.Country)


    try:
        latlong= dict_univ_country_geolocation[string_location]  # if i have already calculated that geolocation before
            #print "geolocation already in dict"
    except KeyError:

        latlong = np.nan


        if string_location   not in list_places_with_zero_or_unknown_results:  # i dont search for a place if i already know that google api doesnt give me any results (as not o waste my daily requests)
            try:

                attempts = 0
                success = False

                while success != True  and  attempts < tot_attempts: 
                    #data = requests.get(url_string+string_location+"&key="+my_google_api_key  )  # i make the request for a given site

                    data = requests.get(url_string+string_location  )  # i make the request for a given site
                    jdict = json.loads(data.text)        # it conveninently parses the info using the fact that it is in JSON (it is like a big dictionary of dictionaries)                                            

                    status=jdict['status']





                    if status == "OVER_QUERY_LIMIT":  # if too many queries per second
                        time.sleep(5)    # waiting time in seconds
                        success = False   
                        attempts +=1

                        if attempts == tot_attempts:
                          # send an alert as this means that the daily limit has been reached

                            print "Daily limit has been reached"
                            print jdict

                            path="/home/julia/Dropbox_collaborations/Results/"
                            filename="dict_univ_country_geolocation_incomplete.pickle"
                            with open(path+filename,'wb') as f:
                                pickle.dump(dict_univ_country_geolocation, f)
                            print "written:",path+filename





                            path="/home/julia/Dropbox_collaborations/Results/"
                            filename="list_places_with_ZERO_or_UNKNOWN_RESULTS_incomplete.pickle"
                            with open(path+filename,'wb') as f:
                                pickle.dump(list_places_with_zero_or_unknown_results, f)
                            print "written:",path+filename, "!!"




		            print "\nhit ctrl+C to kill the process  or wait for hours...... :("

                            time.sleep(54000)  # wait for 15h

                           




                    elif status=='OK':

                        zip_code=""
                        
                        lat = jdict['results'][0]['geometry']['location']['lat']
                        lng = jdict['results'][0]['geometry']['location']['lng']


                        try:                            
                            for item in  jdict['results'][0]['address_components']:
                                if item['types']== ['postal_code']:
                                    zip_code=item['long_name']                                    
                                   # print item, zip_code
                                    break                               
                        except IndexError:   pass                         
                            #print jdict
                           # raw_input()


                        latlong = (lat, lng)                 
                        latlong=str(latlong)+" "+zip_code                            
                        dict_univ_country_geolocation[string_location]=latlong     

                        success = True 




                    else:# if it cant find the geolocation of the string :      'status': u'ZERO_RESULTS',  OR  'status': u'UNKNOWN_ERROR'

                        list_places_with_zero_or_unknown_results.append(string_location)



                        print jdict , string_location,"added  to list of places with zero or unknown results"
                        success = True 
                       









            except KeyError:  # if it cant find the geolocation of the string

                print string_location,"couldnt be found"
                print jdict








        return latlong










####################################
 ##################################




#############################
#########################





def get_geolocation_by_dict (input_df):
    
    #string_location=input_df.University_Country
    string_location=str(input_df.Cleaned_university_name)+ ", " + str(input_df.Country)
    
    
    try:
        latlong= dict_univ_country_geolocation[string_location]  # if i have already calculated that geolocation before
        #print "geolocation already in dict"
    except KeyError:

        latlong = np.nan
        
     

    return latlong




##################################
##########################





def get_zip(cadena):
    
    try:
        new_cadena=cadena.split(") ")[1]        
        new_cadena=int(new_cadena)
        
    except :  # for NANs  OR NAMES
        new_cadena=np.nan
    return new_cadena

###############################


def get_lat (cadena):   # (lat, lng) zip  -----     example:      (40.3439888, -74.6514481) 08544   
    try:
        new_cadena=cadena.split(") ")[0].split(", ")[0].strip("(")
    except AttributeError:  # for NANs  (which are Floats, and dont have .slitp!)
        new_cadena=np.nan
    return new_cadena
    
######

def get_long (cadena):   # (lat, lng)              
    try:
        new_cadena=cadena.split(") ")[0].split(", ")[1]
    except AttributeError:  # for NANs  (which are Floats, and dont have .slitp!)
        new_cadena=np.nan
    return new_cadena
    
    




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



