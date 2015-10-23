#!/usr/bin/env python
# encoding: utf-8

DATA_DIR ="C:\\BigData\\defra-lidar\\LIDAR-DSM-2M-SJ46"
    
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


def main():
    datafiles = listdir(DATA_DIR)
    print("Found {} datafiles".format(len(datafiles)))

#    for item in datafiles:
        # Open file
        

            #print(log_line)

    # Select a file and then load it into an array
    currentfile = datafiles[0]

    metadata = get_header_info(currentfile)
    print(metadata)

    data = np.zeros((500,500), dtype=np.float)
    with open(os.path.join(DATA_DIR, currentfile)) as f:
        content = f.readlines()
        idx = 0
        for line in content:
            parts = line.split()
            if len(parts) == 500:
                data[idx,] = [float(x) for x in parts]
                idx = idx + 1 
    print(data)

    print("Number of NODATA_values: {}".format(np.sum(data == -9999)))
    data[data == -9999] = np.nan
    print("Minimum value found: {}".format(np.nanmin(data)))
    print("Maximum value found: {}".format(np.nanmax(data)))
    # Show the data
    
    plt.imshow(data, interpolation='nearest', cmap=plt.gray())
    plt.show()

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