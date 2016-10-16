#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import os

# Set the current working directory
os.getcwd()
os.chdir('C:/Users/CRCIII/Desktop/P3')

def count_tags(filename):
    """Create a dictionary of nodes from a file. Increment the node count for every new instance of the same node."""

	# initialize defaultdict to avoid a KeyError; capture new keys not in dictionary
    tags = defaultdict(int)

    # iterate through each node element and increment the dictionary value for that node.tag key
    for event, node in ET.iterparse(filename):
        if event == 'end':
            tags[node.tag] += 1
        # clear node to speed up processing
        node.clear()
    return tags

tags = count_tags('boston_massachusetts.osm')
pprint.pprint(tags)
