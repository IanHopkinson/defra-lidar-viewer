#!/usr/bin/env python
# encoding: utf-8

DATA_DIR ="C:\\BigData\\defra-lidar\\LIDAR-DTM-2M-SJ46"
    
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

def main():
    datafiles = listdir(DATA_DIR)
    print("Found {} datafiles".format(len(datafiles)))

    for item in datafiles:
        # Open file
        with open(os.path.join(DATA_DIR, item)) as f:
            content = f.readlines()
            print("{} has {} lines".format(item, len(content)))
            log_line = LOGLINE_TEMPLATE.copy()
            log_line["name"] = item
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

            print(log_line)

if __name__ == "__main__":
    main()