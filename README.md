# pyScreenArranger

Tool which helps screen arranging by coordinating window.

Currently, support _linux_ only. We will __not__ support _MS Windows_, maybe.
If you are using Windows, consider using _WinSplitRevolution_ which gave
inspiration to this project or using _linux_.

# Usage
```
Usage: ./wcoordinate.py <screen> <left> <top> <right> <bottom>
    screen: number of screen which should window locate.
        start from 0, ordered by xrandr says.
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
    left: X coordinate of left side of the window in percentage
        relative to the screen
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
    top: Y coordinate of the top of the window in percentage
        relative to the screen
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
    right: X coordinate of right side of the window in
        percentage relative to the screen
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
    bottom: Y coordinate of bottom of the window in percenatge
        relative to the screen
        prefix 'a_' for absolute value,
        prefix 'r_' for value relative to current value.
```

# License
GPL v3.
Anyone can use source code everywhere. But, should follow limitation of GPL
v3.(http://www.gnu.org/licenses/gpl-3.0.html)

# Author
SeongJae Park (sj38.park@gmail.com)
