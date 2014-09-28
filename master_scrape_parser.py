# -*- coding: utf-8 -*-
# PROCEDURE: Read from list of URLS -> grab first two paragraphs
import time
import datetime
import re
from bs4 import BeautifulSoup
import itertools
from multiprocessing import Pool
from os import path, pardir, makedirs, chdir, remove, getcwd
import csv

start_time = datetime.datetime.now().time().isoformat()

source_path = path.join(getcwd(),"wikipedia")
chdir(source_path)

file_name = "List_of_academic_disciplines_and_sub_disciplines.html"


souper = open(file_name,'r').read()
souper = BeautifulSoup(souper)

output_path = path.join(getcwd(),"wikipedia_output")

if not path.exists(output_path):
    makedirs(output_path)

chdir(output_path)

#print souper

all_tds = souper.findAll('td',{'style':'width:50%; text-align:left; vertical-align:top;'})

#c = csv.writer(open("main_list_fields.csv", "wb"))
#c.writerow(["level1","level2","level3","url"])

for td in all_tds:
    #print td
    mains = td.findAll('ul')
    for main in mains:
        print main


print ""
print ""
print "Start time: " + str(start_time)
print "End time: " + str(datetime.datetime.now().time().isoformat())
print ""
print ""