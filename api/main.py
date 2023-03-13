from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
"""from httpx import request"""
import motor.motor_asyncio
from bson import ObjectId
import pydantic
import requests
from datetime import datetime

app = FastAPI()


origins = [
    "http://127.0.0.1:8000"
    #"https://temperature-sensing.onrender.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client=motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Enginebot:XxGxwdO7zDzBH8hU@cluster1.h0ath04.mongodb.net/?retryWrites=true&w=majority")
db= client.temperature_collection

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

current_time=datetime.now()
temperature= int(input('temp'))
"""{api_key="6998b79864a503ef23fa80755eac9689"
city_name="Kingston"

endpoint ="https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
response= requests.get(endpoint)
if response.status_code== 200:
     time= response.json()
     sunset_time=datetime['sys']['sunset']"""

endpoint= "https://ecse-sunset-api.onrender.com/api/sunset"
response= requests.get(endpoint)
sunset= response.json()
time= datetime.strptime(sunset["sunset"], "%Y-%m-%dT%H:%M:%S.%f")

@app.get("/api/place")
async def get_states():
    fan_light_state= await db["state"].find_one()
    
    if current_time>=time:
         fan_light_state["light"]=True
    else:
         fan_light_state["light"]=False
    
    if fan_light_state["temperature"] >28:
         fan_light_state["fan"]=True
    else:
         fan_light_state["fan"]=False

@app.put("/api/place", status_code=204)
async def create_new_temp(request:Request):
    temp_object= await request.json()

    ready_temp= await db["state"].find_one({"temperature": "celcius"})

    if ready_temp:

        await db["state"].update_one({"temperature":"celsius"},{'$set': temp_object})

    else:
        
        await db["state"].insert_one({**temp_object,"temperature": "celsius"})
    
    new_temp_object= await db["state"].find_one({"temperature":"celsius"})

    return new_temp_object

    