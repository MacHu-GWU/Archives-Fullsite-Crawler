##encoding=utf-8

from angora.DATA.timewrapper import timewrapper

class DataModel():
    def __init__(self):
        self.key_map = {
            "Birth Date:": "1",
            "Death Date:": "2",
            "Marriage Date:": "3",
            "Divorce Date:": "4",
            "Name:": "5",
            "Location:": "6",
            "Collection:": "7",
            }
        for key, value in list(self.key_map.items()):
            self.key_map[value] = key.replace(":", "")
        self.date_key = set(["Birth Date:", "Death Date:", "Marriage Date:", "Divorce Date:"])
        self.timewrapper = timewrapper
        
    def convert_document(self, doc):
        new_doc = dict()
        for key, value in doc.items():
            if key in self.date_key:
                new_doc[self.key_map[key]] = self.timewrapper.str2datetime(value)
            else:
                new_doc[self.key_map[key]] = value
        return new_doc
    
datamodel = DataModel()

if __name__ == "__main__":
    from pprint import pprint as ppt
    ppt(datamodel.convert_document({'Birth Date:': 'Sep 25, 2000', 'Collection:': 'Vermont, Statewide Birth Records', 'Location:': 'Middlebury, Addison, Vermont, USA', 'Name:': 'Aubrey Colette Smith'}))
    ppt(datamodel.convert_document({'Name:': 'Robert P. Smith', 'Location:': 'Middletown, Middlesex, CT', 'Birth Date:': 'Jun 22, 1910', 'Collection:': 'Connecticut Death Records', 'Death Date:': 'Aug 8, 2000'}))
    ppt(datamodel.convert_document({'Location:': 'Williamson, TX', 'Marriage Date:': 'Jan 4, 2000', 'Name:': 'Patricia Nadine Smith', 'Collection:': 'Texas, Williamson County Marriage Records'}))
    ppt(datamodel.convert_document({'Divorce Date:': 'Oct 18, 2000', 'Name:': 'Rachel Michelle Smith', 'Collection:': 'Oregon Divorce Records', 'Location:': 'Multnomah County, OR'}))
    