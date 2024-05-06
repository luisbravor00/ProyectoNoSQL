#!/usr/bin/env python3
import os

from fastapi import FastAPI
from pymongo import MongoClient

from routes import router as app_router


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'DB_PROJECT')

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]
    print(f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("GG wp")

app.include_router(app_router, tags=["airport"], prefix="/airport")
