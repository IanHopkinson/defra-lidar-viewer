#!/usr/bin/env python
# encoding: utf-8

from nose.tools import assert_equal

from process import tile_origin

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

def test_tile_org():
    for tile_code in DATA_DICT.keys():
        expected_xorg = DATA_DICT[tile_code]["xorg"]
        expected_yorg = DATA_DICT[tile_code]["yorg"]
        print("{}: expected xorg: {}, expected_yorg {}".format(tile_code, expected_xorg, expected_yorg))
        calc_xorg, calc_yorg = tile_origin(tile_code)
        assert_equal(calc_xorg, expected_xorg)
        assert_equal(calc_yorg, expected_yorg)
