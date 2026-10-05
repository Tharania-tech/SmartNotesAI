from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")

    db = client["smartnotes_ai"]

    collection = db["test"]

    result = collection.insert_one({
        "message": "MongoDB Connected Successfully"
    })

    print("Connected Successfully!")
    print("Inserted ID:", result.inserted_id)

except Exception as e:
    print("Error:", e)