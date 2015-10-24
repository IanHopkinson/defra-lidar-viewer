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

LOGLINE_TEMPLATE = OrderedDict([
    ('name', None),
    ('nrows', None),
    ('ncols', None),
    ('xllcorner', None),
    ('yllcorner', None),
    ('cellsize', None),
    ('NODATA_value', None),
])

from os import listdir
import os.path

import numpy as np

from matplotlib import pyplot as plt
import matplotlib

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter

DATA_DICT = {
            "NY22": {"name":"Keswick", "xorg":320000, "yorg":520000},
            "NZ26": {"name":"Newscastle", "xorg":420000, "yorg":560000},
            "SJ36": {"name":"Deeside", "xorg":330000, "yorg":360000},
            "SJ46": {"name":"Chester", "xorg":340000, "yorg":360000},
            "SJ89": {"name":"Manchester", "xorg":380000, "yorg":390000},
            "SO74": {"name":"Malvern", "xorg":370000, "yorg":240000},
            "ST76": {"name":"Bath", "xorg":370000, "yorg":160000},
            "TQ38": {"name":"London", "xorg":530000, "yorg":180000},
            }

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

DATA_DIR = "C:\\BigData\\defra-lidar\\LIDAR-DSM-2M-ST76"

def main():
    datafiles = listdir(DATA_DIR)
    print("Found {} datafiles".format(len(datafiles)))
    xorg, yorg = tile_origin(DATA_DIR.split("-")[-1])

    # Select a file and then load it into an array
    # 8 - includes home!
    #currentfile = datafiles[7]

    #metadata = get_header_info(currentfile)
    #print(metadata)

    #data = get_image(currentfile)

    #print("Number of NODATA_values: {}".format(np.sum(data == -9999)))
    #print("Minimum value found: {}".format(np.nanmin(data)))
    #print("Maximum value found: {}".format(np.nanmax(data)))

    # filelist = [7, 8, 17, 18]
    filelist = [x for x in range(len(datafiles))]

    bigdata = np.zeros((5000,5000), dtype=np.float)
    for idx in filelist:
        # Get data
        metadata = get_header_info(datafiles[idx])
        data = get_image(datafiles[idx])        
        data[data == -9999] = np.nan
        # Calculate x,y offset
        xoffset, yoffset = calculate_offsets(metadata, xorg, yorg)
        width = 500
        height = 500
        # Write into array
        bigdata[yoffset - height:yoffset, xoffset:xoffset + width] = data 
    # Show the data
    plot_image(bigdata)
    #plot_surface(data)

def tile_origin(tile_code):
    xorg = PRIMARY[tile_code[0]]["xorg"] + SECONDARY[tile_code[1]]["xorg"] + int(tile_code[2]) * 10000
    yorg = PRIMARY[tile_code[0]]["yorg"] - SECONDARY[tile_code[1]]["yorg"] + int(tile_code[3]) * 10000
    #if tile_code in DATA_DICT.keys():
    #    xorg = DATA_DICT[tile_code]["xorg"]
    #    yorg = DATA_DICT[tile_code]["yorg"]
    return xorg, yorg

def calculate_offsets(metadata, xorg=340000, yorg=360000):
    xoffset = (metadata["xllcorner"] - xorg) / 2
    yoffset = 5000 - (metadata["yllcorner"] - yorg) / 2
    return xoffset, yoffset

def plot_image(data):
    plt.imshow(data, interpolation='nearest', cmap=plt.gray())
    plt.show()

def plot_surface(data):
    # generate 3D sample data

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(0,500)
    Y = np.arange(0,500)
    X, Y = np.meshgrid(X, Y)
    surf = ax.plot_surface(X, Y, data, linewidth=0, antialiased=False)
    # ax.set_zlim(-1.01, 1.01)

    # ax.zaxis.set_major_locator(LinearLocator(10))
    # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()


def get_image(filename):
    data = np.zeros((500,500), dtype=np.float)
    with open(os.path.join(DATA_DIR, filename)) as f:
        content = f.readlines()
        idx = 0
        for line in content:
            parts = line.split()
            if len(parts) == 500:
                data[idx,] = [float(x) for x in parts]
                idx = idx + 1 
    return data

def get_header_info(filename):
    log_line = LOGLINE_TEMPLATE.copy()
    with open(os.path.join(DATA_DIR, filename)) as f:
        content = [next(f) for x in range(7)]
        log_line["name"] = filename
        for line in content:
            parts = line.split()
            #assert len(parts) in [1,2]
            if len(parts) == 500:
                break
            elif len(parts) == 2:
                if parts[0] == "nrows":
                    log_line["nrows"] = int(parts[1])
                elif parts[0] == "ncols":
                    log_line["ncols"] = int(parts[1])
                elif parts[0] == "xllcorner":
                    log_line["xllcorner"] = int(parts[1])
                elif parts[0] == "yllcorner":
                    log_line["yllcorner"] = int(parts[1])
                elif parts[0] == "cellsize":
                    log_line["cellsize"] = int(parts[1])
                elif parts[0] == "NODATA_value":
                    log_line["NODATA_value"] = int(parts[1])
                else:
                    print("Keyword not recognised: {}".format(parts[0]))
            else: 
                print("Unexpected line length (not 2 or 500): {}".format(len(parts)))
    return log_line


if __name__ == "__main__":
    main()