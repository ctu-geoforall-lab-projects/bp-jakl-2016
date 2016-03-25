import sys
import urllib2
import xmltodict
import zipfile
from IPRbase import IprDownloader
from osgeo import ogr

class IprDownloaderPg(IprDownloader):
    def __init__(self,):
        pass


    def Import2Pg(self):

        for item in self.filename:

#            if item.split('.')[-1] == 'zip':
            with zipfile.ZipFile(self.outdir+item, "r") as z:
                itemDir = self.outdir +item.split('.')[-2] +'/'
                z.extractall(itemDir)
