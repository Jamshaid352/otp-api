import random
import smtplib
from fastapi import FastAPI
from pydantic import BaseModel
from email.message import EmailMessage

app = FastAPI()

otp_store = {}

FROM_EMAIL = "ka2169389@gmail.com"
APP_PASSWORD = "YOUR_APP_PASSWORD"

class EmailRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    otp: str

@app.get("/")
def home():
    return {"message": "OTP API running"}

@app.post("/send-otp")
def send_otp(data: EmailRequest):

    otp = str(random.randint(1000,9999))
    otp_store[data.email] = otp

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(FROM_EMAIL,APP_PASSWORD)

    msg = EmailMessage()
    msg["Subject"] = "OTP Verification"
    msg["From"] = FROM_EMAIL
    msg["To"] = data.email

    msg.set_content(f"Your OTP is: {otp}")

    server.send_message(msg)
    server.quit()

    return {"message":"OTP Sent"}

@app.post("/verify-otp")
def verify(data: VerifyRequest):

    if otp_store.get(data.email) == data.otp:
        return {"status":"verified"}

    return {"status":"invalid"}
