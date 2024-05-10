#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import random

from datetime import datetime
from model import Airport, Client, Store

router = APIRouter()
BASE_URL = "http://localhost:8000/airport"

@router.post("/client", response_description="post client", status_code=status.HTTP_201_CREATED, response_model=Client)
def create_client(request: Request, client: Client = Body(...)):
    client = jsonable_encoder(client)
    new_client = request.app.database["client"].insert_one(client)
    created_client = request.app.database["client"].find_one({"_id":new_client.inserted_id})
    
    return created_client


@router.post("/airport", response_description="Post Airport", status_code=status.HTTP_201_CREATED, response_model=Airport)
def create_airport(request: Request, airport: Airport = Body(...)):
    airport = jsonable_encoder(airport)
    # print(airport["stores"])
    new_stores = []
    for store in airport['stores']:
        #print("suffix->", BASE_URL+suffix)
        x = get_stores(request, store)
        num = random.randint(0, len(x)-1)
        new_stores.append(x[num])
    airport["stores"] = new_stores        
    new_airport = request.app.database["airport"].insert_one(airport)
    created_airport = request.app.database["airport"].find_one({"_id":new_airport.inserted_id})
    
    return created_airport

@router.post("/store", response_description="Post store", status_code=status.HTTP_201_CREATED, response_model=Store)
def create_airport(request: Request, store: Store = Body(...)):
    store = jsonable_encoder(store)
    new_store = request.app.database["store"].insert_one(store)
    created_store = request.app.database["store"].find_one({"_id":new_store.inserted_id})
    
    return created_store

@router.get("/store", response_description="Get stores", response_model=List[Store])
def get_stores(request:Request, storeName:str):
    stores = list(request.app.database["store"].find({"storeName": storeName}))
    return stores

@router.get("/client", response_description="get clients", response_model=List)
def get_client(request:Request, age:int = 0, gender:str = "", waitTime: int = 0, travelReason:str='', fromDate:str = '2000-01-01',toDate:str='2030-01-01'):
    
    fromDate = datetime.strptime(fromDate, "%Y-%m-%d")
    toDate = datetime.strptime(toDate, "%Y-%m-%d")
    clients = list(request.app.database["client"].find({"age":{"$gte":age}}))
    for client in clients:
        client["_id"] = str(client["_id"])
    return clients

@router.get("/countClient", response_description="get clients", response_model=int)
def get_client(request:Request, age:int = 0, gender:str = ".*", waitTime: int = 0, travelReason:str='.*', fromDate:str = '2000-01-01', toDate:str='2030-01-01'):
    
    fromDate = datetime.strptime(fromDate, "%Y-%m-%d")
    toDate = datetime.strptime(toDate, "%Y-%m-%d")
    clients = request.app.database["client"].count_documents({"age":{"$gte":age}, "waitTime":{"$gte":waitTime}, "gender":{"$regex":gender}, 
                                                        'travelReason':{"$regex":travelReason}, 'flightDate':{"$gte":fromDate}, 'flightDate':{"$lte":toDate}})

    return clients

@router.get("/airport", response_description="airports clients", response_model=List)
def get_airport(request:Request, airport:str = '.*', store:str = '.*', product:str='.*'):
    print(airport)
    pipeline = [
        { "$match": { "airportCode": airport } }
    ]
    if store != '.*':
        pipeline.append({'$unwind':'$stores'})
        pipeline.append({'$match':{"stores.storeName":{"$regex":store}}})
    
    if product != '.*':
        pipeline.append({'$unwind':'$stores.products'})
        pipeline.append({'$match':{"stores.products":{"$regex":product}}})
        
    # print(pipeline)
    airports = list(request.app.database["airport"].aggregate(pipeline))
    print(airports)
    return airports