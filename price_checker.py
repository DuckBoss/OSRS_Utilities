import urllib.request
import json
import datetime as dt

class priceCheck:

    jsonURL = "https://rsbuddy.com/exchange/summary.json"
    jsonURL_2 = "https://api.rsbuddy.com/grandExchange?a=guidePrice&i="

    def __init__(self):
        print("OSRS Price Checker Initialized!")

    def main(self):
        searchCriteria = self.manageSearchCriteria(input("Please input either the item name or item ID: "))
        allItemData = self.pullJSON(searchCriteria)
        if allItemData is not None:
            print("SUCCESS: Valid data found for the given search item!\n")
        else:
            print("ERROR: No valid data found for the given search item.\n")

        print(self.printFormat(allItemData))

    def manageSearchCriteria(self, searchCriteria):
        try:
            return int(searchCriteria)
        except ValueError:
            return searchCriteria.lower()

    def printFormat(self, itemData):
        print("Item ID: %s" %itemData.get('id'))
        print("Item Name: %s" %itemData.get('name'))
        print("Average Buy Price: %s gp" %itemData.get('buy_average'))
        print("Average Sell Price: %s gp" %itemData.get('sell_average'))
        print("Buying Quantity: %s" % itemData.get('buying_quantity'))
        print("Selling Quantity: %s" % itemData.get('selling_quantity'))
        print("\n")

    def pullJSON(self, item):
        returnItem = None
        with urllib.request.urlopen(self.jsonURL) as url:
            jsonData = json.loads(url.read().decode('utf-8').lower())
            for section in jsonData:
                jsonItem = jsonData[section]
                if jsonItem.get('name') == item or jsonItem.get('id') == item:
                    returnItem = jsonItem


        self.jsonURL_2 += str(returnItem.get('id'))
        with urllib.request.urlopen(self.jsonURL_2) as url_2:
            jsonDataExtra = json.loads(url_2.read().decode('utf-8').lower())
            print(jsonDataExtra)
            returnItem['buying_quantity'] = jsonDataExtra.get('buyingquantity')
            returnItem['selling_quantity'] = jsonDataExtra.get('sellingquantity')
        return returnItem

def main():
    startTime = dt.datetime.now()
    program = priceCheck()
    program.main()
    endTime = dt.datetime.now()
    print("Total Runtime: %s" % (endTime - startTime))

if __name__ == "__main__":
    main()
