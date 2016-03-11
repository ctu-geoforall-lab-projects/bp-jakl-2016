import sys
import urllib2
import xmltodict

def main():
    xml_file = "http://opendata.iprpraha.cz/feed.xml"	
		
    data = parse_xml(xml_file)	
    for item in data['feed']['entry']: 
        print '\n',item['title']
	if 'Ortofoto' in item['title']: print ('too much XMLs !!')
	if 'Ortofoto' not in item['title']: 
		xml_item = downXML(item)
		subdata = parse_xml(xml_item)
		if isinstance(subdata['feed']['entry'],list):
			for subitem in subdata['feed']['entry']:
				print '     ',subitem['category']['@label']
				for links in subitem['link']:
					print '          ',links['@href']
		else:
			print '     ',subdata['feed']['entry']['category']['@label']
			for links in subdata['feed']['entry']['link']:
				print '          ',links['@href']

    return 0



def downXML(data):
    for item in data['link']:
	if item['@title'] in ('download','Download'): 
	    xml_file = item['@href']
    return (xml_file)


def parse_xml(xml_file):
    try:
        fd = urllib2.urlopen(xml_file)
    except urllib2.URLError as e:
        sys.exit(e)
        
    obj = xmltodict.parse(fd.read())
    fd.close()
    return obj
main()
