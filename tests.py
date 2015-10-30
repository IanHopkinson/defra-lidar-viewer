#!/usr/bin/env python
# encoding: utf-8

from nose.tools import assert_equal

from process import tile_origin, calculate_offsets

DATA_DICT = {
            "NY22": {"name":"Keswick", "xorg":320000, "yorg":520000},
            "NZ26": {"name":"Newscastle", "xorg":420000, "yorg":560000},
            "SJ36": {"name":"Deeside", "xorg":330000, "yorg":360000},
            "SJ46": {"name":"Chester", "xorg":340000, "yorg":360000},
            "SJ89": {"name":"Manchester", "xorg":380000, "yorg":390000},
            "SO74": {"name":"Malvern", "xorg":370000, "yorg":240000},
            "ST76": {"name":"Bath", "xorg":370000, "yorg":160000},
            "SY98": {"name":"Corfe Castle", "xorg":390000, "yorg":80000},
            "SY68": {"name":"Maiden Castle", "xorg":360000, "yorg":80000},
            "TQ38": {"name":"London", "xorg":530000, "yorg":180000},
            }

OFFSET_TEST_SET = [
    {"xoffset_exp": 4500.0, "yoffset_exp": 500.0, "output_data_size":5000.0, "cellsize": 2.0, 
     "xorg": 340000.0, "yorg": 360000.0, "xllcorner": 349000.0, "yllcorner": 369000.0},
     {"xoffset_exp": 0.0, "yoffset_exp": 5000.0, "output_data_size":5000.0, "cellsize": 2.0, 
     "xorg": 340000.0, "yorg": 360000.0, "xllcorner": 340000.0, "yllcorner": 360000.0},
     {"xoffset_exp": 3500.0, "yoffset_exp": 2500.0, "output_data_size":5000.0, "cellsize": 2.0, 
     "xorg": 340000.0, "yorg": 360000.0, "xllcorner": 347000.0, "yllcorner": 365000.0},
    ]

def test_tile_org():
    for tile_code in DATA_DICT.keys():
        yield tile_origin_calc, tile_code

def test_calculate_offset():
    for params in OFFSET_TEST_SET:
        yield calc_offset, params

def calc_offset(params):
    metadata = {"cellsize": params["cellsize"], "xllcorner": params["xllcorner"], "yllcorner": params["yllcorner"]  }
    output_data_size = params["output_data_size"]
    xorg = params["xorg"]
    yorg = params["yorg"]
    xoffset_exp = params["xoffset_exp"]
    yoffset_exp = params["yoffset_exp"]
    calc_xoffset, calc_yoffset = calculate_offsets(metadata, output_data_size, xorg, yorg)
    assert_equal(calc_xoffset, xoffset_exp)
    assert_equal(calc_yoffset, yoffset_exp)

def tile_origin_calc(tile_code):
        expected_xorg = DATA_DICT[tile_code]["xorg"]
        expected_yorg = DATA_DICT[tile_code]["yorg"]
        print("{}: expected xorg: {}, expected_yorg {}".format(tile_code, expected_xorg, expected_yorg))
        calc_xorg, calc_yorg = tile_origin(tile_code)
        assert_equal(calc_xorg, expected_xorg)
        assert_equal(calc_yorg, expected_yorg)
