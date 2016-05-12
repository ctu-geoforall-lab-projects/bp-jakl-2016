/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% RECYCLING Centre 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

CREATE TABLE export_recycling_centre (
    geom geometry,
	amenity varchar DEFAULT 'recycling',
	recycling_type text DEFAULT 'centre',
	opening_hours text,
	fee text,
	operator text,
	source text,
	"source:loc" text DEFAULT 'IPR',   
	"recycling:wood" text  DEFAULT 'no'  ,
	"recycling:green_waste" text   DEFAULT 'no'   ,
	"recycling:metal" text  DEFAULT 'no'   ,
	"recycling:paper" text  DEFAULT 'no'   ,
	"recycling:glass" text  DEFAULT 'no'   ,
	"recycling:plastic" text  DEFAULT 'no'   , 
	"recycling:scrap_metal" text DEFAULT 'no'   ,
	"recycling:rubble" text DEFAULT 'no'  ,	
	"recycling:hazardous_waste" text  DEFAULT 'no'   ,
	"recycling:tyres" text  DEFAULT 'no'  
	)

/*===================================================================*/

INSERT INTO export_recycling_centre(
"geom",
"opening_hours","fee","operator","source","source:loc",
"recycling:wood",
"recycling:green_waste",
"recycling:metal",
"recycling:paper",
"recycling:glass",
"recycling:plastic", 
"recycling:scrap_metal",
"recycling:rubble",	
"recycling:hazardous_waste",
"recycling:tyres" 
)
SELECT geom, 
(	
REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
REPLACE(operatingh,
    'SincMondays','Mo'), /* <-- maji tam chybu*/
	'Mondays' , 'Mo'), 
    'Tuesdays','Tu'),
	'Wednesdays','We'),
	'Thursdays','Th'),		
	'Fridays' , 'Fr'),
	'Saturdays','Sa'),
	'Sundays','Su'),
	'to' , '-'),
	'from' , ''), 
	'through' , '-'),
	'0e','0'),
	'Since January 2016: ',''
)
						
	) AS "opening_hours",

	CASE WHEN (paymentwas LIKE '%Prague%') THEN 'free of charge for the Prague citizens' END  AS "fee" , 
	operator AS "operator",
	poskyt AS "source",
	poskyt AS "source:loc",
	
 	CASE WHEN wasteaccep LIKE '%wood%'				    THEN 'yes' 	ELSE 'no'  END  AS "recycling:wood"  ,
	CASE WHEN wasteaccep LIKE '%waste from greenery%'	THEN 'yes' 	ELSE 'no'  END  AS "recycling:green_waste",
	CASE WHEN wasteaccep LIKE '%scrap metal%' 			THEN 'yes' 	ELSE 'no'  END  AS "recycling:metal" ,
	CASE WHEN wasteaccep LIKE '%paper%' 				THEN 'yes' 	ELSE 'no'  END  AS "recycling:paper" ,
	CASE WHEN wasteaccep LIKE '%glass%' 				THEN 'yes' 	ELSE 'no'  END  AS "recycling:glass" ,
	CASE WHEN wasteaccep LIKE '%plastic%' 				THEN 'yes' 	ELSE 'no'  END  AS "recycling:plastic" , 
 	CASE WHEN wasteaccep LIKE '%scrap metal%' 			THEN 'yes' 	ELSE 'no'  END  AS "recycling:scrap_metal" ,
	CASE WHEN wasteaccep LIKE '%rubble%'				THEN 'yes' 	ELSE 'no'  END  AS "recycling:rubble" ,	
	CASE WHEN wasteaccep LIKE '%hazardous%' 			THEN 'yes' 	ELSE 'no'  END  AS "recycling:hazardous_waste" ,
	CASE WHEN wasteaccep LIKE '%tyres%' 				THEN 'yes' 	ELSE 'no'  END  AS "recycling:tyres" 
	
 from ipr.zpk_o_sberodpadu_b
