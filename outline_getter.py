# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import requests
from os import path, chdir, getcwd
import csv

start_time = datetime.datetime.now().time().isoformat()

source_path = path.join(getcwd(),"wikipedia")
chdir(source_path)

file_name = "List_of_academic_disciplines_and_sub_disciplines.html"

souper = open(file_name,'r').read()
souper = BeautifulSoup(souper)

outline_list = []
master_list = []
deduplicate_list = []

all_urls = souper.findAll('a')

for url_frag in all_urls:
    url = url_frag.attrs.get('href')
    #print url
    name = str(url)
    if name[:6] == "/wiki/" and "#" not in name and ":" not in name:
        name = url.split('/wiki/')[-1]
        text_name = url_frag.getText()
        name = name.replace("_"," ")
        url = "http://en.wikipedia.org" + url
        try:
            if "Outline" in name and name not in deduplicate_list:
                item_dict = dict(
                    name=name,
                    url=url,
                )
                deduplicate_list.append(name)
                outline_list.append(item_dict)
            if str(name) == str(text_name) and "Outline" not in name and name not in deduplicate_list:
                print name,"|",text_name,"|",url
                item_dict = dict(
                    name=name,
                    url=url,
                )
                master_list.append(item_dict)
                deduplicate_list.append(name)
        except:
            pass

c = csv.writer(open("outline_list_fields.csv", "wb"))
c.writerow(["field","link",])

print len(outline_list)


for item in outline_list:
    c.writerow([item['name'],item['url']])
    url = item['url']
    name = item['name']
    page = requests.get(url,timeout=30)
    souper = BeautifulSoup(page.content)
    souper = str(souper)
    filename = str(name.replace(' ','_')) + ".html"
    open(filename,'w').write(souper)
    print filename,"FILE SAVED"

print len(master_list)

c = csv.writer(open("main_list_fields.csv", "wb"))
c.writerow(["field","link",])

for item in master_list:
    c.writerow([item['name'],item['url']])



print ""
print ""
print "Start time: " + str(start_time)
print "End time: " + str(datetime.datetime.now().time().isoformat())
print ""
print ""