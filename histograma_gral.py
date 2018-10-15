import numpy as np

def histogram(lista, path_name_h):

    file = open(path_name_h,'wt')
    cont=0
    cumulat=0.
    for item in np.bincount(lista):   # way faster than using my function!!  
        if item >0:
         
            print >> file, cont,  float(item)/len(lista), item,  1. - float(cumulat)/len(lista), float(cumulat)/len(lista), len(lista)- cumulat, cumulat
         
        cont +=1 
        cumulat = cumulat + item    
    file.close()
    print "written: ", path_name_h





##########################################

def histograma_mio(lista, path_name_h, maximum):
        


    if maximum!=None:

        maximum+=2

        Prob=[0]*int(maximum)
        Cumul_prob=[0]*int(maximum)
    else:        
        Prob=[0]*50000
        Cumul_prob=[0]*50000


    norm=0.
    for item in lista:
        #print "item:",item
        Prob[int(item)]+=1.
        for i in range(len(Cumul_prob)):
            if i<= item:
                Cumul_prob[i]+=1.
        norm+=1.

    #print "\n",name_h,"max:",max(lista),"min:",min(lista)
  #  print Prob
   
   
    #file = open("histogram_"+name_h+".dat",'wt')
    file = open(path_name_h,'wt')
    for i in range(len(Prob)):  
        if Prob[i] !=0:
            print >> file, i, Prob[i]/norm, Prob[i], Cumul_prob[i]/norm, Cumul_prob[i]
    file.close()


    print "written: ", path_name_h

##########################################

def histograma_posit_neg(lista, path_name_h):
        
    minimum= min(lista)-1
    maximum=max(lista)+1
    print lista

    dict_value_probability={}
    dict_value_cumulative_probability={}


    value=minimum
    while value <= maximum:
        dict_value_probability[value] =0.
        dict_value_cumulative_probability[value]= 0.
        value +=1.



    norm=0.
    for item in lista:       
        try:
            dict_value_probability[int(item)]+=1.      
        except KeyError:
            dict_value_probability[int(item)] =0.

        for key  in dict_value_cumulative_probability:
            if key<= item:
                try:
                    dict_value_cumulative_probability[key]+=1.
                except KeyError:
                    dict_value_cumulative_probability[key] = 0.
        norm+=1.

 

    file = open(path_name_h,'wt')
    for key in sorted (dict_value_probability):
        if dict_value_probability[key] !=0.:
            print >> file, key,dict_value_probability[key]/norm, dict_value_probability[key], dict_value_cumulative_probability[key]/norm, dict_value_cumulative_probability[key]
    file.close()


    print "written: ", path_name_h




##########################################


def histograma_return_list_freq(lista, path_name_h,maximum):
        

    if maximum!=None:

        maximum+=2

        Prob=[0]*int(maximum)
        Cumul_prob=[0]*int(maximum)
    else:        
        Prob=[0]*50000
        Cumul_prob=[0]*50000

     
    norm=0.
    for item in lista:
        #print "item:",item
        Prob[int(item)]+=1.
        for i in range(len(Cumul_prob)):
            if i<= item:
                Cumul_prob[i]+=1.
        norm+=1.

    #print "\n",name_h,"max:",max(lista),"min:",min(lista)
  #  print Prob
   
   
    #file = open("histogram_"+name_h+".dat",'wt')
    file = open(path_name_h,'wt')
    for i in range(len(Prob)):  
        if Prob[i] !=0:
            print >> file, i, Prob[i]/norm, Prob[i], Cumul_prob[i]/norm, Cumul_prob[i]
    file.close()

   

    return Prob
