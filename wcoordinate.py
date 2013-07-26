#!/usr/bin/env python

"""Coordinate window's location and size."""

__author__ = "SeongJae Park"
__email__ = "sj38.park@gmail.com"
__copyright__ = "Copyright (c) 2013, SeongJae Park"
__license__ = "GPLv3"

import os
import sys

raw_resolutions = os.popen("xrandr | grep '*'").readlines()
resolutions = []
for raw_resolution in raw_resolutions:
    resolution = raw_resolution.split()[0].split('x')
    resolutions.append([int(resolution[0]), int(resolution[1])])

def get_active_window_info():
    x = 0
    y = 0
    w = 0
    h = 0

    active_window_info = os.popen("xwininfo -id $(xdotool getactivewindow)"
                                 ).readlines()
    for info in active_window_info:
        if info.find("Absolute upper-left X: ") != -1:
            x = int(info.split()[-1])
        elif info.find("Absolute upper-left Y: ") != -1:
            y = int(info.split()[-1])
        elif info.find("Width: ") != -1:
            w = int(info.split()[-1])
        elif info.find("Height: ") != -1:
            h = int(info.split()[-1])
    return (x, y, w, h)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: %s <x> <y> <width> <height>"
        print ("     x: x axis of window's left top point in percentage" +
                " relative to current monitor")
        print ("     y: y axis of widnow's left top point in percentage" +
                " relative to current monitor")
        print ("     width: width of window in percentage relative to" +
                " current monitor")
        print ("     height: height of window in percentage relative to" +
                " current monitor")
    x_percent = float(sys.argv[1])
    y_percent = float(sys.argv[2])
    width_percent = float(sys.argv[3])
    height_percent = float(sys.argv[4])

    # TODO: May relative mode can be more helpful
    active_window_info = get_active_window_info()

    current_screen = 0
    x_limit = 0
    for resolution in resolutions:
        x_limit = x_limit + resolution[0]
        if x_limit < active_window_info[0]:
            current_screen = current_screen + 1
        else:
            x_limit = x_limit - resolution[0]

    x_abs = int(x_limit + resolutions[current_screen][0] * x_percent / 100)
    y_abs = int(resolutions[current_screen][1] * y_percent / 100)
    w_abs = int(resolutions[current_screen][0] * width_percent / 100)
    h_abs = int(resolutions[current_screen][1] * height_percent / 100)

    cmd = "wmctrl -r :ACTIVE: -e 0,%d,%d,%d,%d" % (x_abs, y_abs, w_abs, h_abs)
    print cmd
    os.system(cmd)
