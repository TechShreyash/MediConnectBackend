from urllib.parse import unquote
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
from utils import database
from utils.logger import Logger

app = FastAPI()
logger = Logger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "Api Is Running"}


@app.post("/api/auth")
async def api_auth(request: Request):
    data: dict = await request.json()
    logger.info(f"Auth Data: {data}")

    request_type: Literal["new_auth", "check_auth", "get_shops"] = data.get(
        "request_type"
    )
    email: str = data.get("email")
    password: str = data.get("password")

    if request_type == "new_auth":
        results = await database.new_auth(email, data)
    elif request_type == "check_auth":
        results = await database.check_auth(email, password)
    elif request_type == "check_account_type":
        results = await database.check_account_type(email)

    return results


@app.post("/api/shops")
async def api_shops(request: Request):
    data: dict = await request.json()
    logger.info(f"Shops Data: {data}")

    request_type: Literal["get_shops"] = data.get("request_type")

    medicine_name = data.get("medicine_name")
    medicine_name = unquote(medicine_name)

    user_location = data.get("user_location")

    if request_type == "get_shops":
        results = await database.get_shops(medicine_name, user_location)

    return results


@app.post("/api/medicine")
async def api_med(request: Request):
    data: dict = await request.json()
    logger.info(f"Med_data: {data}")

    request_type: Literal["update_med", "get_med", "add_med","delete_med"] = data.get("request_type")
    email: str = data.get("email")
    Med_data: dict = data.get("Med_data")

    if request_type == "add_med":
        results = await database.add_medicine(email, Med_data)

    elif request_type == "update_med":
        results = await database.update_medicine(email, Med_data)
    elif request_type == "get_med":
        results = await database.get_medicines(email)
    elif request_type == "get_all_med":
        results = await database.get_all_medicine()

    elif request_type == "delete_med":
        results = await database.delete_medicine(email,data.get('id'))

    return results


@app.post("/api/buy")
async def api_buy(request: Request):
    data: dict = await request.json()
    logger.info(f"Med_data: {data}")

    request_type: Literal["buy_med"] = data.get("request_type")
    email: str = data.get("email")
    medicine_id: int = data.get("medicine_id")
    sold_quantity: int = data.get("sold_quantity")

    if request_type == "buy_med":
        results = await database.buy_medicines(email, medicine_id, sold_quantity)
    return results
