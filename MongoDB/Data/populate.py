import csv
import requests

BASE_URL = "http://localhost:8000/airport"

def main():
    # with open("storeData.csv") as fd:
        # store_csv = csv.DictReader(fd)
        # for store in store_csv:
            # store["products"] = store["products"].replace("[","")
            # store["products"] = store["products"].replace("]","")
            # store["products"] = store["products"].replace("''","")
            # store["products"] = store["products"].split(",")
            # x = requests.post(BASE_URL+"/store", json=store)
            # print(store)
            # if not x.ok:
                # print(f"Failed to post store {x} - {store}")    
    # 
    # with open("airportData.csv") as fd:
        # airport_csv = csv.DictReader(fd)
        # for airport in airport_csv:
            # airport["stores"] = airport["stores"].replace("[","")
            # airport["stores"] = airport["stores"].replace("]","")
            # airport["stores"] = airport["stores"].replace('""','')
            # airport["stores"] = airport["stores"].split(",")
            # print(airport)
            # x = requests.post(BASE_URL+"/airport", json=airport)
            # if not x.ok:
                # print(f"Failed to post client {x} - {airport}")   


    with open("clientData.csv") as fd:
        client_csv = csv.DictReader(fd)
        for client in client_csv:
            print(client)
            client["age"] = int(client["age"])
            client["waitTime"] = int(client["waitTime"])
            x = requests.post(BASE_URL+"/client", json=client)
            if not x.ok:
                print(f"Failed to post client {x} - {client}")   


if __name__ == "__main__":
    main()