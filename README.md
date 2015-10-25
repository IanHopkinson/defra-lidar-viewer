# LIDAR data from DEFRA

## Usage

`process.py` will display a window showing the data from a LIDAR map tile.

These data must be downloaded manually from:

http://environment.data.gov.uk/ds/survey#/download

And then unzipped to a directory. So far I've successfully used the 2m resolution
Terrain and Surface files.

Once downloaded and unzipped, change `DATA_DIR` to the appropriate location.

Then just run `./process.py`, and after a shortish pause (<1 minute) you should see a greyscale
image of your map tile with height encoded as shade (black = lowest, white = highest).

Nominally there are 100 subtiles to a set but some are missing and appear as black squares,
some locations have NODATA, these appear white in the image.

This assumes you have `numpy` and `matplotlib` libraries installed.

There are minimal tests which can be run by doing `nosetests`, assuming you have `nosetests` installed

## TODO

We could make an image overlay using leafet.js:

http://leafletjs.com/reference.html#imageoverlay 

https://www.mapbox.com/mapbox.js/example/v1.0.0/imageoverlay-georeferenced/

Minimal webserver in Python 3 is:

`python -m http.server 8888 &`

## Data

Terrain data is an estimation of underlying terrain, surface data is the actual
measurement including buildings, vehicles and vegetation.

The data lives here: 

http://environment.data.gov.uk/ds/survey#/download

http://environment.data.gov.uk/ds/survey#/download?grid=SJ36

There's JSON metadata for each grid:

http://www.geostore.com/environment-agency/rest/product/OS_GB_10KM/SJ46

The `id` in the JSON tells you where you can download the zip file, e.g.:

http://www.geostore.com/environment-agency/rest/product/download/6129

## References

Handy collect of links

http://mapgubbins.tumblr.com/post/131424021480/open-data-release-of-aerial-lidar-data-for

This tool converts OS map reference x,y to lat, lng (and shows them on a map)

http://gridreferencefinder.com/

Code for converting OS x,y to lat,lng is by Hannah Fry, described here:

http://www.hannahfry.co.uk/blog/2012/02/01/converting-british-national-grid-to-latitude-and-longitude-ii

Get tile origin from OS National Grid reference:

http://digimap.edina.ac.uk/webhelp/os/gazetteer_plus/grid_ref_conversion.htm