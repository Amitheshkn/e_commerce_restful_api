from typing import List
from typing import Optional

from e_commerce_app.db.definitions import Collection
from e_commerce_app.db.mongo_client import mongodb_client


class MongoAdapter:
    def __init__(self,
                 collection_name: Collection,
                 /):
        self.collection = mongodb_client.db[collection_name]

    def find_document(self,
                      filter_query: dict,
                      /) -> Optional[dict]:
        document = self.collection.find_one(filter_query)
        if document:
            document["id"] = str(document.pop("_id"))
        return document

    def find_documents(self,
                       filter_query: dict,
                       /,
                       *,
                       limit: int = 100) -> List[dict]:
        cursor = self.collection.find(filter_query).limit(limit)
        documents = cursor.to_list(length=limit)
        for doc in documents:
            doc["id"] = str(doc.pop("_id"))
        return documents

    def insert_document(self,
                        document: dict,
                        /) -> str:
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def update_document(self,
                        filter_query: dict,
                        update_data: dict,
                        /) -> bool:
        result = self.collection.update_one(filter_query, update_data)
        return result.modified_count > 0
