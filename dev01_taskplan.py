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
from archives.fingerprint import fingerprint
import math
import sys

def taskplan(record_type, year):
    """For 18800+ lastnames, get results number for each query of:
        {record_type: #record_type, year: #year, lastname: #lastname}
        
    For example:
        if there are 25000 records for: record_type = death, year = 2000, lastname = smith, since
        the webpage display 1000 records per page, so we create pagenumber from 1 to 25 for this
        query. and save it in mongodb database (db = archives, collection = task) like this:
            {_id: md5 string, type: 2, lastname_id: 0, year: 2000, nth: 1, flag: false}
            ... nth + 1

    Afterwards, the crawler gonna go through all these pages, once it's done with one page, then
    it gonna change the flag to true, so the crawler are never gonna crawl that again.
    
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
    for lastname_id, lastname in lastname_dict.items():
        # check if we did this record_type, lastname_id, year combination before
        _id = fingerprint.of_text("%s_%s_%s_%s" % (record_type, lastname_id, year, 1) )
        if task.find({"_id": _id}).count() == 0: # only do it when we never do it
            print("processing type=%s, lastname=%s in %s ..." % (record_type, lastname, year))
            if record_type == 1:
                url = urlencoder.url_birth_record(lastname, year, 10, 1)
            elif record_type == 2:
                url = urlencoder.url_death_record(lastname, year, 10, 1)
            elif record_type == 3:
                url = urlencoder.url_marriage_record(lastname, year, 10, 1)
            elif record_type == 4:
                url = urlencoder.url_divorce_record(lastname, year, 10, 1)
            
            html = spider.html(url)
            if html:
                try:
                    num_of_records = htmlparser.get_total_number_of_records(html)
                    max_pagenum = int(math.ceil(float(num_of_records)/1000)) # calculate how many page we should crawl
                    print("\tWe got %s pages to crawl" % max_pagenum)
                    for pagenum in range(1, max_pagenum+1):
                        doc = {"_id": fingerprint.of_text("%s_%s_%s_%s" % (record_type, lastname_id, year, pagenum) ),
                               "type": record_type,
                               "lastname_id": lastname_id,
                               "year": year,
                               "nth": pagenum,
                               "flag": False}
                        try:
                            task.insert(doc)
                        except:
                            pass
                except:
                    pass
            else:
                print("\tFailed to get html")
                
if __name__ == "__main__":
#     record_type, year = int(sys.argv[1]), int(sys.argv[2])
#     record_type, year = 2, 2007
    for record_type in [1,2,3,4]:
        taskplan(record_type, 2014)
#     client.close()
