# -*- coding: utf-8 -*-
# PROCEDURE: Read from list of URLS -> grab first two paragraphs
import datetime
from bs4 import BeautifulSoup
from os import path, pardir, makedirs, chdir, remove, getcwd
import requests

start_time = datetime.datetime.now().time().isoformat()

master_address = "http://en.wikipedia.org/wiki/List_of_academic_disciplines_and_sub-disciplines"

output_path = path.join(getcwd(), 'wikipedia')

if not path.exists(output_path):
    makedirs(output_path)

chdir(output_path)

page = requests.get(master_address,timeout=30)
souper = BeautifulSoup(page.content)
souper = str(souper)

file_name = "List_of_academic_disciplines_and_sub_disciplines.html"

open(file_name,'w').write(souper)
print "FILE SAVED"

print ""
print ""
print "Start time: " + str(start_time)
print "End time: " + str(datetime.datetime.now().time().isoformat())
print ""
print ""