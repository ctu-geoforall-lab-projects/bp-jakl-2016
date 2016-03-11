import sys
import urllib2
import xmltodict

def main():
	xml_file = "http://opendata.iprpraha.cz/feed.xml"
	data = parse_xml(xml_file)
	alike = ''
	if alike:
		for item in data ['feed']['entry']:
			exist=0 
			if (alike in item['title']):
				exist=1
				item_print(item)
	else:
		for item in data['feed']['entry']: 
			item_print(item)
	return 0


def item_print(item):
	print '\n',item['title']
	if 'Ortofoto' in item['title']: 
		print (' -- too much links to display !! --')
	if 'Ortofoto' not in item['title']: 
		xml_item = downXML(item)
		subdata = parse_xml(xml_item)
		#print '    ',xml_item  # nebude
		subitems_Links_print(subdata)


def subitems_Links_print(subdata):
	if isinstance(subdata['feed']['entry'],list):
		for item in subdata['feed']['entry']: 
			print '     ',item['category']['@label']
			for links in item['link']:
				print '          ',links['@href']#,'	',links['@title']
	else:
		print '          ',subdata['feed']['entry']['category']['@label']
		for links in subdata['feed']['entry']['link']:
			print '          ',links['@href']#,'	',links['@title']
	return 0 



def downXML(data):
	for item in data['link']:
		if item['@title'] in ('download','Download'):
			xml_file = item['@href']
			#print xml_file

	return xml_file



def parse_xml(xml_file):
	try:
		fd = urllib2.urlopen(xml_file)
	except urllib2.URLError as e:
		sys.exit(e)
        
	obj = xmltodict.parse(fd.read())
	fd.close()
	return obj


main()


