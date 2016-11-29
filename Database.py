from pymongo import MongoClient

class Database:

    def __int__(self):
        self.client = MongoClient ("10.192.69.41")
        self.db = self.client.supplyChain
        self.bomhs = self.db.bomHS
        self.hs = self.db.HS

    def queryBom(self, bom):
        '''returns the hs code'''
        cursor = self.hs.find({"Part Number":bom})
        if cursor.count() > 0:
            return cursor[0]["HS Code"]
        return "not found"

    def queryHS(self, hs):
        return


class Query:
    def __int__(self):
        self.adValoremPercentage = None
        self.fodinfaPercentage = None
        self.safeguardPercentage = None
        self.vatPercentage = None
        self.hsCode = None


