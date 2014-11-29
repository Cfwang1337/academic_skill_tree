# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import requests
from os import path, chdir, getcwd, listdir
import csv
import string

start_time = datetime.datetime.now().time().isoformat()

chdir(path.join(getcwd(),"wikipedia"))

csvs_dict = dict(
    ancillary = "ancillary_list_fields.csv",
    main = "main_list_fields.csv",
)

main_csv_list = csvs_dict['main']

master_subject_list = []

with open(main_csv_list,"rU") as f:
    vals = csv.DictReader(f)
    for i in vals:
        master_subject_list.append(str(i['field']).lower())

chdir(path.join(getcwd(),"linkage_pages"))

c = csv.writer(open("interrelations.csv",'wb'))
c.writerow(['field','interrelation'])

for file in listdir(getcwd()):
    if file.endswith('.html'):
        file_name = str(file).replace('.html',"")
        file_blob = ""
        for element in file_name.split('_')[:-1]:
            file_blob = file_blob + element + " "
        file_blob = str(file_blob[:-1].lower())
        if file_blob in master_subject_list:
            souper = open(file,'r').read()
            souper = BeautifulSoup(souper)
            for link in souper.findAll('ul')[0].findAll('li'):
                linktext = str(filter(lambda x: x in string.printable, link.getText().replace('(links)',"").strip().lower())).strip()
                if linktext in master_subject_list:
                    print file_blob + "|"+ linktext
                    c.writerow([file_blob,linktext])