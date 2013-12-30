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
    [--system-menu-screen=<screen>] [--verbose]
    <screen> <left> <top> <right> <bottom>

    --menu-height: height of menu bar of window in pixel.
    --system-menu-height: height of system menu bar in pixel.
    --system-menu-screen: number of screen which system menu bar located.
    --verbose: show message about what's going on inside.

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
MENU_HEIGHT = 15
SYSTEM_MENU_HEIGHT = 10
SYSTEM_MENU_SCREEN = 1

VERBOSE = False

def get_screen_config():
    """Return screen configuration include start coordinate, width, height"""
    raw_displays = os.popen('xrandr | grep " connected"').readlines()
    displays = []
    for raw_display in raw_displays:
        display = raw_display.split()[2].split('+')
        displays.append(display)
    displays = sorted(displays, key=lambda display: display[1])
    resolutions = []
    screen_left = 0
    for display in displays:
        resolution = display[0].split('x')
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

def parse_arguments(args):
    """Parse arguments and set global values, return destination position"""
    global MENU_HEIGHT, SYSTEM_MENU_HEIGHT, SYSTEM_MENU_SCREEN, VERBOSE
    for arg in args[:-5]:
        if arg.startswith("--menu-height"):
            MENU_HEIGHT = int(arg.split("=")[1])
        elif arg.startswith("--system-menu-height"):
            SYSTEM_MENU_HEIGHT = int(arg.split("=")[1])
        elif arg.startswith("--system-menu-screen"):
            SYSTEM_MENU_SCREEN = int(arg.split("=")[1])
        elif arg == "--verbose":
            VERBOSE = True

    screen_no = args[-5].split("_")
    screen_no[1] = int(screen_no[1])

    left_percent = args[-4].split("_")
    left_percent[1] = float(left_percent[1])

    top_percent = args[-3].split("_")
    top_percent[1] = float(top_percent[1])

    right_percent = args[-2].split("_")
    right_percent[1] = float(right_percent[1])

    bottom_percent = args[-1].split("_")
    bottom_percent[1] = float(bottom_percent[1])

    return (screen_no,
            left_percent, top_percent, right_percent, bottom_percent)

def relative_to_absolute(destination, resolutions, active_window_info):
    """Tranlate relative values to absolute values in percentage.

    param destination:
        Tuple of destination position informations. It contains target screen
        number, target left, top, right, bottom coordinate. coordinates are
        list with mode('r' for relative mode, 'a' for absolute mode) in
        percentage relative to target screen. elements are ordered in mentioned
        order."""
    if destination[0][0] == "r":
        destination[0][0] = "a"
        destination[0][1] = ((active_window_info[0] + destination[0][1]) %
                len(resolutions))

    if destination[1][0] == "r":
        destination[1][0] = "a"
        destination[1][1] = active_window_info[1] + destination[1][1]

    if destination[2][0] == "r":
        destination[2][0] = "a"
        destination[2][1] = active_window_info[2] + destination[2][1]

    if destination[3][0] == "r":
        destination[3][0] = "a"
        destination[3][1] = active_window_info[3] + destination[3][1]

    if destination[4][0] == "r":
        destination[4][0] = "a"
        destination[4][1] = active_window_info[4] + destination[4][1]

    # If left is right side of right or top is lower side of bottom,
    # do nothing.
    if (destination[1][1] >= destination[3][1] or
            destination[2][1] >= destination[4][1]):
        for i in range(1, 5):
            destination[i][1] = active_window_info[i]

def percent_to_pixel(destination, resolutions):
    """Translate absolute percent value to absolute pixel coordinate.

    param destination:
        Tuple of destination position informations. It contains target screen
        number, target left, top, right, bottom coordinate. coordinates are
        list with mode('r' for relative mode, 'a' for absolute mode) in
        percentage relative to target screen. elements are ordered in mentioned
        order."""
    resolution = resolutions[destination[0][1]]
    destination[1][1] = int(resolution[0] + resolution[1] * destination[1][1] /
            100)
    destination[2][1] = int(resolution[2] * destination[2][1] / 100)
    destination[3][1] = int(resolution[0] + resolution[1] * destination[3][1] /
            100)
    destination[4][1] = int(resolution[2] * destination[4][1] / 100)

    if destination[0][1] == SYSTEM_MENU_SCREEN:
        destination[2][1] = destination[2][1] + SYSTEM_MENU_HEIGHT

def locate_window(destination):
    resolutions = get_screen_config()
    active_window_info = get_active_window_info(resolutions)
    if VERBOSE:
        print "active window: ", active_window_info
        print "user want: ", destination

    #Tranlate relative percent values to absolute percent values
    relative_to_absolute(destination, resolutions, active_window_info)
    if VERBOSE:
        print "absolute dest: ", destination

    # Translate absolute percent value to absolute pixel coordinate
    percent_to_pixel(destination, resolutions)
    if VERBOSE:
        print "absolute pixel: ", destination

    left = destination[1][1]
    top = destination[2][1]
    right = destination[3][1]
    bottom = destination[4][1]

    width = right - left
    height = bottom - top - MENU_HEIGHT

    cmd = "wmctrl -r :ACTIVE: -e 0,%d,%d,%d,%d" % (left, top, width, height)
    if VERBOSE:
        print cmd
    os.system(cmd)

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print USAGE
        exit(1)

    destination_position = parse_arguments(sys.argv)

    locate_window(destination_position)
