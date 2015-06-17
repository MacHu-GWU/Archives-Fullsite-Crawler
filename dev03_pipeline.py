##encoding=utf-8

"""
This module is to delivery json data to database
"""

from archives.js import load_js
from archives.windowsexplorer import (WinFile, WinDir, 
    FileCollections, WinExplorer, string_SizeInBytes)
from archives.database import client, birth, death, marriage, divorce
import time

WinFile.set_initialize_mode(fastmode=True)

def json_filter(winfile):
    if winfile.basename.endswith(".json"):
        return True
    else:
        return False

def push2db():
    for record_type, collection in zip(range(1, 4+1),
                                       [birth, death, marriage, divorce]):
        for winfile in FileCollections.from_path_by_criterion(
                        r"pipeline_%s" % record_type, json_filter).iterfiles():
            data = load_js(winfile.abspath, enable_verbose=False)
            for doc in data:
                try: # code block to save data in database
                    print(doc)
#                     collection.insert(doc)
                except:
                    pass
#             try:
#                 os.remove(winfile.abspath)
#             except:
#                 pass
            
if __name__ == "__main__":
    while 1:
        push2db()
        time.sleep(1 * 60)
        
    client.close()