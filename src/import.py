import sys
import urllib2
import xmltodict

def main(alike,datum):
	xml_file = "http://opendata.iprpraha.cz/feed.xml"
	data = parse_xml(xml_file)
	if alike:
		for item in data ['feed']['entry']:
			if (alike in item['title']):
				item_print(item,datum)
	else:
		for item in data['feed']['entry']: 
			item_print(item,datum)


def item_print(item,datum):
	print '\n',item['title']
	xml_item = downXML(item)
	print xml_item
	if '10 cm' in item['title']: 
		print (' -- too much links to display !! --')
	if '10 cm' not in item['title']: 
		subdata = parse_xml(xml_item)
		subitems_Links(subdata['feed']['entry'],datum)



def subitems_Links(subdata,datum):
	if isinstance(subdata,list):
		if datum:
			for item in subdata: 
				if (datum in item['category']['@label']):
					print_subItem(item)
		else:
			for item in subdata: 
				print_subItem(item) 
	else: 
		item = subdata
		print_subItem(item)


def print_subItem(item):
	print '     ',item['category']['@label']
	for links in item['link']:
		print '          ',links['@href'],'	',links['@title']



def downXML(data):
	for item in data['link']:
		if item['@title'] in ('download','Download'):
			xml_file = item['@href']
	return xml_file


def parse_xml(xml_file):
	try:
		fd = urllib2.urlopen(xml_file)
	except urllib2.URLError as e:
		sys.exit(e)
        
	obj = xmltodict.parse(fd.read())
	fd.close()
	return obj



if __name__ == "__main__":
	if len(sys.argv) == 1:
		alike = ''
		datum = ''
	elif len(sys.argv) ==2:
		alike = sys.argv[1]
		datum = ''
	else:
		alike = sys.argv[1]
		datum = sys.argv[2]

	sys.exit(main(alike,datum))


main(alike,datum)


