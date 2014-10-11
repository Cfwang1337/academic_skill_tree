# -*- coding: utf-8 -*-
# PROCEDURE: Read from list of URLS -> grab first two paragraphs
import time
import datetime
import re
from bs4 import BeautifulSoup
import itertools
from multiprocessing import Pool
import requests
from os import path, pardir, makedirs, chdir, remove, getcwd, listdir
import csv

start_time = datetime.datetime.now().time().isoformat()

source_path = path.join(getcwd(),"wikipedia")
chdir(source_path)

source_contents = listdir(source_path)

print source_contents

master_list = []
deduplicate_list = []

for item in source_contents:
    if item.endswith('.html'):
        item_name = item.replace('.html',"")
        item_name = item_name.replace('Outline_of_',"")
        item_name = item_name.title()
        souper = open(item,'r').read()
        souper = BeautifulSoup(souper)
        #print souper
        all_urls = souper.findAll('a')

        for url_frag in all_urls:
            url = url_frag.attrs.get('href')
            #print url
            try:
                name = str(url)
                if name[:6] == "/wiki/" and "#" not in name and ":" not in name:
                    name = url.split('/wiki/')[-1]
                    text_name = url_frag.getText()
                    name = name.replace("_"," ")
                    url = "http://en.wikipedia.org" + url
                    try:
                        if str(name) == str(text_name) and "Outline" not in name and name not in deduplicate_list:
                            print name,"|",text_name,"|",url
                            item_dict = dict(
                                item_name=item_name,
                                name=name,
                                url=url,
                            )
                            master_list.append(item_dict)
                            deduplicate_list.append(name)
                    except:
                        pass
            except:
                pass

print len(master_list)

c = csv.writer(open("ancillary_list_fields.csv", "wb"))
c.writerow(["origin","field","link",])

for item in master_list:
    c.writerow([item['item_name'],item['name'],item['url']])


print ""
print ""
print "Start time: " + str(start_time)
print "End time: " + str(datetime.datetime.now().time().isoformat())
print ""
print ""