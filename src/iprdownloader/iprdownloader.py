#!/usr/bin/env python
#########################################################################
#
# Command-line tool for downloading IPR data
# http://www.iprpraha.cz/clanek/1313/otevrena-data-open-data (in Czech)
#
# 2016 (c) by Martin Jakl (OSGeoREL CTU in Prague)
#
# Licence: GNU GPL v2+
#
#########################################################################


import sys
import urllib2
import xmltodict
import argparse

from IPRbase import IprDownloader
from IprPg   import IprDownloaderPg


def main(alike=None, crs=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--alike", type=lambda s: unicode(s, 'utf8'), help = "search name title alike given string")
    parser.add_argument("--crs",   type=str,default = "S-JTSK",       help = "specify coordinate system (WGS-84 or S-JTSK > default: S-JTSK")
    parser.add_argument("--format",type=str,default = "shp",          help = "specify file format (default: shp) ..for rasters tiff,png..")
    parser.add_argument("--outdir",type=str,default = "data",         help = "define the folder to save (default: data)")
    parser.add_argument("--download", action='store_true', help = "download selected data")
    args = parser.parse_args()

    if args.crs == "5514":
        args.crs = "S-JTSK"
    elif args.crs == "4326":
        args.crs = "WGS 84"
    else:
        args.crs = args.crs.upper()
        if args.crs == 'WGS-84':
            args.crs = args.crs.replace('-', ' ')

    if args.crs not in ('S-JTSK', 'WGS 84'):
        sys.exit("Unsupported coordinate system: {0}. Valid options: S-JTSK, WGS-84".format(args.crs))

    ipr = IprDownloaderPg()
    ipr.filter(args.alike, args.crs, args.format)

    if args.download:
        ipr.download(args.outdir)
        ipr.Import2Pg()
    else:
        ipr.print_items()


    return 0

if __name__ == "__main__":
    sys.exit(main())

