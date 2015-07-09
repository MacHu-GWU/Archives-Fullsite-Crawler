##encoding=utf-8

"""
Import Command
--------------
    from archives.metadata import lastname_dict, lastname_reverse_dict
"""

from archives.lastname_list import lastname_list
from archives.statename_list import statename_list
from collections import OrderedDict

lastname_dict = OrderedDict()
for lastname_id, lastname in enumerate(lastname_list):
    lastname_dict[lastname_id] = lastname
    
lastname_reverse_dict = OrderedDict()
for lastname_id, lastname in enumerate(lastname_list):
    lastname_dict[lastname] = lastname_id