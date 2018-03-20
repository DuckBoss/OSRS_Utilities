import urllib.request
import json
import datetime as dt
import matplotlib.pyplot as plt

class priceCheck:

    #https://api.rsbuddy.com/grandExchange?a=graph&g=30&start=1474615279000&i=2
    #&g = increments
    #&start = start in unix ms (defaults to 1 week)
    jsonURL_GRAPH = "https://api.rsbuddy.com/grandExchange?a=graph"
    jsonURL_ID = "https://rsbuddy.com/exchange/summary.json"
    itemID = None
    itemName = None

    def __init__(self):
        print("OSRS Price Checker Initialized!")

    def main(self):
        searchCriteria = self.manageSearchCriteria(input("Please input either the item name or item ID: "))
        searchIncrement = int(input("Please input an increment value (1440 daily, 60 hourly, 30 half hourly): "))

        self.pullJSON_ID(searchCriteria)
        itemHistoryData = self.pullJSON_GRAPH(self.itemID, searchIncrement)

        print(itemHistoryData)

    def manageSearchCriteria(self, searchCriteria):
        try:
            return int(searchCriteria)
        except ValueError:
            return searchCriteria.lower()

    def pullJSON_ID(self, item):
        returnItem = None
        with urllib.request.urlopen(self.jsonURL_ID) as url:
            jsonData = json.loads(url.read().decode('utf-8').lower())
            for section in jsonData:
                jsonItem = jsonData[section]
                if jsonItem.get('name') == item or jsonItem.get('id') == item:
                    returnItem = jsonItem
        self.itemID = returnItem.get('id')
        self.itemName = returnItem.get('name')

    def pullJSON_GRAPH(self, id, searchIncrement):
        self.jsonURL_GRAPH += '&g={}&i={}'.format(searchIncrement, id)

        buyingprice = []
        sellingprice = []
        overallprice = []
        with urllib.request.urlopen(self.jsonURL_GRAPH) as url:
            jsonData = json.loads(url.read().decode('utf-8').lower())
            for section in jsonData[:-1]:
                buyingprice.append(section.get("buyingprice"))
                sellingprice.append(section.get("sellingprice"))
                overallprice.append(section.get("overallprice"))

        plt.plot(buyingprice, 'r', sellingprice, 'b', overallprice, 'g', linewidth=1)
        plt.ylabel("Price(gp)")
        plt.xlabel("Data points from last 7 days")
        plt.title("Price History of ID:{}".format(id))
        plt.show()


def main():
    startTime = dt.datetime.now()
    program = priceCheck()
    program.main()
    endTime = dt.datetime.now()
    print("Total Runtime: %s" % (endTime - startTime))

if __name__ == "__main__":
    main()
