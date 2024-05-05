import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Store(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    storeName: str = Field(...)
    storeType: str = Field(...)
    openingHours: str = Field(...)
    country: str = Field(...)
    products: list = Field(...)    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-48513c7f1f4e",
                "storeName":"Valentina's",
                "storeType":"snacks",
                "openingHours":"7:00 AM to 8:00 PM",
                "country":"United States",
                "products":["spicy chips","sweet chips","coca-cola","apple juice","cookies"]
                
            }
        }
class Airport(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airportCode: str = Field(...)
    name: str = Field(...)
    country: str = Field(...)
    stores: list[Store] = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "airportCode":"DEN",
                "name":"DENVER INTERNATIONAL AIRPORT",
                "country":"US",
                "stores":["Ruby Red Retail","City Lights Corner Store","Emerald Isle Emporium","Harbor Haven Shop","Starlight Supplies"]
                
            }
        }

class Client(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    gender: str = Field(...)
    age: int = Field(...)
    airport: list[Airport] = Field(...)
    travelReason: str = Field(...)    
