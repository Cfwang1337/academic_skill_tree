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
link_list = []

with open(main_csv_list,"rU") as f:
    vals = csv.DictReader(f)
    for i in vals:
        master_subject_list.append(str(i['field']).lower())
        link_list.append(i['link'])

output_path = path.join(getcwd(),"main_pages")

if not path.exists(output_path):
    makedirs(output_path)

chdir(output_path)

for url in link_list:
    page = requests.get(url, timeout=30)
    souper = BeautifulSoup(page.content)
    filename = url.split('/')[-1] + ".html"
    with open(filename, 'w') as html_file:
        html_file.write(str(souper))

print ""
print ""
print "Start time: " + str(start_time)
print "End time: " + str(datetime.datetime.now().time().isoformat())
print ""
print ""