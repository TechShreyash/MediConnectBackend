from datetime import datetime
import certifi
import math
import jwt
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Literal
from utils.logger import Logger

SECRET_KEY = "your_secret_key"
logger = Logger(__name__)

logger.info("Connecting to MongoDB")
DB = AsyncIOMotorClient(
    "mongodb+srv://somya15:Somya%401528@somya15.wl3vu.mongodb.net/",
    tls=True,
    tlsCAFile=certifi.where(),
)["MediConnect"]
logger.info("Connected to MongoDB")

ACCOUNTDB = DB["ACCOUNTDB"]


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (
        math.sin(dLat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dLon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


async def new_auth(email: str, data, token: str = None):
    if token:
        decode_token(token)
    if await ACCOUNTDB.find_one({"email": email}):
        return {"status": False, "token": ""}
    await ACCOUNTDB.insert_one(data)
    new_token = jwt.encode({"email": email}, SECRET_KEY, algorithm="HS256")
    return {"status": True, "token": new_token}


async def check_auth(email: str, password: str, token: str = None):
    if token:
        decode_token(token)
    user = await ACCOUNTDB.find_one({"email": email})
    if user and user["password"] == password:
        new_token = jwt.encode({"email": email}, SECRET_KEY, algorithm="HS256")
        return {"status": True, "token": new_token}
    return {"status": False, "token": ""}


async def check_account_type(email: str):
    acc = await ACCOUNTDB.find_one({"email": email})
    if acc:
        new_token = jwt.encode({"email": email}, SECRET_KEY, algorithm="HS256")
        return {"status": True, "type": acc["type"], "token": new_token}
    return {"status": False, "message": "Email not found"}


async def get_shops(medicine_name, user_location, token: str = None):
    if token:
        decode_token(token)
    shops = []
    async for shop in ACCOUNTDB.find({"type": "shop"}):
        shop.pop("_id", None)
        shop.pop("password", None)
        for medicine in shop.get("medicine", []):
            if medicine["name"] == medicine_name:
                data = {
                    "shop_name": shop["name"],
                    "shop_location": shop["location"],
                    "distance": calculate_distance(
                        float(user_location["lat"]),
                        float(user_location["long"]),
                        float(shop["location"]["lat"]),
                        float(shop["location"]["long"]),
                    ),
                    "price": medicine["price"],
                    "id": medicine["id"],
                    "shop_email": shop["email"],
                    "frequency": medicine["dosage"],
                    "sideeffect": medicine["side_effects"],
                    "precaution": medicine["precautions"],
                }
                shops.append(data)
                break
    shops.sort(key=lambda x: x["distance"])
    return {"status": True, "shops": shops}


async def update_account(email: str, data: dict, token: str = None):
    if token:
        decode_token(token)
    await ACCOUNTDB.update_one({"email": email}, {"$set": data}, upsert=True)
    return {"status": True, "message": "Account Updated"}


async def get_account(email: str, token: str = None):
    if token:
        decode_token(token)
    account = await ACCOUNTDB.find_one({"email": email})
    if account:
        return {"status": True, "data": account}
    return {"status": False, "message": "Email not found"}


async def add_medicine(email: str, data: dict, token: str = None):
    if token:
        decode_token(token)
    await ACCOUNTDB.update_one(
        {"email": email}, {"$push": {"medicine": data}}, upsert=True
    )
    return {"status": True, "message": "Medicine added"}


async def update_medicine(email: str, data: dict, token: str = None):
    if token:
        decode_token(token)
    await ACCOUNTDB.update_one(
        {"email": email, "medicine.id": data["id"]},
        {"$set": {"medicine.$.quantity": data["quantity"]}},
        upsert=True,
    )
    return {"status": True, "message": "Medicine updated"}


async def get_medicines(email: str, token: str = None):
    if token:
        decode_token(token)
    shop_data = await ACCOUNTDB.find_one({"email": email})
    return {
        "status": True,
        "medicine": shop_data.get("medicine", []) if shop_data else [],
    }


async def get_orders(email: str, token: str = None):
    if token:
        decode_token(token)
    shop_data = await ACCOUNTDB.find_one({"email": email})
    data = {
        "status": True,
        "orders": shop_data.get("orders", []) if shop_data else [],
    }
    data["orders"].reverse()
    return data


async def buy_medicines(
    email: str,
    medicine_id: int,
    sold_quantity: int,
    token: str = None,
):
    if token:
        decode_token(token)

    ctime = datetime.now().strftime("%H:%M:%S")
    cdate = datetime.now().strftime("%Y-%m-%d")  # Adjust the date format as needed

    medi = await ACCOUNTDB.find_one({"email": email, "medicine.id": int(medicine_id)})

    for i in medi["medicine"]:
        if i["id"] == int(medicine_id):
            medicine_name = i["name"]
            break

    result = await ACCOUNTDB.update_one(
        {"email": email, "medicine.id": int(medicine_id)},
        {
            "$inc": {
                "medicine.$.quantity": -int(sold_quantity),
                "medicine.$.units_sold": int(sold_quantity),
            },
            "$push": {
                "orders": {
                    "id": int(medicine_id),
                    "medicine": medicine_name,
                    "quantity": int(sold_quantity),
                    "date": cdate,
                    "time": ctime,
                    "status": "Delivered",
                }
            },
        },
        upsert=True,
    )

    return {"status": True, "message": "Medicine Sold"}


async def get_all_medicine():
    medicines = []
    async for shop in ACCOUNTDB.find({"type": "shop"}):
        if shop.get("medicine", []) != []:
            for medicine in shop["medicine"]:
                medicines.append(medicine["name"])

    return {"status": True, "medicines": list(set(medicines))}


async def delete_medicine(email: str, id, token: str = None):
    if token:
        decode_token(token)
    await ACCOUNTDB.update_one({"email": email}, {"$pull": {"medicine": {"id": id}}})
    return {"status": True, "message": "Medicine Deleted"}
