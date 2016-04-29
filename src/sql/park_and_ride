/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% PARK + RIDE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

CREATE TABLE export_park_ride (
    geom geometry,
	amenity text DEFAULT 'parking',
	park_ride text DEFAULT 'yes',
	source text DEFAULT 'IPR',
	"source:loc" text DEFAULT 'IPR'
	)

/*==================================================*/

INSERT INTO export_park_ride(geom)
SELECT geom 
FROM ipr.dop_zachparkoviste_b

