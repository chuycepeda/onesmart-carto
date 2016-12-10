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

<em>For the ease of understanding I use the word <strong>"drawing"</strong> to refer the equivalent to POSTGIS <a href="www.postgis.org/docs/ST_AsText.html" target="_blank">ST_AsText()</a> also known as the Well-Known Text (WKT) for geometries and geographies.</em>
