##encoding=utf-8

from archives.database import client, task, birth, death, marriage, divorce
from archives.metadata import lastname_dict
from archives.urlencoder import urlencoder
from archives.htmlparser import htmlparser
from archives.spider import spider
from archives.js import safe_dump_js
from archives.fingerprint import fingerprint
from multiprocessing.dummy import Pool
import sys
import os

def select_todo_url(record_type, year):
    """
    Return a argument list for multithread crawler.
    arugments is a tuple of:
        (record_type, lastname_id, lastname, year, pagenum, left_counter)
        
    [args]
    ------
        record_type:
            1. birth record
            2. death record
            3. marriage record
            4. divorce record
        year: 4 digits year
    """
    todo = list()
    for doc in task.find({"type": record_type, "year": year, "flag": False}).limit(20000):
        todo.append([
            doc["type"],
            doc["lastname_id"],
            lastname_dict[doc["lastname_id"]],
            doc["year"],
            doc["nth"],
            ])
    counter = len(todo)
    for l in todo:
        counter -= 1
        l.append(counter)
    return todo

def process_one(argument):
    """unit processor function for multithread crawler
    argument = (record_type, lastname_id, lastname, year, pagenumber, leftcounter)
    """
    record_type, lastname_id, lastname, year, pagenum, left_counter = argument
    if record_type == 1:
        url = urlencoder.url_birth_record(lastname, year, 1000, pagenum)
        date_key = "Birth Date:"
    elif record_type == 2:
        url = urlencoder.url_death_record(lastname, year, 1000, pagenum)
        date_key = "Death Date:"
    elif record_type == 3:
        url = urlencoder.url_marriage_record(lastname, year, 1000, pagenum)
        date_key = "Marriage Date:"
    elif record_type == 4:
        url = urlencoder.url_divorce_record(lastname, year, 1000, pagenum)
        date_key = "Divorce Date:"

    html = spider.html(url)
    
    if html:
        try:
            data = list()
            for record in htmlparser.extract_records(html):
                record.setdefault("Lastname:", lastname) # <== create new field "Lastname:"
                record.setdefault("Year:", year) # <== create new field "Year:"
    
                record["_id"] = fingerprint.of_text("%s_%s_%s" % (
                                    record.get("Name:", None),
                                    record.get(date_key, None),
                                    record.get("Location:", None),
                                    ))
                
                data.append(record)

            if len(data) > 0:
                _id = fingerprint.of_text("%s_%s_%s_%s" % (record_type, lastname_id, year, pagenum) )
                safe_dump_js(data, r"pipeline_%s\%s.json" % (record_type, _id), enable_verbose=False)
                task.update({"_id": _id}, {"$set": {"flag": True}}) # edit document in task
                print("successfully crawled type=%s, year=%s, lastname='%s', pagenum=%s; %s url left" % (
                            record_type, year, lastname, pagenum, left_counter))
        except Exception as e:
            print(e)

def singlethread_process(record_type, year):
    todo = select_todo_url(record_type, year)
    for argument in todo:
        process_one(argument)
        
def mutithread_process(record_type, year):
    todo = select_todo_url(record_type, year)
    print("we got %s url to crawl" % len(todo))
    pool = Pool(4)
    pool.map(process_one, todo)

if __name__ == "__main__":
    for i in range(1, 4+1):
        try:
            os.mkdir("pipeline_%s" % i)
        except:
            pass
#     record_type, year = int(sys.argv[1]), int(sys.argv[2])
#     record_type, year = 1, 2000
    record_type = 4
    for year in range(2000, 2014+1):
        mutithread_process(record_type, year)