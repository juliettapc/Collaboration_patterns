import pandas as pd
import numpy as np
# from tqdm import tqdm
# from tqdm import tnrange, tqdm_notebook
# from time import sleep
import scipy
import operator
from IPython.core.display import display,HTML
from tqdm import tnrange, tqdm_notebook

try:
    import cPickle as pickle     #it is faster than pickle!
except:
    import pickle





    
fields = ['author_id','year','author_name','affiliation','total_pubs']  # i only upload certain fields
#fields = ['author_id','uid','seq','year','author_name','affiliation','total_pubs']


#path_wos_win='C:\\Users\\julietta\\Work\\Dropbox_studies\\Data\\WoS_data\\Disambiguated_authors\\'
path_wos_linux='/home/juliaponcela/at_NICO/Dropbox_collaboration_patterns/Data/WoS_data/Disambiguated_authors/'

#%time df_disamb_wos_test=pd.read_csv(path_wos_linux+'only_USA_active_years_2000-2015_filtered_WoS_file.tsv', usecols=fields, sep="\t")#, nrows=100000)
%time df_disamb_wos_test=pd.read_csv(path_wos_linux+'only_USA_active_years_2005-2015_filtered_WoS_file_simplified.tsv', usecols=fields, sep="\t")#, nrows=100000)

df_disamb_wos_test.rename(columns={'affiliation':'affiliations'}, inplace=True) 
df_disamb_wos_test.rename(columns={'author_name':'author_names'}, inplace=True) 
#df_disamb_wos_test.rename(columns={'seq':'seqs'}, inplace=True) 
