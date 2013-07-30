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
Usage: %s [--menu-height<=height>] [--system-menu-height<=height>]
    [--system-menu-screen=<screen>] <screen> <left> <top> <right> <bottom>

    --menu-height: height of menu bar of window in pixel.
    --system-menu-height: height of system menu bar in pixel.
    --system-menu-screen: number of screen which system menu bar located.

    screen: number of screen which should window locate.
        start from 0, ordered by xrandr says.
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
    left: X coordinate of left side of the window in percentage
        relative to the screen.
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
    top: Y coordinate of the top of the window in percentage
        relative to the screen.
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
    right: X coordinate of right side of the window in
        percentage relative to the screen.
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
    bottom: Y coordinate of bottom of the window in percenatge
        relative to the screen.
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
""" % sys.argv[0]

# bound for menu line
MENU_HEIGHT = 29
SYSTEM_MENU_HEIGHT = 10
SYSTEM_MENU_SCREEN = 1

def get_screen_config():
    """Return screen configuration include start coordinate, width, height"""
    raw_resolutions = os.popen("xrandr | grep '*'").readlines()
    resolutions = []
    screen_left = 0
    for raw_resolution in raw_resolutions:
        resolution = raw_resolution.split()[0].split('x')
        resolutions.append([screen_left, int(resolution[0]),
            int(resolution[1])])
        screen_left = screen_left + resolutions[-1][1]
    resolutions[SYSTEM_MENU_SCREEN][2] = (resolutions[SYSTEM_MENU_SCREEN][2] -
            SYSTEM_MENU_HEIGHT)
    return resolutions

def get_active_window_info(resolutions):
    """Return active window's coordinate in percent relative to current screen
    """
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
            t = t - MENU_HEIGHT
        elif info.find("Width: ") != -1:
            r = l + int(info.split()[-1])
        elif info.find("Height: ") != -1:
            b = t + int(info.split()[-1])

    screen_no = -1
    for resolution in resolutions:
        if resolution[0] <= l:
            screen_no = screen_no + 1
        else:
            break

    resolution = resolutions[screen_no]
    return (screen_no,
            round((l - resolution[0]) / float(resolution[1]) * 100, -1),
            round(t / float(resolution[2]) * 100, -1),
            round((r - resolution[0]) / float(resolution[1]) * 100, -1),
            round(b / float(resolution[2]) * 100, -1))

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print USAGE
        exit(1)

    for arg in sys.argv[:-5]:
        if arg.startswith("--menu-height"):
            MENU_HEIGHT = int(arg.split("=")[1])
        elif arg.startswith("--system-menu_height"):
            SYSTEM_MENU_HEIGHT = int(arg.split("=")[1])
        elif arg.startswith("--system-menu-screen"):
            SYSTEM_MENU_SCREEN = int(arg.split("=")[1])

    screen_no = sys.argv[-5].split("_")
    screen_no[1] = int(screen_no[1])

    left_percent = sys.argv[-4].split("_")
    left_percent[1] = float(left_percent[1])

    top_percent = sys.argv[-3].split("_")
    top_percent[1] = float(top_percent[1])

    right_percent = sys.argv[-2].split("_")
    right_percent[1] = float(right_percent[1])

    bottom_percent = sys.argv[-1].split("_")
    bottom_percent[1] = float(bottom_percent[1])

    resolutions = get_screen_config()
    active_window_info = get_active_window_info(resolutions)

    # Tranlate relative percent values to absolute percent values
    if screen_no[0] == "r":
        screen_no[0] = "a"
        screen_no[1] = ((active_window_info[0] + screen_no[1]) %
                len(resolutions))

    if left_percent[0] == "r":
        left_percent[0] = "a"
        left_percent[1] = active_window_info[1] + left_percent[1]

    if top_percent[0] == "r":
        top_percent[0] = "a"
        top_percent[1] = active_window_info[2] + top_percent[1]

    if right_percent[0] == "r":
        right_percent[0] = "a"
        right_percent[1] = active_window_info[3] + right_percent[1]

    if bottom_percent[0] == "r":
        bottom_percent[0] = "a"
        bottom_percent[1] = active_window_info[4] + bottom_percent[1]


    # Translate absolute percent value to absolute pixel coordinate
    resolution = resolutions[screen_no[1]]
    left_pix = int(resolution[0] + resolution[1] * left_percent[1] / 100)
    top_pix = int(resolution[2] * top_percent[1] / 100)
    right_pix = int(resolution[0] + resolution[1] * right_percent[1] / 100)
    bottom_pix = int(resolution[2] * bottom_percent[1] / 100)

    if screen_no[1] == SYSTEM_MENU_SCREEN:
        top_pix = top_pix + SYSTEM_MENU_HEIGHT


    width_pix = right_pix - left_pix
    height_pix = bottom_pix - top_pix - MENU_HEIGHT

    cmd = "wmctrl -r :ACTIVE: -e 0,%d,%d,%d,%d" % (left_pix, top_pix,
            width_pix, height_pix)
    print cmd
    os.system(cmd)
