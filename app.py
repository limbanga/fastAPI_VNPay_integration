import hashlib
import hmac
import urllib.parse
from fastapi import FastAPI, Request
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import os

app = FastAPI()

VNPAY_URL = os.environ.get("VNPAY_URL")
VNPAY_TMN_CODE =   os.environ.get("VNPAY_TMN_CODE")
VNPAY_HASH_SECRET = os.environ.get("VNPAY_HASH_SECRET") 
VNPAY_RETURN_URL = os.environ.get("VNPAY_RETURN_URL") 


def generate_vnpay_signature(params: dict, secret_key: str):
    """Tạo chữ ký HMAC SHA512 đúng chuẩn VNPAY"""

    if "vnp_SecureHash" in params:
        del params["vnp_SecureHash"]

    sorted_params = sorted(params.items())  # Sắp xếp theo key A-Z
    query_string = "&".join(
        f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params
    )

    print("Chuỗi trước khi hash:", query_string)  # Debug kiểm tra

    signature = hmac.new(
        secret_key.encode(), query_string.encode(), hashlib.sha512
    ).hexdigest()
    return signature


def verify_vnpay_response(params: dict, secret_key: str):
    """Xác thực chữ ký phản hồi từ VNPAY"""

    secure_hash = params.pop("vnp_SecureHash", None)  # Tách chữ ký ra khỏi params
    generated_hash = generate_vnpay_signature(params, secret_key)  # Tạo lại chữ ký

    return secure_hash.lower() == generated_hash.lower()  # So sánh chữ ký


@app.get("/create_payment")
async def create_payment(amount: int, order_desc: str):
    now = datetime.now()
    expire_time = now + timedelta(minutes=15)  # Thời gian hết hạn của đơn hàng

    vnp_params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": VNPAY_TMN_CODE,
        "vnp_Amount": amount * 100,  # VND * 100 (đơn vị là đồng)
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": now.strftime("%Y%m%d%H%M%S"),  # Mã giao dịch duy nhất
        "vnp_OrderInfo": order_desc,
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": VNPAY_RETURN_URL,
        "vnp_IpAddr": "127.0.0.1",
        "vnp_CreateDate": now.strftime("%Y%m%d%H%M%S"),
        "vnp_ExpireDate": expire_time.strftime("%Y%m%d%H%M%S"),  # Thời gian hết hạn
    }

    # Tạo chữ ký
    vnp_params["vnp_SecureHash"] = generate_vnpay_signature(
        vnp_params, VNPAY_HASH_SECRET
    )

    # Tạo URL thanh toán
    payment_url = f"{VNPAY_URL}?{urllib.parse.urlencode(vnp_params, quote_via=urllib.parse.quote)}"

    return {"payment_url": payment_url}


@app.get("/vnpay_return")
async def vnpay_return(request: Request):
    params = dict(request.query_params)  # Lấy dữ liệu từ URL
    if verify_vnpay_response(params, VNPAY_HASH_SECRET):
        if (
            params["vnp_ResponseCode"] == "00"
            and params["vnp_TransactionStatus"] == "00"
        ):
            return {"message": "Giao dịch thành công!", "data": params}
        else:
            return {"message": "Giao dịch không thành công!", "data": params}
    return {"message": "Chữ ký không hợp lệ!"}
