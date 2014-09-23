# -*- coding: utf-8 -*-
# PROCEDURE: Read from list of URLS -> grab first two paragraphs
import re
import urllib2
from bs4 import BeautifulSoup
from os import path, pardir, makedirs, chdir, remove, getcwd
import requests

master_address = "http://en.wikipedia.org/wiki/List_of_academic_disciplines_and_sub-disciplines"

output_path = path.join(getcwd(), 'wikipedia')

if not path.exists(output_path):
    makedirs(output_path)

