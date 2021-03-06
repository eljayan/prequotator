from pymongo import MongoClient

client = MongoClient ("10.192.69.41")
db = client.get_database("supplyChain")
bomhscollection = db.get_collection("bomHS")
hscollection = db.get_collection("HS")
common = db.get_collection("commonRegimes")


def queryBom(bom):
    '''returns the hs code'''
    cursor = bomhscollection.find({"Part Number":bom})

    if cursor.count() > 0:
        return cursor[0]["HS Code"]
    return "not found"


def queryHS(hs):
    '''retruns mongo cursor object'''
    cursor = hscollection.find({"HS Code":hs})
    if cursor.count() > 0:
        return cursor
    return


def queryPL(pl):
    '''returns cursor object'''
    cursor = common.find({"pl_number":{"$regex":pl}})
    if cursor.count()>0:
        return cursor
    return