#!/usr/bin/env python
#########################################################################
#
# Command-line tool for downloading IPR data
# http://www.iprpraha.cz/clanek/1313/otevrena-data-open-data (in Czech)
#
# 2016 (c) by Martin Jakl (OSGeoREL CTU in Prague)
#
# Licence: GNU GPL v2+
#
#########################################################################


import sys
import urllib2
import xmltodict
import argparse



def main(alike=None, crs=None):
    xml_file = "http://opendata.iprpraha.cz/feed.xml"
    data = parse_xml(xml_file)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--alike" ,type=str,                     help = "search name title alike given string")
    parser.add_argument("--crs"   ,type=str,default = "S-JTSK",  help = "specife coordinate system(WGS or S-JTSK > default = S-JTSK")
    parser.add_argument("--form"  ,type=str,default = "shp",     help = "specife file format (default = *.shp)")
    args = parser.parse_args()

    if args.crs == "5514": args.crs="WGS"
    if args.crs == "4326": args.crs="S-JTSK"

    if args.alike:
        for item in data['feed']['entry']:
            if (args.alike in item['title']):
                item_print(item, args.crs,args.form)
    else:
        for item in data['feed']['entry']:
            xml_item = downXML(item)
            print item['title']
            
           
def item_print(item, crs, file_format):
    xml_item = downXML(item)
    if '10 cm' in item['title']:
        print (' -- too much links to display !! --')
    if '10 cm' not in item['title']:
        subdata = parse_xml(xml_item)
        subitems_Links(subdata['feed']['entry'], crs,file_format)


def subitems_Links(subdata, crs,file_format):
    if isinstance(subdata, list):
        for item in subdata:
            if (crs in item['category']['@label']):
                    print_subItem(item,file_format)
    else:
        item = subdata
        print_subItem(item,file_format)


def print_subItem(item,file_format):
    for links in item['link']:
        if file_format in links['@type']:
            print links['@href']


def downXML(data):
    for item in data['link']:
        if item['@title'] in ('download', 'Download'):
            xml_file = item['@href']
    return xml_file


def parse_xml(xml_file):
    try:
        fd = urllib2.urlopen(xml_file)
    except urllib2.URLError as e:
        sys.exit('{}'.format(e))

    obj = xmltodict.parse(fd.read())
    fd.close()
    return obj

main()
