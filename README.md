# pyScreenArranger

Tool which helps screen arranging by coordinating window.

Currently, support _linux_ only. We will __not__ support _MS Windows_, maybe.
If you are using Windows, consider using _WinSplitRevolution_ which gave
inspiration to this project or using _linux_.

# Usage
```
Usage: ./wcoordinate.py [--menu-height<=height>] [--system-menu-height<=height>]
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
```

## Examples
```
$ ./wcoordinate.py r_0 a_0 a_0 a_50 a_50
```
Place currently focused window to left top position of current monitor.
```
$ ./wcoordinate.py r_1 r_0 r_0 r_0 r_0
```
Move currently focused window to second monitor.
```
$ ./wcoordinate.py r_0 r_10 r_0 r_0 r_0
```
Shrink left side of currently focused window about 10% of width of current
monitor.

## Keyboard shortcuts mapping
Mapping commands with keyboard shortcuts can help you have much better
experience than only CLI.
Personally, I use some shortcut below:

```
# move window to prev screen
Shift+Super+H   wcoordinate.py r_-1 r_0 r_0 r_0 r_0
# move window to next screen
Shift+Super+L   wcoordinate.py r_1 r_0 r_0 r_0 r_0
# move window to left half
Shift+Ctrl+H    wcoordinate.py r_0 a_0 a_0 a_50 a_100
# move window to bottom half
Shift+Ctrl+J    wcoordinate.py r_0 a_0 a_50 a_100 a_100
# move window to top half
Shift+Ctrl+K    wcoordinate.py r_0 a_0 a_0 a_100 a_50
# move window to right half
Shift+Ctrl+L    wcoordinate.py r_0 a_50 a_0 a_100 a_100
```

# License
GPL v3.
Anyone can use source code everywhere. But, should follow limitation of GPL
v3.(http://www.gnu.org/licenses/gpl-3.0.html)

# Author
SeongJae Park (sj38.park@gmail.com)
