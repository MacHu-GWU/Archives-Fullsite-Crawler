##encoding=utf-8

"""
Import Command
--------------
    from archives.urlencoder import urlencoder
"""

import random

class UrlEncoder():
    base_url = "http://www.archives.com/member/"
    available_activity_id = [
        "8d99f71d-432a-428f-b5e4-ad02e84925b4",
        "db4af76f-426b-4e8c-9fe7-0b88b9c4d179",
        "bebd6b46-e347-4667-b476-ac580ec21d48",
        "ad1ef8c1-6bef-4010-aa95-1f089abe0f50",
        "2c6e2876-5342-424c-9223-f3a31be5cac7",
        ]
    def __init__(self):
        self.birth_record_query_url_template = (
                "http://www.archives.com/member/Default.aspx?_act=VitalSearchResult"
                "&LastName=%s"
                "&BirthYear=%s"
                "&Country=US&State=&Location=US&ShowSummaryLink=1&RecordType=1"
                "&activityID=%s"
                "&pagesize=%s"
                "&pageNumber=%s"
                "&pagesizeAP=%s"
                "&pageNumberAP=%s"
                )
        self.death_record_query_url_template = (
                "http://www.archives.com/member/Default.aspx?_act=VitalSearchResult"
                "&LastName=%s"
                "&DeathYear=%s"
                "&Country=US&State=&Location=US&ShowSummaryLink=1&RecordType=2"
                "&activityID=%s"
                "&pagesize=%s"
                "&pageNumber=%s"
                "&pagesizeAP=%s"
                "&pageNumberAP=%s"
                )
        self.marriage_record_query_url_template = (
                "http://www.archives.com/member/Default.aspx?_act=VitalSearchResult"
                "&LastName=%s"
                "&MarriageYear=%s"
                "&Country=US&State=&Location=US&ShowSummaryLink=1&RecordType=3"
                "&activityID=%s"
                "&pagesize=%s"
                "&pageNumber=%s"
                "&pagesizeAP=%s"
                "&pageNumberAP=%s"
                )
        self.divorce_record_query_url_template = (
                "http://www.archives.com/member/Default.aspx?_act=VitalSearchResult"
                "&LastName=%s"
                "&DivorceYear=%s"
                "&Country=US&State=&Location=US&ShowSummaryLink=1&RecordType=4"
                "&activityID=%s"
                "&pagesize=%s"
                "&pageNumber=%s"
                "&pagesizeAP=%s"
                "&pageNumberAP=%s"
                )
    def get_random_activity_id(self):
        return random.choice(self.available_activity_id)

    def url_birth_record(self, lastname, birthyear, pagesize, pagenumber):
        return self.birth_record_query_url_template % (
                lastname, birthyear, self.get_random_activity_id(),
                pagesize, pagenumber, pagesize, pagenumber,
                )
        
    def url_death_record(self, lastname, deathyear, pagesize, pagenumber):
        return self.death_record_query_url_template % (
                lastname, deathyear, self.get_random_activity_id(),
                pagesize, pagenumber, pagesize, pagenumber,
                )

    def url_marriage_record(self, lastname, marriageyear, pagesize, pagenumber):
        return self.marriage_record_query_url_template % (
                lastname, marriageyear, self.get_random_activity_id(),
                pagesize, pagenumber, pagesize, pagenumber,
                )

    def url_divorce_record(self, lastname, divorceyear, pagesize, pagenumber):
        return self.divorce_record_query_url_template % (
                lastname, divorceyear, self.get_random_activity_id(),
                pagesize, pagenumber, pagesize, pagenumber,
                )    
urlencoder = UrlEncoder()

if __name__ == "__main__":
    import unittest
    print(urlencoder.url_birth_record("smith", 2000, 1000, 1))
    print(urlencoder.url_death_record("smith", 2000, 1000, 1))
    print(urlencoder.url_marriage_record("smith", 2000, 1000, 1))
    print(urlencoder.url_divorce_record("smith", 2000, 1000, 1))
    