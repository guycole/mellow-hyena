#
# Title: driver.py
# Description:
# Development Environment: Ubuntu 22.04.5 LTS/python 3.10.12
# Author: G.S. Cole (guycole at gmail dot com)
#
import json
import os
import sys

print("start driver")

#
# argv[1] = configuration filename
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_name = sys.argv[1]
    else:
        config_name = "config.yaml"

pytprint("stop driver")

# ;;; Local Variables: ***
# ;;; mode:python ***
# ;;; End: ***
