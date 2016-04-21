import sys
import urllib2
import xmltodict
import os
import zipfile
from osgeo import ogr,osr
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

class IprError(StandardError):
    pass

class IprDownloader:
    def __init__(self):
        pass

    def filter(self, alike, crs, file_format):
        xml_file = "http://opendata.iprpraha.cz/feed.xml"
        data = self.parse_xml(xml_file)

        self.itemURLs = []
        self.IprItems = []
        self.itemSizes= []

        if alike:
            for item in data['feed']['entry']:
                if (alike in item['title']): 
                    self.IprItems += [item['title']]
                    self.item_print(item, crs, file_format)
        else:
            for item in data['feed']['entry']:
                xml_item = self.downXML(item)
                self.IprItems += [item['title']]


    def item_print(self, item, crs, file_format):
        xml_item = self.downXML(item)
        subdata = self.parse_xml(xml_item)
        self.subitems_Links(subdata['feed']['entry'], crs, file_format)
        return 0


    def subitems_Links(self, subdata, crs, file_format):
        if isinstance(subdata, list):
#            for item in subdata:
            item = subdata[0]# this will download only first item with all data
            if (crs in item['category']['@label']):
                self.print_subItem(item,file_format)
        else:
            item = subdata
            if (crs in item['category']['@label']):
                self.print_subItem(item,file_format)
        return 0


    def print_subItem(self, item, file_format):
        if isinstance(item['link'], list):
            for links in item['link']:
                if file_format in links['@type']:
                    self.itemURLs += [links['@href']]
                    self.itemSizes += [links['@title']]
        else:
            links = item['link']
            if file_format in links['@type']:
                self.itemURLs += [links['@href']]
        return 0


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

        if (os.path.isdir(outdir)):
            pass
        else:
            try:
                os.makedirs(outdir)
            except OSError:
                print ' Cannot create file direcotry !! '

        self.outdir = outdir
        self.filename = []

        print ' Downloading:  '

        i=0
        for itemURL in self.itemURLs:

            itemfile = urllib2.urlopen(itemURL)
            filename = itemURL.split('/')[-1]
            self.filename += [filename]

            print self.itemSizes[i] + '\t' + filename
            i += 1
             
            filepath = os.path.join(outdir,filename)
            with open(filepath,"wb") as output:
                while True:
                    data = itemfile.read(32768)
                    if data:
                        output.write(data)
                    else:
                        break

    def print_items(self):
        for item in self.IprItems:
            print (u'{}'.format(item))

    def _unzip_file(self, item):
        filename = os.path.join(self.outdir, item)
        with zipfile.ZipFile(filename, "r") as z:
            itemDir = os.path.splitext(filename)[0]
            z.extractall(itemDir)
            
        return itemDir

    def _import_gdal(self, dsn_input, dsn_output, overwrite, crs, format_output):
        def import_layer(layer, odsn, overwrite, crs):
            options = ['PRECISION=NO','GEOMETRY_NAME=geom']
            if hasattr(self, 'dbschema'):
                options.append('SCHEMA={}'.format(self.dbschema if self.dbschema else 'public'))
            if overwrite:
                options.append('OVERWRITE=YES')


#       Rewrite existing prj file with correct EPGS
            DIR = dsn_input.split('/')[-1]
            prjFile = DIR.rsplit('_',1)[0] +".prj"

            os.remove(os.path.join(dsn_input,prjFile))
            prj = open(os.path.join(dsn_input,prjFile), "w")

            spatialRef = osr.SpatialReference()

            if crs == 'S-JTSK':
                spatialRef.ImportFromEPSG(5514)
            else:
                spatialRef.ImportFromEPSG(4326)

#            spatialRef.MorphToESRI()

            prj.write(spatialRef.ExportToWkt())
            prj.close()

            # copy input layer to output data source
            olayer = odsn.CopyLayer(layer, layer.GetName() , options)

            if olayer is None:
                raise IprError("Unable to copy layer {}".format(layer.GetName()))
            
        # open input data source (directory with shapefile/gml/... files)
        idsn = ogr.Open(dsn_input, False) # read
        if not idsn:
            raise IprError("Unable to open {}".format(dsn_input))

        # open output data source (PostGIS/SpatiaLite)
        odsn = ogr.Open(dsn_output, True) # write
        if not odsn:
            raise IprError("Unable to open {}".format(dsn_output))

        for idx in range(idsn.GetLayerCount()):
            # process shp/gml file
            import_layer(idsn.GetLayer(idx), odsn, overwrite, crs)
