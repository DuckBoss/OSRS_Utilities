import urllib.request
import json
import datetime as dt

class priceCheck:
    # Grabs pricing data from rsbuddy
    jsonURL = "https://rsbuddy.com/exchange/summary.json"

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
        print("\n")

    def pullJSON(self, item):
        with urllib.request.urlopen(self.jsonURL) as url:
            jsonData = json.loads(url.read().decode('utf-8').lower())
            for section in jsonData:
                jsonItem = jsonData[section]
                if jsonItem.get('name') == item or jsonItem.get('id') == item:
                    return  jsonItem

def main():
    startTime = dt.datetime.now()
    program = priceCheck()
    program.main()
    endTime = dt.datetime.now()
    print("Total Runtime: %s" % (endTime - startTime))

if __name__ == "__main__":
    main()
