'''
Many of these methods were inspired by NCR's Catalog Documentation and Docs.
'''

import requests
import re
from HMACAuth import HMACAuth

# method 1: creates an catalog item
def createItem(itemName, version, shortDescription ,location, department):
    url = 'https://gateway-staging.ncrcloud.com/catalog/items/%s' % (itemName)
    payload = "{\"version\":%s,\"shortDescription\":{\"values\":[{\"locale\":\"en-US\",\"value\":\"%s\"}]},\"status\":\"INACTIVE\",\"merchandiseCategory\":\"%s\",\"departmentId\":\"%s\"}" %(
    version, shortDescription, location, department)
    r = requests.put(url, payload, auth=(HMACAuth()))
    return r.json()

# method 2: gets a catalog item based on its name
def getItem(itemName):
    url = url = 'https://gateway-staging.ncrcloud.com/catalog/items/%s' % itemName
    r = requests.get(url,auth=(HMACAuth()))
    return  r.json()

# method 3: get all the items available in the store
def getStoreItems(storeName):
    url = 'https://gateway-staging.ncrcloud.com/catalog/items?merchandiseCategoryId=%s&itemStatus=ACTIVE' % storeName
    r = requests.get(url, auth=(HMACAuth()))
    tempItems = r.json()
    storeItems = []

    for item in tempItems['pageContent']:
        for nestedItem in item['itemId'].values():
            name = nestedItem
            department = item['departmentId']
            result = {}
            result.update({'name': name, 'department': department})
            storeItems.append(result)

    return storeItems

# method 4: create items by price
def createPrice(itemName, itemPriceId, version, price, enterpriseId):
    url = 'https://gateway-staging.ncrcloud.com/catalog/item-prices/%s/%s' % (itemName, itemPriceId)
    payload = "{\"version\":%s,\"price\":%s,\"currency\":\"US Dollar\",\"effectiveDate\":\"2020-07-16T18:22:05.784Z\",\"status\":\"INACTIVE\"}" %(version, price)
    r = requests.put(url,payload,auth=(HMACAuth(enterpriseId)))
    print(r.json)


# method 5: get the price of a catalog item
def getPrice(itemName,itemPriceId,enterpriseId):

    url = 'https://gateway-staging.ncrcloud.com/catalog/item-prices/%s/%s' %(itemName, itemPriceId)
    r = requests.get(url, auth=(HMACAuth(enterpriseId)))
    print(r.json())
    return r.json()

# method 6: get all the prices for all the items in a store
def getAllPrices(itemIds,enterpriseId):
    url = 'https://gateway-staging.ncrcloud.com/catalog/item-prices/get-multiple'
    itemNames = []

    for i in range(len(itemIds)):
        itemNames.append(itemIds[i]['name'])

    modifiedItems  = createJsonString(itemNames)

    payload = "{\"itemIds\":[%s]}" %modifiedItems

    r = requests.post(url,payload, auth=(HMACAuth(enterpriseId)))

    tempPrices = r.json()

    itemsWithPrices = []
    j = 0
    for item in tempPrices['itemPrices']:
        result = {}
        price = item.get('price')
        nested = item.get('priceId')
        name = nested.get('itemCode')
        department = -99

        for collection in itemIds:
            if collection['name'] == name:
                department = collection['department']



        price = addChange(price)
        name = addSpacesInbetweenCaptialLetters(name)
        if isUnique(itemsWithPrices,name):
            result.update({'name': name, 'price': price, 'department': department })
            itemsWithPrices.append(result)
            j += 1
        else:

            result.update({'name': name, 'price': price})


    return itemsWithPrices

# method 7: create json strings for get prices functions
def createJsonString(items):
    String = ""

    for  item in items:
        String =  String + "{\"itemCode\":\"%s\"}," %item

    String =String.rstrip(',')

    return String


def isUnique(dict_list,item):
    for d in dict_list:
        if d['name'] == item:
            return False
    return True


