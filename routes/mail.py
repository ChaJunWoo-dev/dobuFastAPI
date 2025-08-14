from pydantic import EmailStr, BaseModel
from typing import List
from fastapi import BackgroundTasks, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from starlette.responses import JSONResponse
from fastapi import APIRouter
import random
import string
from redisConfig import rd
from starlette.config import Config

config = Config(".env")


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME=config("MAIL_USERNAME"),
    MAIL_PASSWORD=config("MAIL_PASSWORD"),
    MAIL_FROM=config("MAIL_USERNAME"),
    MAIL_PORT=config("MAIL_PORT"),
    MAIL_SERVER=config("MAIL_SERVER"),
    MAIL_FROM_NAME="[DOBU]",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

verification_codes = {}


class EmailVerificationRequest(BaseModel):
    email: EmailStr


router = APIRouter()


def generate_verification_code(length=6):
    characters = string.ascii_uppercase + string.digits
    verification_code = "".join(random.choice(characters) for _ in range(length))

    return verification_code


def store_verification_code(email):
    verification_code = generate_verification_code()

    rd.set(f"{email}_verification_code", verification_code, ex=120)

    return verification_code


@router.post("/send/verify/email/background")
async def send_in_background(
    background_tasks: BackgroundTasks, email: EmailSchema
) -> JSONResponse:
    request_email = email.email[0]
    verification_code = store_verification_code(request_email)
    html = f"""
        <p>인증 코드는 2분간 유효합니다.</p>
        <p style='font-size: 24px;'><b>{verification_code}</b></p>
        <p>타인에게 인증 코드를 절대 알려주지 마세요<p>
    """
    message = MessageSchema(
        subject="[DOBU] 이메일 인증코드입니다",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})


def is_code_valid(email, input_code):
    stored_code = rd.get(f"{email}_verification_code")

    if stored_code is None:
        return False

    return input_code == stored_code.decode("utf-8")


class VerifyRequest(BaseModel):
    email: str
    input_code: str


@router.post("/verify/email_code")
def verifyCode(request: VerifyRequest):
    is_ok = is_code_valid(request.email, request.input_code)

    if is_ok:
        return {"message": "Verification successful"}
    else:
        raise HTTPException(
            status_code=400, detail="Invalid or expired verification code"
        )
