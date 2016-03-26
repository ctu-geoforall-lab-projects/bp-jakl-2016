import sys
import urllib2
import xmltodict
import zipfile
import os
from IPRbase import IprDownloader
from osgeo import ogr

class IprDownloaderPg(IprDownloader):
    def __init__(self):
        pass


    def Import2Pg(self):

        for item in self.filename:
#            if item.split('.')[-1] == 'zip':

            with zipfile.ZipFile(self.outdir+item, "r") as z:
                itemDir = self.outdir +item.split('.')[-2]
                z.extractall(itemDir +'/')
                
            format = itemDir.split('_')[-1]
#            print format

#            out_driver = ogr.GetDriverByName( 'ESRI Shapefile' )
#            out_ds = out_driver.CreateDataSource()
#            out_srs = None
#            out_layer = out_ds.CreateLayer("point", out_srs, ogr.wkbPoint)
#            fd = ogr.FieldDefn('name',ogr.OFTString)
#            out_layer.CreateField(fd)
