## Quick-reference repo for POSTGIS + Carto

Download and play with index.html in browser's console.

You'll find it useful to jump start your implementations.

<em>Some of the things you'll find</em>

<strong>Google Maps</strong>
<ul>
	<li> <strong>init.</strong> A method to add Google Maps in your html.</li>
	<li> <strong>geocodeAddress.</strong> Geocoder for quick map centering</li>
	<li> <strong>addDrawingManager.</strong> Drawing manager for fast geospatial content</li>
	<li> <strong>drawingToWKT.</strong> A method to get from Google Drawings to POSTGIS ST_AsText()</li>
	<li> <strong>dropMarker.</strong> A method to drop markers on the Google Map</li>
</ul>

<strong>POSTGIS + Carto</strong>
<ul>
	<li> <strong>createLayers.</strong> A method to easily detect how to create map layers.</li>
	<li> <strong>setQ.</strong> A method for the ease of setting up your queries.</li>
	<li> <strong>setStyle.</strong> A method for the easr of changing layer styles.</li>
	<li> <strong>getFullQuery.</strong> A method for quick querying your carto tables.</li>
	<li> <strong>getLatLng.</strong> A method to get coordinates from your queries.</li>
	<li> <strong>triggerInfowindow.</strong> A method to programatically launch an infowindow.</li>
	<li> <strong>getIntersectFromDrawing.</strong> A method to query for intersecting elements in your data with a drawing.</li>
	<li> <strong>getIntersectFromBufferedDrawing.</strong> A method to query for intersecting elements in your data an expanded (buffered) drawing.</li>
	<li> <strong>getArea.</strong> A method to calculate area from your queried data.</li>
	<li> <strong>getAreaFromDrawing.</strong> A method to calculate area from a drawing.</li>
	<li> <strong>getDistanceFromDrawing.</strong> A method to calculate distance from your data to a drawing.</li>
	<li> <strong>getDistanceBetweenDrawings.</strong> A method to calculate distance between drawings.</li>
	<li> <strong>getDrawingFromGeom.</strong> A method to take a coded GEOM to readable Text</li>
	<li> <strong>ajax<em>*</em>.</strong> A series of snippets to override carto when cache is messing up your stuff.</li>
</ul>

<em>For the ease of understanding I use the word <strong>"Drawing"</strong> to refer the equivalent of POSTGIS <a href="www.postgis.org/docs/ST_AsText.html" target="_blank">ST_AsText()</a> also known as the Well-Known Text (WKT) for geometries and geographies.</em>

<hr>

## Notes


	USEFUL SQL STATEMENTS

	(1) GET SCHEMA (needs to be in carto console)
		
		SELECT column_name FROM information_schema.columns WHERE table_name = 'YOUR_TABLE'

	(2) INSERT AN ELEMENT (need api_key parameter)

		INSERT INTO table (col1,col2,col3) VALUES ('a',2,'c')

	(3) UPDATE AN ELEMENT (need api_key parameter)

		UPDATE SET (col1,col2,col3) = ('A',100,'C') FROM table WHERE cartodb_id = 1

	(4) DELETE AN ELEMENT (need api_key parameter)

		DELETE FROM table WHERE cartodb_id = 1


	(5) INTERSECTION

		from tables: 	

			SELECT table_1.* FROM table_1, table_2 WHERE ST_Intersects(table_1.the_geom, table_2.the_geom)

		from a GEOM TEXT:

			SELECT * FROM table WHERE ST_Intersects(the_geom, ST_GeomFromText('POLYGON((-100.3047801554203 25.709135581044972,-100.30812755227089 25.70364473148278,-100.30134692788124 25.70364473148278,-100.3047801554203 25.709135581044972))',4326))

		from a GEOM (useful for querying intersections among different carto accounts):

			query for the_geom in one carto user, then query second user as:

			SELECT * FROM table WHERE ST_Intersects(the_geom, ST_GeomFromText(ST_AsText('"+previous.the_geom+"'),4326))



	(6) INTERSECTIONS 

		WITHIN 
		
			use a distance in meters (e.g. 25):

				SELECT table_1.* FROM table_1, table_2 WHERE ST_DWithin(ST_Transform(table_1.the_geom, 2163), ST_Transform(table_2.the_geom, 2163), 25)

			using meters (e.g. 25) from GEOM TEXT element:

				SELECT * FROM table WHERE ST_DWithin(ST_Transform(ST_GeomFromText('POINT(-100.31464064550778 25.720455131035184)', 4326), 2163), ST_Transform(table.the_geom, 2163), 25)

	
		BUFFER

			use an earth radius calculated as:

				// dist is the distance in meters
				function updateEarthRadius(lat, lng, dist) {
				    var deg = 180,
				        brng = deg * Math.PI / 180,
				        dist = dist / 6371000,
				        lat1 = lat * Math.PI / 180,
				        lon1 = lng * Math.PI / 180, radius;

				    var lat2 = Math.asin(Math.sin(lat1) * Math.cos(dist) + Math.cos(lat1) * Math.sin(dist) * Math.cos(brng));

				    var lon2 = lon1 + Math.atan2(Math.sin(brng) * Math.sin(dist) * Math.cos(lat1), Math.cos(dist) - Math.sin(lat1) * Math.sin(lat2));

				    if (isNaN(lat2) || isNaN(lon2)) radius = null;

				    else radius = lat - (lat2 * 180 / Math.PI);

				    return radius
				}

				SELECT * FROM table WHERE ( ST_Intersects(table.the_geom,ST_Buffer( ST_SetSRID('POINT(-100.31464064550778 25.720455131035184)'::geometry , 4326),0.04496608029593929)))

			using meters (e.g. 25):

				SELECT * FROM table WHERE ST_Intersects(ST_Buffer(ST_Transform(ST_GeomFromText('POINT(-100.31464064550778 25.720455131035184)', 4326), 2163), 25), ST_Transform(table.the_geom, 2163))


	(8) DATES

		intervals: 		

			SELECT * FROM table WHERE (((now()) - table.date_field) < INTERVAL '7 day')

			SELECT * FROM table WHERE (((now()) - table.date_field) < INTERVAL '7 hour')
		
		betweens: 	

			SELECT * FROM table WHERE ((table.date_field BETWEEN ('2016-12-09') AND (DATE '2016-12-09' + 1)))

			SELECT * FROM table WHERE ((date_part('hour', table.date_field) BETWEEN 8 AND 15))

		days of week: 	

			SELECT * FROM table WHERE EXTRACT(dow FROM table.date_field) IN (1 , 3 , 5)


	(9) DISTANCE

		from a GEOM TEXT in a given range (e.g. 25 meters):

			SELECT * FROM table where ST_Distance(ST_Transform(table.the_geom, 2163), ST_Transform(ST_GeomFromText('POINT(-100.31464064550778 25.720455131035184)', 4326), 2163)) < 25

			how about using ST_DWithin ?

			SELECT * FROM table where ST_DWithin(ST_Transform(table.the_geom, 2163), ST_Transform(ST_GeomFromText('POINT(-100.31464064550778 25.720455131035184)', 4326), 2163), 25)

		get distance only

			SELECT ST_Distance(ST_GeomFromText('"+geom_text_1+"', 4326), ST_GeomFromText('"+geom_text_2+"', 4326)) as degrees, ST_Distance(ST_Transform(ST_GeomFromText('"+geom_text_1+"', 4326), 2163), ST_Transform(ST_GeomFromText('"+geom_text_2+"', 4326), 2163)) as m, ST_Distance(ST_Transform(ST_GeomFromText('"+geom_text_1+"', 4326), 2163), ST_Transform(ST_GeomFromText('"+geom_text_2+"', 4326), 2163))/1000 as km

	(10) AREA

		SELECT ST_Area(the_geom::geography) as sqm, ST_Area(the_geom::geography)/1000000 as sqkm, ST_Area(the_geom::geography)*10.7639 as sqft FROM table
	
	= = = 

	NOTES

		POSTGIS PROJECTIONS ARE BASED ON SRIDs SUCH AS:
			4326, WGS 84, UNITS IN PLANAR DEGREES [GEOMetry] (CARTO DEFAULT)
			2163, US NATIONAL ATLAS, UNITS IN METERS [GEOGraphy] (easiest appreciation as it is in meters)


