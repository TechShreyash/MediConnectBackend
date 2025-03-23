from urllib.parse import unquote
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Literal
from utils import database
from utils.logger import Logger
from fastapi import FastAPI, Request, HTTPException, Depends
from datetime import datetime, timedelta, timezone
from google import genai

app = FastAPI()
logger = Logger(__name__)
SECRET_KEY = "your_secret_key"
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key="AIzaSyCulYZDjvxoLbu1qXC4375rX2XYExbUNR8")


@app.post("/api/askai")
async def health_advisor(request: Request):
    data: dict = await request.json()
    logger.info(f"Health Advisor Request: {data}")

    user_prompt = data.get("prompt", "")
    if not user_prompt:
        return {"status": "False", "message": "No prompt provided"}

    # Create a health instructor prompt
    health_prompt = f"""As a pharmacist, provide accurate and helpful advice on the following:
    
    {user_prompt}
    
    Focus only on general wellness information, exercise guidance, nutrition basics, and healthy habits. 
    Do not provide medical diagnoses or treatment recommendations and advice to seek medical professionals for medical conditions.
    [keep the text format in paragraph dont format text.]
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=health_prompt
        )
        return {"status": "True", "response": response.text}
    except Exception as e:
        logger.error(f"Error generating health advice: {str(e)}")
        return {
            "status": "False",
            "message": f"Error generating health advice: {str(e)}",
        }


@app.get("/")
async def root():
    return {"status": "Api Is Running"}


def generate_jwt(email: str):
    payload = {"user": email, "exp": datetime.now(timezone.utc) + timedelta(hours=24)}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


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
        if results.get("status") == "True":
            token = generate_jwt(email)
            results["token"] = token
    elif request_type == "check_auth":
        results = await database.check_auth(email, password)
        if not results:
            return {"status": "False", "message": "No data returned from check_auth"}
        if results.get("status") == "True":
            token = generate_jwt(email)
            results["token"] = token
        return results
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

    request_type: Literal["update_med", "get_med", "add_med", "delete_med"] = data.get(
        "request_type"
    )
    email: str = data.get("email")
    Med_data: dict = data.get("Med_data")

    results = None  # Initialize results

    if request_type == "add_med":
        results = await database.add_medicine(email, Med_data)
    elif request_type == "update_med":
        results = await database.update_medicine(email, Med_data)
    elif request_type == "get_med":
        results = await database.get_medicines(email)
    elif request_type == "get_orders":
        results = await database.get_orders(email)
    elif request_type == "get_all_med":
        results = await database.get_all_medicine()
    elif request_type == "delete_med":
        results = await database.delete_medicine(email, data.get("id"))

    return results


@app.post("/api/buy")
async def api_buy(request: Request):
    data: dict = await request.json()
    logger.info(f"Med_data: {data}")

    request_type: Literal["buy_med"] = data.get("request_type")
    email: str = data.get("email")
    user_mail: str = data.get("user_mail")
    medicine_id: int = data.get("medicine_id")
    sold_quantity: int = data.get("sold_quantity")

    if request_type == "buy_med":
        results = await database.buy_medicines(email, medicine_id, sold_quantity,user_mail)
    return results
