import csv
import requests

BASE_URL = "http://localhost:8000"

def main():
    with open("airportData.csv") as fd:
        airport_csv = csv.DictReader(fd)
        for airport in airport_csv:
            
            airport["store_name"] = airport["store_name"].replace("[","")
            airport["store_name"] = airport["store_name"].replace("]","")
            airport["store_name"] = airport["store_name"].split(",")
            
            x = requests.post(BASE_URL+"/airport", json=airport)
            print(x)
            if not x.ok:
                print(f"Failed to post airport {x} - {airport}")        

    # with open("clientData.csv") as fd:
        # client_csv = csv.DictReader(fd)
        # for client in client_csv:
            # client["authors"] = client["authors"].replace("[","")
            # client["authors"] = client["authors"].replace("]","")
            # client["authors"] = client["authors"].split(",")
            # x = requests.post(BASE_URL+"/client", json=client)
            # if not x.ok:
                # print(f"Failed to post client {x} - {client}")   
# 
    # with open("storeData.csv") as fd:
        # store_csv = csv.DictReader(fd)
        # for store in store_csv:
            # x = requests.post(BASE_URL+"/store", json=store)
            # if not x.ok:
                # print(f"Failed to post store {x} - {store}")    


if __name__ == "__main__":
    main()