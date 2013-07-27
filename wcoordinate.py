#!/usr/bin/env python

"""Coordinate window's location and size."""

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013, SeongJae Park"
__license__ = "GPLv3"

import os
import platform
import sys

if platform.system() != "Linux":
    print "Sorry, we Support only linux(yet)."
    exit(1)

USAGE = """
Usage: %s <screen> <left> <top> <right> <bottom>
    screen: number of screen which should window locate.
        start from 0, ordered by xrandr says.
        -1 for current screen.
    left: X coordinate of left side of the window in percentage
        relative to the screen
        -1 for current value.
    top: Y coordinate of the top of the window in percentage
        relative to the screen
        -1 for current value.
    right: X coordinate of right side of the window in
        percentage relative to the screen
        -1 for current value.
    bottom: Y coordinate of bottom of the window in percenatge
        relative to the screen
        -1 for current value.
""" % sys.argv[0]

raw_resolutions = os.popen("xrandr | grep '*'").readlines()
resolutions = []
for raw_resolution in raw_resolutions:
    resolution = raw_resolution.split()[0].split('x')
    resolutions.append([int(resolution[0]), int(resolution[1])])

def get_active_window_info():
    l = 0
    r = 0
    t = 0
    b = 0

    active_window_info = os.popen("xwininfo -id $(xdotool getactivewindow)"
                                 ).readlines()
    for info in active_window_info:
        if info.find("Absolute upper-left X: ") != -1:
            l = int(info.split()[-1])
        elif info.find("Absolute upper-left Y: ") != -1:
            t = int(info.split()[-1])
        elif info.find("Width: ") != -1:
            r = l + int(info.split()[-1])
        elif info.find("Height: ") != -1:
            b = t + int(info.split()[-1])
    return (l, t, r, b)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print USAGE
        exit(1)
    screen_no = int(sys.argv[1])
    left_percent = float(sys.argv[2])
    top_percent = float(sys.argv[3])
    right_percent = float(sys.argv[4])
    bottom_percent = float(sys.argv[5])

    active_window_info = get_active_window_info()

    screen_left = 0
    if screen_no == -1:
        for resolution in resolutions:
            if screen_left + resolution[0] < active_window_info[0]:
                screen_no = screen_no + 1
                screen_left = screen_left + resolution[0]
            else:
                break
    else:
        for i, resolution in enumerate(resolutions):
            if i < screen_no:
                screen_left += resolution[0]

    if left_percent == -1:
        left_abs = active_window_info[0]
    else:
        left_abs = int(screen_left + resolutions[screen_no][0] * left_percent /
                100)
    if top_percent == -1:
        top_abs = active_window_info[1]
    else:
        top_abs = int(resolutions[screen_no][1] * top_percent / 100)
    if right_percent == -1:
        width_abs = active_window_info[2] - left_abs
    else:
        width_abs = screen_left + int(resolutions[screen_no][0] *
                right_percent / 100) - left_abs
    if bottom_percent == -1:
        height_abs = active_window_info[3] - top_abs
    else:
        height_abs = int(resolutions[screen_no][1] * bottom_percent /
                100) - top_abs

    cmd = "wmctrl -r :ACTIVE: -e 0,%d,%d,%d,%d" % (left_abs, top_abs,
            width_abs, height_abs)
    print cmd
    os.system(cmd)
