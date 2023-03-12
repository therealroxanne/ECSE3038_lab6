from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from httpx import request
import motor.motor_asyncio
from bson import ObjectId
import pydantic
from datetime import datetime

app = FastAPI()


origins = [
    "http://localhost:8000"
    "https://temperature-sensing.onrender.com"
]
client=motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Enginebot:XxGxwdO7zDzBH8hU@cluster1.h0ath04.mongodb.net/?retryWrites=true&w=majority")
db= client.temperature_collection

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

current_time=datetime.now()

api_key="6998b79864a503ef23fa80755eac9689"
city_name="Kingston"

endpoint ="https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
response= request.get(endpoint)
if response.status_code== 200:
     time= response.json()
     sunset_time=time['sys']['sunset']


app.get("/api/state")
async def get_states():
     fan_light_state= await db["state"].find().to_list(999)
    
     if current_time>=sunset_time:
         fan_light_state["light"]== True
     else:
         fan_light_state["light"]== False
    
     if fan_light_state["temperature"]>"28.0":
         fan_light_state["fan"]=True
     else:
         fan_light_state["fan"]=False

app.put("/temperature", status_code=204)
async def create_new_temp(request:Request):
    temp_object= await request.json()

    new_temp= await db["temp_data"].insert_one(temp_object)
    ready_temp= await db["temp_data"].find_one({"_id": new_temp.inserted_id})

    if ready_temp is not None:
         return ready_temp
    
    else:
          raise HTTPException(status_code=400, detail="Bad Request")
         


"""uvicorn api.main:app --reload"""