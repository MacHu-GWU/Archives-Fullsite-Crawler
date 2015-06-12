##encoding=utf-8

"""
collection schema:

task = {
    _id: md5( (type, name, year, nth) ),
    type: 1. birthrecord, 2. deathrecord, 3. marriage 4. divorce
    name_id: lastname_id
    year: 1900 - 2015
    nth: pagenumber, 1000 records per page
    flag: true - has been crawled, false - has not been crawled
    }

Import Command
--------------
    from archives.database import client, task, backup
"""

from pymongo import MongoClient

client = MongoClient()
db = client.archives
task = db.task

if __name__ == "__main__":
    pass