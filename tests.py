#!/usr/bin/env python
# encoding: utf-8

from nose.tools import assert_equal

from process import DATA_DICT, tile_origin

def test_tile_org():
    for tile_code in DATA_DICT.keys():
        expected_xorg = DATA_DICT[tile_code]["xorg"]
        expected_yorg = DATA_DICT[tile_code]["yorg"]
        print("{}: expected xorg: {}, expected_yorg {}".format(tile_code, expected_xorg, expected_yorg))
        calc_xorg, calc_yorg = tile_origin(tile_code)
        assert_equal(calc_xorg, expected_xorg)
        assert_equal(calc_yorg, expected_yorg)
