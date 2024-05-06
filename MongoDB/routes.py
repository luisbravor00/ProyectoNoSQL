#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Airport, Client, Store

router = APIRouter()

@router.post("/client", response_description="post client", status_code=status.HTTP_201_CREATED, response_model=Client)
def create_clienit(request: Request, client: Client = Body(...)):
    pass


@router.post("/airport", response_description="Post Airport", status_code=status.HTTP_201_CREATED, response_model=Airport)
def create_airport(request: Request, airport: Airport = Body(...)):
    print("Hola soy un aeropuerto")
    airport = jsonable_encoder(airport)
    new_airport = request.app.database["airport"].insert_one(airport)
    created_airport = request.app.database["airport"].find_one({"_id":new_airport.inserted_id})
    
    return created_airport

@router.post("/store", response_description="Post store", status_code=status.HTTP_201_CREATED, response_model=Store)
def create_airport(request: Request, store: Store = Body(...)):
    pass