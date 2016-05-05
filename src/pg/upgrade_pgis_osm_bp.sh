#!/bin/sh
set -e

SCRIPT=`realpath $0` # realpath is a separate package and doesn't need
                     # to be installed
if [ -z $SCRIPT ] ; then
    SCRIPTPATH='.'
else
    SCRIPTPATH=`dirname $SCRIPT`
fi

DB=pgis_osm_bp
FILE=czech-republic-latest.osm.bz2

# download
wget http://download.geofabrik.de/openstreetmap/europe/$FILE

# clean-up DB 
psql $DB -c "DROP SCHEMA IF EXISTS osm CASCADE"
psql $DB -c "CREATE SCHEMA osm"
psql $DB -c "GRANT USAGE ON SCHEMA osm TO public"
 
# import
osm2pgsql -d $DB -E 3857 -p czech -S $SCRIPTPATH/pgis_osm_bp.style -s $FILE

# czech_polygon: polygon -> multipolygon
echo "ALTER TABLE czech_polygon ADD COLUMN way1 geometry(MultiPolygon,3857);
UPDATE czech_polygon SET way1 = ST_Multi(way);
ALTER TABLE czech_polygon DROP COLUMN way;
ALTER TABLE czech_polygon RENAME COLUMN way1 TO way" | psql $DB

# add primary key 'gid'
# move tables to 'osm' schema
# rename column way -> geom
tables=`psql $DB -t -c "SELECT f_table_name FROM geometry_columns WHERE f_table_name LIKE 'czech%' and f_geometry_column = 'way'"`
for table in $tables; do
    echo "ALTER TABLE $table RENAME COLUMN way to geom;
ALTER TABLE $table ADD COLUMN gid serial;
ALTER TABLE $table ADD primary key (gid);
ALTER TABLE $table SET SCHEMA osm;
GRANT SELECT ON osm.$table TO public" | psql $DB
done

rm -rf $FILE

exit 0
