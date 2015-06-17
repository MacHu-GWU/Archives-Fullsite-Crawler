##encoding=utf-8

"""
usage:
    cd to this directory, run cmd (crawl death record in year 2000):
        python dev01_taskplan.py 2 2000
"""

from archives.database import client, task
from archives.metadata import lastname_dict
from archives.urlencoder import urlencoder
from archives.htmlparser import htmlparser
from archives.spider import spider
from angora.DATA.hashutil import md5_obj
import math
import sys

def taskplan(record_type, year):
    """For 18800+ lastnames, get results number for each query of:
        {record_type: #record_type, year: #year, lastname: #lastname}
        
    For example:
        if there are 25000 records for: record_type = death, year = 2000, lastname = smith, since
        the webpage display 1000 records per page, so we create pagenumber from 1 to 25 for this
        query. and save it in mongodb database (db = archives, collection = task) like this:
            {_id: md5 string, type: 2, name_id: 0, year: 2000, nth: 1, flag: false}
            ... nth + 1
    
    For more information about task plan data model, see archives.database.py
    
    [args]
    ------
        record_type:
            1. birth record
            2. death record
            3. marriage record
            4. divorce record
        year: 4 digits year
    """
    for name_id, name in lastname_dict.items():
        # check if we did this record_type, name_id, year combination before
        _id = md5_obj( (record_type, name_id, year, 1) )
        if task.find({"_id": _id}).count() == 0: # only do it when we never do it
            print("processing lastname=%s in %s ..." % (name, year))
            url = urlencoder.url_death_record(name, year, 10, 1)
            html = spider.html(url)
            if html:
                try:
                    num_of_records = htmlparser.get_total_number_of_records(html)
                    max_pagenum = int(math.ceil(float(num_of_records)/1000))+1
                    print("\tWe got %s pages to crawl" % max_pagenum)
                    for pagenum in range(1, max_pagenum+1):
                        doc = {"_id": md5_obj( (record_type, name_id, year, pagenum) ),
                               "type": record_type,
                               "name_id": name_id,
                               "year": year,
                               "nth": pagenum,
                               "flag": False}
                    try:
                        task.insert(doc)
                    except:
                        pass
                except:
                    pass
#                 

if __name__ == "__main__":
    record_type, year = int(sys.argv[1]), int(sys.argv[2])
#     record_type, year = 2, 2007
    taskplan(record_type, year)
    client.close()