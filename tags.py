!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import os

# Set the current working directory
os.getcwd()
os.chdir('C:/Users/CRCIII/Desktop/P3')

# Create the three regular expressions we are checking for
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        if re.search(lower, element.attrib['k']):
            keys['lower'] += 1
        elif re.search(lower_colon, element.attrib['k']):
            keys['lower_colon'] += 1
        elif re.search(problemchars, element.attrib['k']):
            # print out any values with problematic characters
			keys['problemchars'] += 1
            # print element
            print element.attrib['k']
        else:
            keys['other'] += 1

    return keys

def process_map(filename):
    # initialize dictionary
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        # clear element to speed up processing
        element.clear()
    return keys

keys = process_map('boston_massachusetts.osm')
len(keys)
pprint.pprint(keys)
