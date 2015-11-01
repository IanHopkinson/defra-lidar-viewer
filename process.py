#!/usr/bin/env python
# encoding: utf-8

# Subdirectory
# LIDAR-DTM-2M-SJ46
# Filenames like: 
# sj4060_DTM_2m.asc, 
# sj4{0-9}{60-69}_DTM_2m.asc
#ncols        500
#nrows        500
#xllcorner    340000
#yllcorner    360000
#cellsize     2
#NODATA_value  -9999

from collections import OrderedDict
import json
import sys
import zipfile
import os

import numpy as np

from matplotlib import pyplot as plt

from coordinate_converter import OSGB36toWGS84
import matplotlib


LOGLINE_TEMPLATE = OrderedDict([
    ('name', None),
    ('nrows', None),
    ('ncols', None),
    ('xllcorner', None),
    ('yllcorner', None),
    ('cellsize', None),
    ('NODATA_value', None),
])

# Primary grid: (S, T), (N, O), H going North 500km x 500km
# Secondary grid: A-Z (omitting I, 5x5) 100km x 100km
PRIMARY = {
        "H": {"xorg": 0, "yorg":1400000},
        "N": {"xorg": 0, "yorg":900000},
        "O": {"xorg": 500000, "yorg":900000},
        "S": {"xorg": 0, "yorg": 400000},
        "T": {"xorg": 500000, "yorg": 400000},
}

SECONDARY = {
        "A": {"xorg": 0, "yorg": 0},
        "B": {"xorg": 100000, "yorg": 0},
        "C": {"xorg": 200000, "yorg": 0},
        "D": {"xorg": 300000, "yorg": 0},
        "E": {"xorg": 400000, "yorg": 0},

        "F": {"xorg": 0, "yorg": 100000},
        "G": {"xorg": 100000, "yorg": 100000},
        "H": {"xorg": 200000, "yorg": 100000},
        "J": {"xorg": 300000, "yorg": 100000},
        "K": {"xorg": 400000, "yorg": 100000},

        "L": {"xorg": 0, "yorg": 200000},
        "M": {"xorg": 100000, "yorg": 200000},
        "N": {"xorg": 200000, "yorg": 200000},
        "O": {"xorg": 300000, "yorg": 200000},
        "P": {"xorg": 400000, "yorg": 200000},

        "Q": {"xorg": 0, "yorg": 300000},
        "R": {"xorg": 100000, "yorg":300000},
        "S": {"xorg": 200000, "yorg":300000},
        "T": {"xorg": 300000, "yorg":300000},
        "U": {"xorg": 400000, "yorg":300000},

        "V": {"xorg": 0, "yorg": 400000},
        "W": {"xorg": 100000, "yorg": 400000},
        "X": {"xorg": 200000, "yorg": 400000},
        "Y": {"xorg": 300000, "yorg": 400000},
        "Z": {"xorg": 400000, "yorg": 400000},        
}

DATA_ROOT_DIR = "C:\\BigData\\defra-lidar\\"
if not os.path.exists(DATA_ROOT_DIR):
    DATA_ROOT_DIR = os.getcwd()
DATA_DIR_TEMPLATE = os.path.join(DATA_ROOT_DIR, "LIDAR-DSM-2M-{OS_grid_cell}.zip")
DATA_FILE = ""

OS_GRID_SIZE = 10000.0

def main(argv=None):
    global DATA_FILE
    # Process commandline arguments
    # If we were just going to process one tile then here would be the place to start
    # Return a file list from process_arguments, adjust OS_GRID_SIZE, return os_grid_cell
    DATA_FILE, os_grid_cell, name = process_arguments(argv)

    # Report on datafiles
    zf = zipfile.ZipFile(DATA_FILE, 'r')
    datafiles = zf.namelist()
    print("Data zip file: {}".format(DATA_FILE))
    print("Found {} datafiles".format(len(datafiles)))
    xorg, yorg = tile_origin(os_grid_cell)

    # Calculate bounding box
    lat_ll, lng_ll = OSGB36toWGS84(xorg, yorg) # lower left
    lat_ur, lng_ur = OSGB36toWGS84(xorg + OS_GRID_SIZE, yorg + OS_GRID_SIZE) 
    bb = "[{}, {}], [{}, {}]".format(lat_ll, lng_ll, lat_ur, lng_ur)
    print("Bounding box: {}".format(bb))

    # Write bounding box to data_dict
    write_to_data_dict(os_grid_cell, bb, name)

    # Iterate over datafiles
    filelist = [x for x in range(len(datafiles))]

    # Assume all tiles in a dataset have the same ncols, nrows, cellsize and NODATA_value
    metadata = get_header_info(datafiles[0])
    # Output_data_size is OS_GRID_SIZE/cellsize
    output_data_size = OS_GRID_SIZE / metadata["cellsize"]

    bigdata = np.zeros((output_data_size, output_data_size), dtype=np.float)
    for idx in filelist:
        # Get data
        metadata = get_header_info(datafiles[idx])
        data = get_image(datafiles[idx], metadata["ncols"], metadata["nrows"])        
        data[data == -9999] = 0.0
        # Calculate x,y offset
        xoffset, yoffset = calculate_offsets(metadata, output_data_size, xorg, yorg)
        width = metadata["ncols"]
        height = metadata["nrows"]
        # Write into array
        bigdata[yoffset - height:yoffset, xoffset:xoffset + width] = data 
    # Show the data
    plot_image(bigdata)

    # Export the data to an image
    filename = "images/" + os_grid_cell
    matplotlib.image.imsave(filename, bigdata, cmap=plt.gray())

def write_to_data_dict(os_grid_cell, bb, name):
    try:
        with open('data_dict.json') as data_file:    
            data_dict = json.load(data_file)
    except:
        data_dict = {}

    if os_grid_cell in data_dict.keys(): 
        data_dict[os_grid_cell]["bb"] = bb
        data_dict[os_grid_cell]["name"] = name
    else:
        data_dict[os_grid_cell] = {"bb": bb, "name": name}

    with open('data_dict.json', 'w') as outfile:
        json.dump(data_dict, outfile, sort_keys=True, indent=4)

def process_arguments(argv):
    if argv is None:
        argv = sys.argv
    arg = argv[1:]

    DATA_FILE = ""
    os_grid_cell = ''
    name = "None"

    os_grid_cell = arg[0]

    # If the first argument is short it's assumed to be of the form SJ46
    # And that we are asking for a directory like LIDAR-DSM-2M-{OS_grid_cell}
    # Otherwise we assume we are being given the full directory name
    if len(arg[0]) == 4:
        DATA_FILE = DATA_DIR_TEMPLATE.format(OS_grid_cell=os_grid_cell)
    else:
        DATA_FILE = DATA_ROOT_DIR + arg[0]
        os_grid_cell = arg[0][-4:]

    # If there is a second argument then it is a friendly name
    if len(arg) == 2:
        name = arg[1]
    
    return DATA_FILE, os_grid_cell, name

def list_available_data():
    print("Lookin' for data!")

def tile_origin(tile_code):
    xorg = PRIMARY[tile_code[0]]["xorg"] + SECONDARY[tile_code[1]]["xorg"] + float(tile_code[2]) * OS_GRID_SIZE
    yorg = PRIMARY[tile_code[0]]["yorg"] - SECONDARY[tile_code[1]]["yorg"] + float(tile_code[3]) * OS_GRID_SIZE
    return xorg, yorg

def calculate_offsets(metadata, output_data_size, xorg, yorg):
    xoffset = (metadata["xllcorner"] - xorg) / float(metadata["cellsize"])
    yoffset = output_data_size - (metadata["yllcorner"] - yorg) / float(metadata["cellsize"])
    return xoffset, yoffset

def plot_image(data):
    plt.imshow(data, interpolation='nearest', cmap=plt.gray())
    plt.axis('off')
    plt.margins(0, 0, tight=True)
    plt.show()

def get_image(filename, ncols, nrows):
    data = np.zeros((ncols, nrows), dtype=np.float)
    zf = zipfile.ZipFile(DATA_FILE)
    with zf.open(filename) as f:
        content = f.readlines()
        idx = 0
        for line in content:
            line = line.decode("utf-8")
            parts = line.split()
            if len(parts) == ncols:
                data[idx,] = [float(x) for x in parts]
                idx = idx + 1
    return data

def get_header_info(filename):
    log_line = LOGLINE_TEMPLATE.copy()
    zf = zipfile.ZipFile(DATA_FILE)
    with zf.open(filename) as f:
        content = [next(f) for x in range(7)]
        log_line["name"] = filename
        for line in content:
            line = line.decode("utf-8") 
            parts = line.split()
            #assert len(parts) in [1,2]
            if len(parts) != 2:
                break
            elif len(parts) == 2:
                if parts[0] == "nrows":
                    log_line["nrows"] = int(parts[1])
                elif parts[0] == "ncols":
                    log_line["ncols"] = int(parts[1])
                elif parts[0] == "xllcorner":
                    log_line["xllcorner"] = float(parts[1])
                elif parts[0] == "yllcorner":
                    log_line["yllcorner"] = float(parts[1])
                elif parts[0] == "cellsize":
                    log_line["cellsize"] = float(parts[1])
                elif parts[0] == "NODATA_value":
                    log_line["NODATA_value"] = int(parts[1])
                else:
                    print("Keyword not recognised: {}".format(parts[0]))
            else: 
                print("Unexpected line length (not 2 or 500): {}".format(len(parts)))
    return log_line


if __name__ == "__main__":
    main()
