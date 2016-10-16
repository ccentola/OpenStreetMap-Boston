#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import os

# Set the current working directory
os.getcwd()
os.chdir('C:/Users/CRCIII/Desktop/P3')

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        try:
            users.add(element.attrib['uid'])
        except KeyError:
            pass
        element.clear() # clear memory to speed up processing
    return users

users = process_map('boston_massachusetts.osm')
print len(users) # print the count of users who edited the file
