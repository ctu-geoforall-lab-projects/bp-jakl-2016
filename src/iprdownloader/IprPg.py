import sys
import zipfile
import os
from IPRbase import IprDownloader
from osgeo import ogr

class IprDownloaderPg(IprDownloader):
    def __init__(self):
        pass


    def Import2Pg(self):

        for item in self.filename:
            if item.split('.')[-1] == 'zip':

                with zipfile.ZipFile(self.outdir+item, "r") as z:
                    itemDir = item.split('.')[-2]  +'/'
                    z.extractall(self.outdir +itemDir)
                
                format = itemDir.split('_')[-1]
                format = format.split('/')[-2]

                inFile = itemDir.split('_'+format)[-2] +'.'+format
                PgFile = itemDir.split('_'+format)[-2] +'.db'
                inFilePath = self.outdir +itemDir +inFile

                command = 'ogr2ogr -f PostgreSQL -nlt PROMOTE_TO_MULTI "PG:'

                dbname  = 'pgis_osm_bp'
                host    = 'geo102.fsv.cvut.cz'
                user    = ''#modify
                password= ''#modify

                command += 'dbname=' +dbname +' host=' +host +' user=' +user +' password=' +password
                command += '" ' +inFilePath +' -overwrite'

                os.system(command)
