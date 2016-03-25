import sys
import urllib2
import xmltodict
import zipfile
from IPRbase import IprDownloader

class IprDownloaderPg(IprDownloader):
    def __init__(self,):
        pass


    def Ipr2Pg(self):

        for item in self.filename:
#            print self.outdir + item

            if item.split('.')[-1] == 'zip':#    asi zbytecne
                with zipfile.ZipFile(self.outdir+item, "r") as z:
                    item.split('.')[-2]
                    z.extractall(self.outdir +'/' +item.split('.')[-2])

