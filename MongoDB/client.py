import argparse
import logging
import os
import requests

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('store.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
app_url = os.getenv("app_url", "http://localhost:8000/airport")

def print_object(obj):
    for ans in obj.keys():
        if type(obj[ans]) == dict:
            print_object(obj[ans])
        else:
            print(f"{ans}: {obj[ans]}")
    print("="*50)

def print_list(list):
    for element in list:
        print(element)   
        
def search_client(age:int, gender:str, waitTime:int, travelReason:str, fromDate:str, toDate:str):
    suffix = "/client"
    endpoint = app_url + suffix
    params = {
        'age': age,
        'gender': gender,
        'waitTime':waitTime,
        'travelReason':travelReason, 
        'fromDate':fromDate, 
        'toDate':toDate 
        
    }   
    
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_response = response.json()
        for client in json_response:
            print_object(client)
    else:
        print(f"Error: {response}")
        
def count_client(age:int, gender:str, waitTime:int, travelReason:str, fromDate:str, toDate:str):
    suffix = "/countClient"
    endpoint = app_url + suffix
    params = {
        'age': age,
        'gender': gender,
        'waitTime':waitTime 
    }   
    
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_response = response.json()
        print("Registros encontrados -> ",json_response)
    else:
        print(f"Error: {response}")
        
def list_stores(airport:str, store:str, product:str):
    suffix = '/airport'
    endpoint = app_url + suffix
    params = {
        'airport':airport,
        'store':store,
        'product':product
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_response = response.json()
        for airport in json_response:        
            print_object(airport)
    else:
        print(f"Error: {response}")
    


def main():
    log.info(f"Welcome store helper. App requests to: {app_url}")
    parser = argparse.ArgumentParser()
    
    list_of_actions = ["search", "count", "list"]
    
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the books library")
    parser.add_argument("-a","--age",
                        help="Search by age", default=None)
    parser.add_argument("-g","--gender",
                        help="Search by gender", default=None)
    parser.add_argument("-w","--waitTime",
                        help="Search by wait time in airport", default=None)
    parser.add_argument("-tr","--travelReason",
                        help="Search fro travel reason", default=None)
    parser.add_argument("-f","--fromDate",
                        help="Set a date to start the search yyy/mm/dd", default=None)
    parser.add_argument("-t","--toDate",
                        help="set a limit date for the search yyy/mm/dd", default=None)
    parser.add_argument("-p","--airport",
                        help="Search a specific airport", default=None)
    parser.add_argument("-s","--store",
                        help="Search a store by it's name", default=None)
    parser.add_argument("-pd","--product",
                        help="Search a product", default=None)
    
    args = parser.parse_args()
    
    if args.action == "search":
        search_client(args.age, args.gender, args.waitTime, args.travelReason, args.fromDate, args.toDate)
    elif args.action == "count":
        count_client(args.age, args.gender, args.waitTime, args.travelReason , args.fromDate, args.toDate)
    elif args.action == "list":
        list_stores(args.airport, args.store, args.product)

if __name__ == "__main__":
    main()