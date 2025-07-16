class Rules:
    @staticmethod
    def add(client, database, collection, data):
        return client[database][collection].insert_one(data)
    
    @staticmethod
    def get(client, database, collection, query):
        return client[database][collection].find_one(query)
    
    @staticmethod
    def get_all(client, database, collection, query):
        return client[database][collection].find(query)
    
    @staticmethod
    def update(client, database, collection, query, data):
        return client[database][collection].update_one(query, {"$set": data})
    
    @staticmethod
    def update_many(client, database, collection, query, data):
        return client[database][collection].update_many(query, {"$set": data})
    
    @staticmethod
    def delete(client, database, collection, query):
        return client[database][collection].delete_one(query)