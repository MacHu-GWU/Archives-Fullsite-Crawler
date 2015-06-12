##encoding=utf-8

"""
Import Command
--------------
    from archives.htmlparser import htmlparser
"""

from bs4 import BeautifulSoup as BS4
import re

class HTMLParser():
    def get_total_number_of_records(self, html):
        """get how many results returns
        """
        s = re.findall(r"(?<=>Showing 1-10 of ).{1,10}(?=</span>)", html)[0]
        s = s.replace(",", "")
        return int(s)
    
    def extract_records(self, html):
        """record extractor from result page
        silently handle exception
        """
        soup = BS4(html)
        for resultsLists in soup.find_all("div", id="resultsLists"):
            for resultBox in resultsLists.find_all("div", class_ = "resultBox"):
                resultRows = resultBox.find_all("div", class_ = "resultRow")
                resultRows.pop()
                
                record = dict()
                for resultRow in resultRows:
                    field = resultRow.find("div", class_ = "field").text
                    fieldValue = resultRow.find("div", class_ = "fieldValue").text
                    record[field] = fieldValue
                yield record
            break # only need the first resultsLists div block
    
    def records(self, html):
        """deathrecord generator from result page.
        silently handle exception
        """
        soup = BS4(html)
        for resultVital in soup.find_all("div", id = "resultVital"):
            for resultBox in resultVital.find_all("div", class_ = "resultBox"):
                
                resultRows = resultBox.find_all("div", class_ = "resultRow")
                resultRows.pop()
                
                record = dict()
                for resultRow in resultRows:
                    field = resultRow.find("div", class_ = "field").text.strip()
                    fieldValue = resultRow.find("div", class_ = "fieldValue").text.strip()
                    record[field] = fieldValue
                yield record


htmlparser = HTMLParser()

if __name__ == "__main__":
    import requests
    from urlencoder import urlencoder
    def read(fname):
        with open(fname, "rb") as f:
            return f.read().decode("utf-8")
    
    def get_test_data():
        """get some test data for test
        """
        ses = requests.Session()
        ses.post("http://www.archives.com/member/",
                 data={"__uid":"efdevices@theeagleforce.net","__pwd":"MYpasswd"})

        url = urlencoder.url_birth_record("smith", 2000, 10, 1)
        with open(r"test_data\birth.html", "wb") as f:
            f.write(ses.get(url).content)

        url = urlencoder.url_death_record("smith", 2000, 10, 1)
        with open(r"test_data\death.html", "wb") as f:
            f.write(ses.get(url).content)
              
        url = urlencoder.url_marriage_record("smith", 2000, 10, 1)
        with open(r"test_data\marriage.html", "wb") as f:
            f.write(ses.get(url).content)
              
        url = urlencoder.url_divorce_record("smith", 2000, 10, 1)
        with open(r"test_data\divorce.html", "wb") as f:
            f.write(ses.get(url).content)
            
#     get_test_data()

    def test_htmlparser():
#         html = read(r"test_data\birth.html")
#         html = read(r"test_data\death.html")
#         html = read(r"test_data\marriage.html")
        html = read(r"test_data\divorce.html")
        print(htmlparser.get_total_number_of_records(html))
        for record in htmlparser.extract_records(html):
            print(record)
            
    test_htmlparser()