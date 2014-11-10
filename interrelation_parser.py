# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import requests
from os import path, chdir, getcwd
import csv

start_time = datetime.datetime.now().time().isoformat()

source_path = path.join(getcwd(),"wikipedia")
chdir(source_path)

csvs_dict = dict(
    ancillary = "ancillary_list_fields.csv",
    main = "main_list_fields.csv",
)

output_path = path.join(getcwd(),"linkage_pages")

#get main subject linkages:

main_csv_list = csvs_dict['main']

master_subject_list = []

with open(main_csv_list,"rU") as f:
    vals = csv.DictReader(f)
    for i in vals:
        print i['field']
        master_subject_list.append(i['field'])
        linkage_page = requests.get()