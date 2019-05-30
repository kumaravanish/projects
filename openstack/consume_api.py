import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from requests.exceptions import HTTPError
from os_api import OSCommon
from os_api import OSNovaApi

flavor_list = OSNovaApi().get_flavor_name_list()
for flavor in flavor_list:
    print flavor

