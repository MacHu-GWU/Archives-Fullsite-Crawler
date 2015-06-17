##encoding=utf-8

"""
Imoprt Command
--------------
    from archives.spider import spider
"""

import requests

class ArchivesSpider():
    def __init__(self, timeout=30, sleeptime=0):
        self.session = requests.Session()
        self.default_timeout = timeout
        self.default_sleeptime = sleeptime
        self.default_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
            "Content-Type": "text/html; charset=UTF-8",
            "Connection": "close",
            "Referer": "http://www.archives.com/member/",
            }
        
        self.login()

    def set_timeout(self, timeout):
        """set default timeout limit in second
        """
        self.default_timeout = timeout
    
    def set_sleeptime(self, sleeptime):
        """change default_sleeptime
        """
        self.default_sleeptime = sleeptime
        
    def login(self):
        """try to log in to www.archives.com, and keep connection
        """
        for i in range(3):
            try:
                self.session.post("http://www.archives.com/member/",
                                  data={"__uid":"efdevices@theeagleforce.net","__pwd":"MYpasswd"})
                print("Successfully login to http://www.archives.com/member/")
                return
            except:
                pass
        raise Exception("Failed to login to http://www.archives.com/member/")
    
    def html(self, url):
        """get utf-8 encoded string of html page
        """
        try:
            return self.session.get(url, 
                        headers=self.default_header, timeout=self.default_timeout).\
                        content.decode("utf-8")
        except:
            return None

spider = ArchivesSpider()

if __name__ == "__main__":
    print(spider.html("http://www.archives.com/member/Default.aspx?_act=VitalSearchResult&LastName=Smith&DeathYear=2012&State=AK&Country=US&Location=AK&ShowSummaryLink=1&RecordType=2&activityID=ad1ef8c1-6bef-4010-aa95-1f089abe0f50"))
#     print(spider.html("http://www.archives.com/member/Default.aspx?_act=VitalSearchResult&LastName=Smith&DeathYear=2007&Country=US&State=&Location=US&ShowSummaryLink=1&RecordType=2&activityID=db4af76f-426b-4e8c-9fe7-0b88b9c4d179&pagesize=10&pageNumber=1&pagesizeAP=10&pageNumberAP=1"))