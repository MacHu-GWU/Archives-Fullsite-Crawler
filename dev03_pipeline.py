##encoding=utf-8

"""
This module is to delivery json data to database
"""

from archives.datamodel import datamodel
from angora.DATA import *
from angora.LIBRARIAN import *
import time

WinFile.set_initialize_mode(fastmode=True)

def json_filter(winfile):
    if winfile.basename.endswith(".json"):
        return True
    else:
        return False

def push2db():
    for record_type in range(1, 4+1):
        for winfile in FileCollections.from_path_by_criterion(
                        r"pipeline_%s" % record_type, json_filter).iterfiles():
            data = load_js(winfile.abspath, enable_verbose=False)
            for doc in data:
                try: # code block to save data in database
                    doc = datamodel.convert_document(doc)
                    print(doc)
                except:
                    pass
            try:
                os.remove(winfile.abspath)
            except:
                pass
            
if __name__ == "__main__":
    while 1:
        push2db()
        time.sleep(1 * 60)