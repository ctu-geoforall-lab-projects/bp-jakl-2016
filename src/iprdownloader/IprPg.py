from IprBase import IprDownloader

class IprDownloaderPg(IprDownloader):
    def __init__(self):
        pass

    def import_data(self, crs, dbname, overwrite, dbhost=None, dbport=None, dbuser=None, dbpasswd=None):
        def conn_string(dbname, dbhost=None, dbport=None, dbuser=None, dbpasswd=None):
            dbconn = 'PG:dbname={0}'.format(dbname)
            if dbhost:
                dbconn += ' host={0}'.format(dbhost)
            if dbport:
                dbconn += ' port={0}'.format(dbport)
            if dbuser:
                dbconn += ' user={0}'.format(dbuser)
            if dbpasswd:
                dbconn += ' password={0}'.format(dbpasswd)

            return dbconn

        dsn_output = conn_string(dbname, dbhost, dbport, dbuser, dbpasswd)
        for item in self.filename:
            if item.split('.')[-1] != 'zip':
                continue
            dsn_input = self._unzip_file(item)
            self._import_gdal(dsn_input, dsn_output, overwrite, crs, format_output='PostgreSQL')
