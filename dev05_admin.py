from archives.database import client, task, birth, death, marriage, divorce
from archives.metadata import lastname_dict

"""
in birth we have 202936 data
in death we have 511535 data
in marriage we have 408358 data
in divorce we have 222500 data
"""
# for record_type in range(1, 4+1):
#     for year in range(2000, 2014):
#         print(record_type, year, task.find({"type": record_type,
#                                             "year": year}).count())

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
    for collection in [birth, death, marriage, divorce]:
        print("In %s we have %s records." % (
            collection.name, stringlize(collection.count())))

def crawler_status(year):
    for collection in [birth, death, marriage, divorce]:
        total = collection.find({"Year:": year}).count()
        print("In %s on year %s we have %s records." % (
                collection.name, year, stringlize(total)))
        
if __name__ == "__main__":
#     general_crawler_status()
    crawler_status(2001)