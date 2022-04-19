from flask import Flask, request, json, Response
from pymongo import MongoClient



############ defininig  read function from db
def read(self):
    documents = self.collection.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    return output
#############  define write function to db
    def write(self, data):
        log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

#####################  define update function
    def update(self):
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output
    ##############  define delete from db
    def delete(self, data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

#############  creating class for use in our database


class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient("mongodb://localhost:5000/")

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

############################   test reading data

if __name__ == '__main__':
    data = {
        "database": "movie_posters",
        "collection": "movies",
    }
    mongo_obj = MongoAPI(data)
    print(json.dumps(mongo_obj.read(), indent=4))