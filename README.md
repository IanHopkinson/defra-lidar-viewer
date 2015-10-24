# LIDAR data from DEFRA

## Usage

The `process.py` will display a window showing the data from a LIDAR map tile.

These data must be downloaded manually from:

http://environment.data.gov.uk/ds/survey#/download

And then unzipped to a directory. So far I've successfully used the 2m resolution
Terrain and Surface files.

Once downloaded and unzipped, change `DATA_DIR` to the appropriate location and
set `xorg` and `yorg` in the `main()` loop to the `xllcorner` and `yllcorner` values
of the lower left corner of the first file in your tile. (I'm looking to automating this)

Then just run `./process.py`, and after a shortish pause (<1 minute) you should see a greyscale
image of your map tile with height encoded as shade (black = lowest, white = highest).
 
This assumes you have `numpy` and `matplotlib` libraries installed.

## Data

Terrain data is an estimation of underlying terrain, surface data is the actual
measurement including buildings, vehicles and vegetation.

The data lives here: 

http://environment.data.gov.uk/ds/survey#/download

http://environment.data.gov.uk/ds/survey#/download?grid=SJ36

Handy collect of links

http://mapgubbins.tumblr.com/post/131424021480/open-data-release-of-aerial-lidar-data-for

This tool converts OS map reference x,y to lat, lng (and shows them on a map)

http://gridreferencefinder.com/

See here for converting OS x,y to lat,lng

https://bitbucket.org/ian_hopkinson/rail-statistics