import os
from dotenv import load_dotenv

load_dotenv()

VNPAY_URL = os.getenv("VNPAY_URL")
VNPAY_TMN_CODE = os.getenv("VNPAY_TMN_CODE")
VNPAY_HASH_SECRET = os.getenv("VNPAY_HASH_SECRET")
VNPAY_RETURN_URL = os.getenv("VNPAY_RETURN_URL")
