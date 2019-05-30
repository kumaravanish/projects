#!/usr/bin/python
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from os_api import OSCommon
from os_api import OSNovaApi

flavor_list = OSNovaApi().get_flavor_name_list()
for flavor in flavor_list:
    print flavor

