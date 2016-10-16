#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
addr = re.compile(r'^addr:')
addr_too_much = re.compile(r"addr:.+:.+")
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
	"""Transforms the shape of our data into a list of dictionaries"""
    node = defaultdict(list) # using defaultdict to simplify pos and node_refs insertion
    if element.tag == "node" or element.tag == "way":
        created = {}
        address = {}
        for key, value in element.attrib.iteritems():
            if key in CREATED:
                # tags in CREATED go to a sub dictionary
                created[key] = value
            elif key == "lat":
                node['pos'].insert(0, float(value))
            elif key == "lon":
                node['pos'].append(float(value))
            else:
                node[key] = value
        # handle the tags key value pairs
        for child in element.iter("tag"):
            tag_key = child.attrib['k']
            tag_value = child.attrib['v']
            if addr.search(tag_key):
                # ignore second ":"
                if addr_too_much.search(tag_key):
                    continue
                else:
                    address[tag_key[5:]] = tag_value
            else:
                node[tag_key] = tag_value
        # handle nodes
        for child in element.iter("nd"):
            node['node_refs'].append(child.attrib['ref'])

        node['type'] = element.tag
        if address:
            node['address'] = address
        node['created'] = created
        return dict(node)

    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

process_map('boston_massachusetts.osm')
