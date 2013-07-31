#!/usr/bin/env python

import unittest

import wcoordinate

class TestWcoordinate(unittest.TestCase):
    def setUp(self):
        print "test wcoordinate start..."

    def tearDown(self):
        print "tear down..."

    def test_parse_arguments(self):
        args = ["a_0", "a_10", "r_10", "a_-10", "r_-10"]
        parsed = wcoordinate.parse_arguments(args)
        self.assertEqual(parsed, (["a", 0], ["a", 10.0], ["r", 10.0],
                ["a", -10.0], ["r", -10.0]))

        args = ["--menu-height=15", "--system-menu-height=16",
                "--system-menu-screen=7", "--verbose",
                "a_0", "a_10", "r_10", "a_-10", "r_-10"]
        parsed = wcoordinate.parse_arguments(args)
        self.assertEqual(wcoordinate.MENU_HEIGHT, 15)
        self.assertEqual(wcoordinate.SYSTEM_MENU_HEIGHT, 16)
        self.assertEqual(wcoordinate.SYSTEM_MENU_SCREEN, 7)
        self.assertEqual(wcoordinate.VERBOSE, True)

    def test_relative_to_absolute(self):
        resolutions = [[0,100,100], [100,200,200]]
        active_window_info = [0, 10, 10, 20, 20]
        destination = [
                ["r", 0],
                ["a", 10.0],
                ["r", 10.0],
                ["r", 10.0],
                ["r", 10.0]]
        wcoordinate.relative_to_absolute(destination, resolutions,
                active_window_info)
        self.assertEqual(destination,
                [["a", 0], ["a", 10.0], ["a", 20.0], ["a", 30.0], ["a", 30.0]])

        # test bound value
        resolutions = [[0,100,100], [100,200,200]]
        active_window_info = [0, 10, 10, 20, 20]
        destination = [
                ["r", 0],
                ["r", 0.0],
                ["r", 0.0],
                ["r", -10.0],
                ["r", 0.0]]
        wcoordinate.relative_to_absolute(destination, resolutions,
                active_window_info)
        self.assertEqual(destination,
                [["a",0], ["a", 10.0], ["a", 10.0], ["a", 20.0], ["a", 20.0]])

    def test_percent_to_pixel(self):
        resolutions = [[0,100,100], [100,200,200]]
        wcoordinate.SYSTEM_MENU_SCREEN = 1
        destination = [
                ["a", wcoordinate.SYSTEM_MENU_SCREEN],
                ["a", 15.0],
                ["a", 15.0],
                ["a", 30.0],
                ["a", 35.0]]
        wcoordinate.percent_to_pixel(destination, resolutions)
        self.assertEqual(destination, 
                [["a", 1], ["a", resolutions[1][0] + 2 * 15],
                    ["a", 2 * 15 + wcoordinate.SYSTEM_MENU_HEIGHT],
                    ["a", resolutions[1][0] + 2 * 30],
                    ["a", 2 * 35]])
