from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict
class TripOut(BaseModel):
 model_config=ConfigDict(from_attributes=True)
 id:str;operator:str;bus_name:str;origin:str;destination:str;departure_at:datetime;arrival_at:datetime;fare_paise:int;seat_layout:str
class HoldIn(BaseModel): trip_id:str;seat_ids:list[str]=Field(min_length=1,max_length=6);owner_token:str=Field(min_length=8,max_length=80)
class PassengerIn(BaseModel): owner_token:str=Field(min_length=8,max_length=80);passenger_name:str=Field(min_length=2,max_length=120);email:str=Field(min_length=5,max_length=254);phone:str=Field(min_length=8,max_length=20)
