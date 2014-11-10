# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import requests
from os import path, chdir, getcwd, makedirs
import csv

start_time = datetime.datetime.now().time().isoformat()

source_path = path.join(getcwd(),"wikipedia")
chdir(source_path)

csvs_dict = dict(
    ancillary = "ancillary_list_fields.csv",
    main = "main_list_fields.csv",
)

main_csv_list = csvs_dict['main']

master_subject_list = []

with open(main_csv_list,"rU") as f:
    vals = csv.DictReader(f)
    for i in vals:
#        print i['field']
        master_subject_list.append(i['link'].split('/')[-1])

output_path = path.join(getcwd(),"linkage_pages")

if not path.exists(output_path):
    makedirs(output_path)

chdir(output_path)

for field in master_subject_list:
    index = 0
    url = "http://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/" + field + "&namespace=0&limit=500&hideredirs=1"
    print url
    page = requests.get(url,timeout=30)
    souper = BeautifulSoup(page.content)
    filename = field + "_" + str(index) + ".html"
    open(filename, 'w').write(str(souper))
    for numb in range(0,len(souper.findAll('a'))):
        next_link = souper.findAll('a')[numb].attrs.get('href')
        next_text = souper.findAll('a')[numb].getText()
        if next_text == "next 500":
#            print next_link
#            print next_text
            break
    while next_text == "next 500":
        tail_frag = next_link.split('limit=500')[-1]
#        print tail_frag
        url = "http://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/" + field + "&namespace=0&limit=500&hideredirs=1" + tail_frag
        print url
        page = requests.get(url,timeout=30)
        souper = BeautifulSoup(page.content)
        index = index + 1
        filename = field + "_" + str(index) + ".html"
        open(filename, 'w').write(str(souper))
        for numb in range(0,len(souper.findAll('a'))):
            next_link = souper.findAll('a')[numb].attrs.get('href')
            next_text  = souper.findAll('a')[numb].getText()
            if next_text == "next 500":
#                print next_link
#                print next_text
                break


print ""
print ""
print "Start time: " + str(start_time)
print "End time: " + str(datetime.datetime.now().time().isoformat())
print ""
print ""