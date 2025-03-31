#
# Title: test_great_circle.py
# Description:
# Development Environment: OS X 12.6.9/Python 3.11.5
# Author: G.S. Cole (guycole at gmail dot com)
#
from unittest import TestCase

from great_circle import range_and_bearing


class TestGreatCircle(TestCase):
    def test_range_and_bearing(self):
        result = range_and_bearing(0.0, 0.0, 0.0, 0.0)
        assert result == (0.0, 0.0)

        # north
        result = range_and_bearing(0.0, 0.0, 1.0, 0.0)
        assert result == (60.04046073261274, 0.0)

        # north east
        result = range_and_bearing(0.0, 0.0, 1.0, 1.0)
        assert result == (84.90787832133203, 44.99563645534485)

        # east
        result = range_and_bearing(0.0, 0.0, 0.0, 1.0)
        assert result == (60.04046073261274, 90.0)

        # south east
        result = range_and_bearing(0.0, 0.0, -1.0, 1.0)
        assert result == (84.90787832133203, 135.00436354465515)

        # south
        result = range_and_bearing(0.0, 0.0, -1.0, 0.0)
        assert result == (60.04046073261274, 180.0)

        # south west
        result = range_and_bearing(0.0, 0.0, -1.0, -1.0)
        assert result == (84.90787832133203, 224.99563645534485)

        # west
        result = range_and_bearing(0.0, 0.0, 0.0, -1.0)
        assert result == (60.04046073261274, 270.0)

        # north west
        result = range_and_bearing(0.0, 0.0, 1.0, -1.0)
        assert result == (84.90787832133203, 315.0043635446552)


# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
