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

def print_object(answer):
    for ans in answer.keys():
        print(f"{ans}: {answer[ans]}")
    print("="*50)
    
def search_client(age:int, gender:str, waitTime:int):
    suffix = "/client"
    endpoint = app_url + suffix
    params = {
        'age': age,
        'gender': gender,
        'waitTime':waitTime 
    }   
    
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_response = response.json()
        for client in json_response:
            print_object(client)
    else:
        print(f"Error: {response}")
        
def count_client(age:int, gender:str, waitTime:int):
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

def main():
    log.info(f"Welcome store helper. App requests to: {app_url}")
    parser = argparse.ArgumentParser()
    
    list_of_actions = ["search", "count"]
    
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the books library")
    parser.add_argument("-a","--age",
                        help="Search by age", default=None)
    parser.add_argument("-g","--gender",
                        help="Search by gender", default=None)
    parser.add_argument("-w","--waitTime",
                        help="Search by wait time in airport", default=None)
    
    args = parser.parse_args()
    
    if args.action == "search":
        search_client(args.age, args.gender, args.waitTime)
    elif args.action == "count":
        count_client(args.age, args.gender, args.waitTime)


if __name__ == "__main__":
    main()