from archives.database import client, db, task, birth, death, marriage, divorce
from archives.metadata import lastname_dict
from archives.windowsexplorer import string_SizeInBytes
from pprint import pprint as ppt

"""
2015-07-09
In birth we have 745,847 records.
In death we have 2,302,602 records.
In marriage we have 2,044,892 records.
In divorce we have 628,018 records.
"""

def stringlize(number):
    res = list()
    while 1:
        number, m = divmod(number, 1000)
        res.append(str(m).zfill(3))
        if number < 1000:
            res.append(str(number))
            break
    return ",".join(res[::-1])

def general_crawler_status():
    dbstats = db.command("dbstats")
    print("storage size: %s" % string_SizeInBytes(dbstats["storageSize"]))
    for collection in [birth, death, marriage, divorce]:
        print("In %s we have %s records." % (
            collection.name, stringlize(collection.count())))

def crawler_status(year):
    for collection in [birth, death, marriage, divorce]:
        total = collection.find({"Year:": year}).count()
        print("In %s on year %s we have %s records." % (
                collection.name, year, stringlize(total)))
        
if __name__ == "__main__":
    general_crawler_status()
#     crawler_status(2001)