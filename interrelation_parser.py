# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import re
from os import path, chdir, getcwd, listdir
import csv
import string

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(filter(lambda x: x in string.printable, element))):
        return False
    return True

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

c = csv.writer(open("referenced_by.csv",'wb'))
c.writerow(['field','interrelation'])
b = csv.writer(open("interrelations.csv","wb"))
b.writerow(['field','interrelation','relation'])

for file in listdir(getcwd()):
    if file.endswith('.html'):
        file_name = str(file).replace('.html',"")
        file_blob = ""
        for element in file_name.split('_')[:-1]:
            file_blob = file_blob + element + " "
        file_blob = str(file_blob[:-1].lower())
        if file_blob in master_subject_list:
            with open(file,'r') as soup:
                souper = soup.read()
                souper = BeautifulSoup(souper)
                for link in souper.findAll('ul')[0].findAll('li'):
                    linktext = str(filter(lambda x: x in string.printable, link.getText().replace('(links)',"").strip().lower())).strip()
                    if linktext in master_subject_list:
                        c.writerow([file_blob,linktext])
                        b.writerow([file_blob,linktext,"referenced_by"])

c = csv.writer(open("references.csv",'wb'))
c.writerow(['field','interrelation'])

chdir("../main_pages")

for file in listdir(getcwd()):
    with open(file,'r') as soup:
        file_blob = file.split('/')[-1].replace('_',' ').lower()
        file_blob = file_blob.replace('.html',"")
        souper = soup.read()
        souper = BeautifulSoup(souper)
        text = souper.findAll(text=True)
        visible_text = filter(visible,text)
        for item in master_subject_list:
            if item.lower in visible_text or item in visible_text or item.title() in visible_text:
                c.writerow([file_blob,item.lower()])
                b.writerow([file_blob,item.lower(),"refers_to"])





print ""
print ""
print "Start time: " + str(start_time)
print "End time: " + str(datetime.datetime.now().time().isoformat())
print ""
print ""