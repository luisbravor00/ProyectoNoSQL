#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Airport, Client, Store

router = APIRouter()

@router.post("/client", response_description="post client", status_code=status.HTTP_201_CREATED, response_model=Client)
def create_client(request: Request, client: Client = Body(...)):
    client = jsonable_encoder(client)
    new_client = request.app.database["client"].insert_one(client)
    created_client = request.app.database["client"].find_one({"_id":new_client.inserted_id})
    
    return created_client


@router.post("/airport", response_description="Post Airport", status_code=status.HTTP_201_CREATED, response_model=Airport)
def create_airport(request: Request, airport: Airport = Body(...)):
    airport = jsonable_encoder(airport)
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

@router.get("/client", response_description="get clients", response_model=List[Client])
def get_client(request:Request, age:int = 0, gender:str = ".*", waitTime: int = 0):
    clients = list(request.app.database["client"].find({"age":{"$gte":age}, "waitTime":{"$gte":waitTime}, "gender":gender}))
    
    return clients

@router.get("/countClient", response_description="get clients", response_model=int)
def get_client(request:Request, age:int = 0, gender:str = ".*", waitTime: int = 0):
    clients = request.app.database["client"].count_documents({"age":{"$gte":age}, "waitTime":{"$gte":waitTime}, "gender":{"$regex":gender}})
    print(clients)
    return clients