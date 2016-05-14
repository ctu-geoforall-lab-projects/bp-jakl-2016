
/* %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

CREATE TABLE praha_building_osm(
        gid int primary key,
        geom geometry,
        building text,
        "building:height" text,
        "building:part" text) ;
		
		
INSERT INTO praha_building_osm

SELECT  B.gid, 
        B.geom,
        B.building, 
        B.height,
        B.part

FROM(   SELECT gid,geom,building, height 
        FROM osm.czech_polygon
        WHERE building IS NOT null
        ) AS B

JOIN(   SELECT gid,geom,name 
        FROM osm.czech_polygon 
        WHERE name LIKE 'Hlavní město Praha' ) AS P

ON ST_Within(B.geom, P.geom);

/* %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
/*         toto -- čislo se bude měnit podle čísla datasetu bd3_prah--  */
CREATE TABLE bud73_OSM( gid int primary key,
                        geom geometry,
                        building text	);

INSERT INTO bud73_OSM
SELECT  budovy.gid, 
        ST_Buffer(budovy.geom,3) as geom,
        budovy.building
FROM(   SELECT ST_MakeEnvelope( max(ST_XMax(geom))+100 ,    max(ST_YMax(geom))+100 ,
                                min(ST_XMin(geom))-100 ,    min(ST_YMin(geom))-100 ,
                                5514 ) AS geom 
        FROM ipr.bd3_prah73
    ) AS hranice

JOIN(   SELECT  gid, 
                ST_Transform(geom,5514) AS geom,
                building
        FROM jakl.praha_building_osm
        WHERE "building:part" IS null
          AND "building:height" IS null
    ) AS budovy
ON ST_Within(budovy.geom , hranice.geom);

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

CREATE TABLE bud73_IPR(
             id_bud int,
             geom geometry);

INSERT INTO bud73_IPR
SELECT  id_bud,
        ST_Union(
            ST_Buffer(
                ST_Force_2D(
                    ST_MakeValid(geom)),0.1)) AS geom
FROM   ipr.bd3_prah73
WHERE  typ LIKE '%stresni%'
GROUP BY id_bud;

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

CREATE TABLE gid_id( gid int,
                     id_bud int);

INSERT INTO gid_id
SELECT	AAA.gid,
        BBB.id_bud
FROM jakl.bud73_osm AS AAA
JOIN jakl.bud73_ipr AS BBB
ON ST_Within(BBB.geom , AAA.geom);

/* %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

CREATE TABLE osm_height( gid int primary key,
                         building_height real );

INSERT INTO osm_height
SELECT  budovy.gid,
        vysky.height
FROM(   SELECT *
        FROM  gid_id
        WHERE gid IN (  SELECT gid
                        FROM gid_id
                        GROUP BY gid
                        HAVING count(gid)=1	)
		) AS budovy
JOIN(   SELECT  id_bud,
                max(maxZ) - min(minZ) AS Height
        FROM(   SELECT  id_bud,
                        ST_ZMax(geom) AS maxZ,
                        ST_ZMin(geom) AS minZ
                FROM   ipr.bd3_prah73
            ) AS max_min
        GROUP BY id_bud
    ) AS vysky
ON budovy.id_bud = vysky.id_bud;

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

UPDATE praha_building_osm
SET "building:height" = building_height
FROM osm_height
WHERE osm_height.gid = praha_building_osm.gid;

/*=========================================================*/

DROP TABLE bud73_osm;
DROP TABLE bud73_ipr;
DROP TABLE gid_id;
DROP TABLE osm_height;
