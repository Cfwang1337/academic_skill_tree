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

source_contents = [
    "Outline_of_the_humanities.html",
    "Outline_of_linguistics.html",
    "Outline_of_literature.html",
    "Outline_of_performing_arts.html",
    "Outline_of_music.html",
    "Outline_of_guitars.html",
    "Outline_of_dance.html",
    "Outline_of_theatre.html",
    "Outline_of_film.html",
    "Outline_of_visual_arts.html",
    "Outline_of_design.html",
    "Outline_of_drawing_and_drawings.html",
    "Outline_of_painting.html",
    "Outline_of_photography.html",
    "Outline_of_sculpture.html",
    "Outline_of_philosophy.html",
    "Outline_of_epistemology.html",
    "Outline_of_ethics.html",
    "Outline_of_aesthetics.html",
    "Outline_of_anarchism.html",
    "Outline_of_humanism.html",
    "Outline_of_logic.html",
    "Outline_of_religion.html",
    "Outline_of_Christianity.html",
    "Outline_of_Christian_theology.html",
    "Outline_of_Islam.html",
    "Outline_of_Judaism.html",
    "Outline_of_Buddhism.html",
    "Outline_of_Hinduism.html",
    "Outline_of_Sikhism.html",
    "Outline_of_atheism.html",
    "Outline_of_social_science.html",
    "Outline_of_anthropology.html",
    "Outline_of_archaeology.html",
    "Outline_of_sinology.html",
    "Outline_of_economics.html",
    "Outline_of_human_sexuality.html",
    "Outline_of_geography.html",
    "Outline_of_cartography.html",
    "Outline_of_politics.html",
    "Outline_of_psychology.html",
    "Outline_of_parapsychology.html",
    "Outline_of_sociology.html",
    "Outline_of_criminal_justice.html",
    "Outline_of_futures_studies.html",
    "Outline_of_natural_science.html",
    "Outline_of_biology.html",
    "Outline_of_human_anatomy.html",
    "Outline_of_biochemistry.html",
    "Outline_of_biophysics.html",
    "Outline_of_biotechnology.html",
    "Outline_of_botany.html",
    "Outline_of_cell_biology.html",
    "Outline_of_ecology.html",
    "Outline_of_genetics.html",
    "Outline_of_nutrition.html",
    "Outline_of_neuroscience.html",
    "Outline_of_zoology.html",
    "Outline_of_chemistry.html",
    "Outline_of_organic_chemistry.html",
    "Outline_of_earth_science.html",
    "Outline_of_geology.html",
    "Outline_of_geophysics.html",
    "Outline_of_hydrology.html",
    "Outline_of_meteorology.html",
    "Outline_of_physics.html",
    "Outline_of_astronomy.html",
    "Outline_of_combinatorics.html",
    "Outline_of_mathematics.html",
    "Outline_of_algebra.html",
    "Outline_of_calculus.html",
    "Outline_of_geometry.html",
    "Outline_of_computer_science.html",
    "Outline_of_databases.html",
    "Outline_of_artificial_intelligence.html",
    "Outline_of_robotics.html",
    "Outline_of_statistics.html",
    "Outline_of_probability.html",
    "Outline_of_agriculture.html",
    "Outline_of_architecture.html",
    "Outline_of_ergonomics.html",
    "Outline_of_finance.html",
    "Outline_of_information_technology.html",
    "Outline_of_marketing.html",
    "Outline_of_theology.html",
    "Outline_of_education.html",
    "Outline_of_engineering.html",
    "Outline_of_computer_engineering.html",
    "Outline_of_journalism.html",
    "Outline_of_radio.html",
    "Outline_of_television_broadcasting.html",
    "Outline_of_the_Internet.html",
    "Outline_of_public_relations.html",
    "Outline_of_law.html",
    "Outline_of_forensic_science.html",
    "Outline_of_healthcare_science.html",
    "Outline_of_dentistry_and_oral_health.html",
    "Outline_of_obstetrics.html",
    "Outline_of_psychiatry.html",
    "Outline_of_technology.html",
    "Outline_of_applied_science.html",
    "Outline_of_prehistoric_technology.html",
    "Outline_of_nanotechnology.html",  
    ]

#print source_contents

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

fail_list = []

for item in master_list:
    c.writerow([item['item_name'],item['name'],item['url']])
    url = item['url']
    name = item['name']
    page = requests.get(url,timeout=30)
    souper = BeautifulSoup(page.content)
    souper = str(souper)
    filename = str(name.replace(' ','_')) + ".html"
    file_path = source_path + "/" + filename
    if path.exists(file_path):
        print "Already exists"
        continue
    else:
        try:
            open(filename,'w').write(souper)
            print filename,"FILE SAVED"
        except:
            fail_list.append(filename)
            pass

print fail_list

print len(fail_list)

print ""
print ""
print "Start time: " + str(start_time)
print "End time: " + str(datetime.datetime.now().time().isoformat())
print ""
print ""