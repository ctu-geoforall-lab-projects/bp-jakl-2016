import sys
import urllib2
import xmltodict

class IprDownloader:
    def __init__(self):
        pass

    def filter(self, alike, crs, file_format):
        xml_file = "http://opendata.iprpraha.cz/feed.xml"
        data = self.parse_xml(xml_file)

        self.links2down = []
        self.IprItems = []
        if alike:
            for item in data['feed']['entry']:
                if (alike in item['title']):
                    self.links2down += [self.item_print(item, crs, file_format)]
        else:
            for item in data['feed']['entry']:
                xml_item = self.downXML(item)
                self.IprItems += [item['title']]
#        print links2down
# print links to verify

    def item_print(self, item, crs, file_format):
        xml_item = self.downXML(item)
        if '10 cm' in item['title']:
            pass
#            print (' -- too much links to display !! --')
        if '10 cm' not in item['title']:
            subdata = self.parse_xml(xml_item)
            return self.subitems_Links(subdata['feed']['entry'], crs, file_format)


    def subitems_Links(self, subdata, crs, file_format):
        if isinstance(subdata, list):
            for item in subdata:
                if (crs in item['category']['@label']):
                    return self.print_subItem(item,file_format)
        else:
            item = subdata
            return self.print_subItem(item,file_format)


    def print_subItem(self, item,file_format):
        for links in item['link']:
            if file_format in links['@type']:
                return links['@href']


    def downXML(self, data):
        for item in data['link']:
            if item['@title'] in ('download', 'Download'):
                xml_file = item['@href']
        return xml_file

    def parse_xml(self, xml_file):
        try:
            fd = urllib2.urlopen(xml_file)
        except urllib2.URLError as e:
            sys.exit('{}'.format(e))
        obj = xmltodict.parse(fd.read())
        fd.close()
        return obj                

        
    def download(self):
        pass

    def print_items(self):
        print self.IprItems
