from pymongo import MongoClient

user = "root"
password = "toan123"
host = "localhost"

connecturl = "mongodb://{}:{}@{}:27017/?authSource=admin".format(user,password,host)

print("Connecting to mongodb server")
connection = MongoClient(connecturl)

db = connection['training']#connection.training

collection = db['mongodb_glossary']#db.mongodb_glossary

doc1 = {"database":"a database contains collections"}
doc2 = {"collection":"a collection stores the documents"}
doc3 = {"document":"a document contains the data in the form or key value pairs."}

collection.insert_one(doc1)
collection.insert_one(doc2)
collection.insert_one(doc3)

#query and print all the documents in the training database and mongodb_glossary collection.
docs = collection.find()

for document in docs:
    print(document)

# close the server connecton
print("Closing the connection.")
connection.close()