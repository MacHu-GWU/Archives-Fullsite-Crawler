##encoding=utf-8

from archives.database import client, task, backup
from archives.metadata import lastname_dict
from archives.urlencoder import urlencoder
from archives.htmlparser import htmlparser
from archives.spider import spider
from angora.DATA import *
from multiprocessing.dummy import Pool
import sys
import os

def select_todo_url(record_type, year):
    """
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
    for doc in task.find({"type": record_type, "year": year, "flag": False}).limit(100*100):
        todo.append([
            doc["type"],
            doc["name_id"],
            lastname_dict[doc["name_id"]],
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
    """
    record_type, name_id, name, year, pagenum, left_counter = argument
    url = urlencoder.url_death_record(name, year, 1000, pagenum)
    html = spider.html(url)
    if html:
        try:
            data = list(htmlparser.extract_records(html))
            if len(data) > 0:
                _id = md5_obj( (record_type, name_id, year, pagenum) )
                safe_dump_js(data, r"pipeline_%s\%s.json" % (record_type, _id), enable_verbose=False)
                task.update({"_id": _id}, {"$set": {"flag": True}}) # edit document in task
                print("successfully crawled type=%s, year=%s, lastname='%s', pagenum=%s; %s url left" % (
                            record_type, year, name, pagenum, left_counter))
        except:
            pass

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
    record_type, year = int(sys.argv[1]), int(sys.argv[2])
    mutithread_process(record_type, year)