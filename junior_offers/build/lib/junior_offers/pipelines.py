# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JuniorOffersPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        fieldNames = adapter.field_names()

        listName = ["locations","stack","salary"]

        for fieldName in fieldNames:
            if fieldName not in listName:
                if adapter[fieldName] is not None:
                    adapter[fieldName] = adapter.get(fieldName).strip()

        # Strip locations 
        locations = adapter.get("locations")
        formattedLocations = []
        for location in locations:
            formattedLocations.append(location.strip())
        adapter["locations"] = formattedLocations;
        
        # Strip tech stack
        strippedTech = []
        for tech in adapter.get("stack"):
            strippedTech.append(tech.strip())
        adapter["stack"] = strippedTech

        # Format salary info 
        salariesInfo = adapter.get("salary")
        salaries = list(filter(lambda x: x not in " PLN ",salariesInfo["salaries"]))
        salaries = [x.replace(" ", "").replace("\xa0","").replace("\u2013"," - ") for x in salaries]
        salariesTypes = [x.split("(")[1].split(")")[0] for x in salariesInfo["salariesTypes"]]
        newSalariesInfo = []
        for index, salaryType in enumerate(salariesTypes):
            newSalariesInfo.append({"salary":salaries[index],"salaryType":salaryType})
        adapter["salary"] = newSalariesInfo

        return item

from pymongo import MongoClient
import certifi

class SaveToMongoDBPipeline:
    def __init__(self):
        connection_string= f"mongodb+srv://danexq:nirLnr7kwAjljss6@joboffers.jjwhd3n.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection_string,tlsCAFile=certifi.where())
        self.collection = client.JobOffers.get_collection("JobOffers")
        self.offersInDb= [x for x in self.collection.find({}, {'_id':0})]
        

    def process_item(self,item,spider): 
        if item not in self.offersInDb:
            itemAdapter = ItemAdapter(item)
            print("Adding: " , itemAdapter.values)
            self.collection.insert_one(dict(item))
        return item
        
        