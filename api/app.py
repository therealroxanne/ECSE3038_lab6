from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
import motor.motor_asyncio
from bson import ObjectId
import pydantic
app = FastAPI()


origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

client=motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Enginebot:XxGxwdO7zDzBH8hU@cluster1.h0ath04.mongodb.net/?retryWrites=true&w=majority")
db= client.current_temp

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

"""app.get()"""

app.put("/temperature", status_code=204)
async def create_new_temp(request:Request):
    temp_object= await request.json()

    new_temp= await db["temp_data"].insert_one(temp_object)
    ready_temp= await db["temp_data"].find_one({"_id": new_temp.inserted_id})

    if ready_temp is not None:
         return ready_temp
    
    else:
          raise HTTPException(status_code=400, detail="Bad Request")
         


