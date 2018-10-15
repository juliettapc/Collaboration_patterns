'''
File: name_checker.py
Author: Adam Pah
Description:
Checks name input against 
'''

#Standard path imports
from __future__ import division, print_function
import argparse
from time import sleep

#Non-standard imports
from google import search
import pandas as pd

#Global directories and variables

def main(args):
    #open the files
    cfile = open('correct_names.csv', 'a')
    ifile = open('incorrect_names.csv', 'a')
    ufile = open('url_failures.csv', 'a')
    #Trackers
    tot_correct = 0
    url_failure = 0
    correct_names, incorrect_names = [], []
    #Read in teh dataframe
    df = pd.read_csv(args.infile)
    #Iterate through faculty names
    for name, email in df.loc[:, [args.name_column, args.email_column]].values:
        correct = False
        try:
            #Try the name first
            for url in search(name, stop = 5):
                #Check to see if the check url is in one of the other urls
                if args.check_url in url:
                    correct = True
                    break
                #Do the email search if it isn't true yet
                if correct != True:
                    sleep(3)
                    for url in search(email, stop = 5):
                        if args.check_url in url:
                            correct = True
                            break
            #Do the addition if the check is true
            if correct == True:
                tot_correct += 1
                print('%s,%s' % (name, email), file=cfile)
            else:
                print('%s,%s' % (name, email), file=ifile)
        except:
            url_failure += 1
            print('%s,%s' % (name, email), file=ufile)
            pass
        #sleep it out
        sleep(3)
    #close all the files
    cfile.close()
    ifile.close()
    ufile.close()
    #Print it out
    print('Total correct ', tot_correct)
    print('number timed out ', url_failure)
    print('Perc. correct ', tot_correct / df[args.email_column].count())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('infile', help = 'input result file')
    parser.add_argument('check_url', help = 'edu url for the appropriate url')
    parser.add_argument('-name_column', default = 'list_of_faculty_names_and_emails', help="column name of found faculty name")
    parser.add_argument('-email_column', default = 'Email', help="column name of found faculty name")
    args = parser.parse_args()
    main(args)
