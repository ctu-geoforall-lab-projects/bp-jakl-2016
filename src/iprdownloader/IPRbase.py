import sys
import urllib2
import xmltodict

class IprDownloader:
    def __init__(self):
        pass

    def filter(self, alike, crs, file_format):
        xml_file = "http://opendata.iprpraha.cz/feed.xml"
        data = self.parse_xml(xml_file)

        self.itemURLs = []
        self.IprItems = []
        if alike:
            for item in data['feed']['entry']:
                if (alike in item['title']):
                    self.itemURLs += [self.item_print(item, crs, file_format)]
        else:
            for item in data['feed']['entry']:
                xml_item = self.downXML(item)
                self.IprItems += [item['title']]


    def item_print(self, item, crs, file_format):
        xml_item = self.downXML(item)
        if '10 cm' in item['title']:
            pass
        else:
            subdata = self.parse_xml(xml_item)
            return self.subitems_Links(subdata['feed']['entry'], crs, file_format)


    def subitems_Links(self, subdata, crs, file_format):
        if isinstance(subdata, list):
            for item in subdata:
                if (crs in item['category']['@label']):
                    return self.print_subItem(item,file_format)
        else:
            item = subdata
            if (crs in item['category']['@label']):
                return self.print_subItem(item,file_format)


    def print_subItem(self, item,file_format):
        for links in item['link']:
            if file_format in links['@type']:
#                print links['@title'] ,'  \t', links['@href']#        will be deleted
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

        
    def download(self,outdir):
        import os

        if outdir.endswith('/'):
            pass
        else:
            outdir += '/'

        if (os.path.isdir(outdir)):
            pass
        else:
            try:
                os.makedirs(outdir)
            except OSError:
                print ' Cannot create file direcotry !! '
        self.outdir = outdir
#        print outdir#

        self.filename = []

        for itemURL in self.itemURLs:
            itemfile = urllib2.urlopen(itemURL)
            filename = itemURL.split('/')[-1]
            self.filename += [filename]
             
#            print "downloading " + filename

            filepath = os.path.join(outdir,filename)
            with open(filepath,"wb") as output:
#                output.write(itemfile.read())
                while True:
                    data = itemfile.read(32768)
                    if data:
                        output.write(data)
                    else:
                        break


    def print_items(self):
#        self.
        for item in self.IprItems:
            print item
