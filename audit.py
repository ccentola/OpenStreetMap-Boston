
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "boston_massachusetts.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "Rd.": "Road",
			"Rd": "Road",
			"rd": "Road",
			"St.": "Street",
			"St": "Street",
			"ST": "Street",
			"st": "Street",
			"St,": "Street",
			"Street.": "Street",
			"Ave": "Avenue",
			"Ave.": "Avenue",
			"ave": "Avenue",
			"rd.": "Road",
			"Pkwy": "Parkway",
			"Pkwy.": "Parkway",
			"place": "Place",
			"HIghway": "Highway",
			"Sq.": "Square",
			"Ct": "Court",
			"Pl": "Place",
			"Sedgwick": "Sedgwick Street",
			"Newbury": "Newbury Street",
			"Boylston": "Boylston Street",
			"Brook": "Brook Parkway",
			"Cambridge": "Cambridge Center",
			"Charles Street South": "Charles Street",
			"Fenway": "Yawkey Way",
			"Hampshire": "Hampshire Street",
			"Boylston Street, 5th Floor": "Boylston Street",
			"Boston Providence Turnpike": "Boston Providence Highway",
			"Holland": "Holland Albany Street",
			"Sidney Street, 2nd Floor": "Sidney Street",
			"First Street, 18th Floor": "First Street",
			"First Street, Suite 1100": "First Street",
			"Webster Street, Coolidge Corner": "Webster Street",
			"Avenue Louis Pasteur": "Louis Pasteur Avenue Louis Pasteur",
			"Kendall Square - 3": "Kendall Square",
			"Faneuil Hall": "Faneuil Hall Market Street",
			"LOMASNEY WAY, ROOF LEVEL": "Lomasney Way",
			"1629 Cambridge St": "Cambridge Street",
			"1 Kendall Sq.": "Kendall Square",
			"Suite 1702": "Franklin Street"
			}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

def audit_zipcode(osmfile):
	"""Identifies zip-codes in our data not conforming to the Boston "02" standard"""
	osm_file = open(osmfile, "r")
	zip_codes = {}
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == "node" or elem.tag == "way":
			for tag in elem.iter("tag"):
				if tag.attrib['k'] == "addr:postcode" and not tag.attrib['v'].startswith('02'):
					if tag.attrib['v'] not in zip_codes:
						zip_codes[tag.attrib['v']] = 1
					else:
						zip_codes[tag.attrib['v']] += 1
	return zip_codes


bos_street_types = audit(OSMFILE)
pprint.pprint(dict(bos_street_types))

def update_name(name, mapping, regex):
	"""Update street names not identified in CREATED to their counterparts in mapping"""
    m = regex.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = re.sub(regex, mapping[street_type], name)

    return name

for street_type, ways in bos_street_types.iteritems():
    for name in ways:
		# Use update_name function to return name adjustments
        better_name = update_name(name, mapping, street_type_re)
        print name, "=>", better_name

zipcodes = audit_zipcode(OSMFILE)
for zip in zipcodes:
	print zip, zipcodes[zip]
