##encoding=utf-8

"""
Import Command
--------------
    from archives.metadata import lastname_dict
"""

from archives.lastname_list import lastname_list
from archives.statename_list import statename_list
from collections import OrderedDict

lastname_dict = OrderedDict()
for name_id, name in enumerate(lastname_list):
    lastname_dict[name_id] = name