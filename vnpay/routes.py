from fastapi import APIRouter, Request
from datetime import datetime, timedelta
import urllib.parse

from config import VNPAY_URL, VNPAY_TMN_CODE, VNPAY_HASH_SECRET, VNPAY_RETURN_URL
from .utils import generate_vnpay_signature, verify_vnpay_response

router = APIRouter()


@router.get("/create_payment")
async def create_payment(amount: int, order_desc: str):
    now = datetime.now()
    expire_time = now + timedelta(minutes=15)

    vnp_params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": VNPAY_TMN_CODE,
        "vnp_Amount": amount * 100,
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": now.strftime("%Y%m%d%H%M%S"),
        "vnp_OrderInfo": order_desc,
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": VNPAY_RETURN_URL,
        "vnp_IpAddr": "127.0.0.1",
        "vnp_CreateDate": now.strftime("%Y%m%d%H%M%S"),
        "vnp_ExpireDate": expire_time.strftime("%Y%m%d%H%M%S"),
    }

    vnp_params["vnp_SecureHash"] = generate_vnpay_signature(vnp_params, VNPAY_HASH_SECRET)
    payment_url = f"{VNPAY_URL}?{urllib.parse.urlencode(vnp_params, quote_via=urllib.parse.quote)}"

    return {"payment_url": payment_url}


@router.get("/vnpay_return")
async def vnpay_return(request: Request):
    params = dict(request.query_params)
    
    if verify_vnpay_response(params, VNPAY_HASH_SECRET):
        if params.get("vnp_ResponseCode") == "00" and params.get("vnp_TransactionStatus") == "00":
            return {"message": "Giao dịch thành công!", "data": params}
        return {"message": "Giao dịch không thành công!", "data": params}

    return {"message": "Chữ ký không hợp lệ!"}
