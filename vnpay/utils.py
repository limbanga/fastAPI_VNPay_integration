import hashlib
import hmac
import urllib.parse


def generate_vnpay_signature(params: dict, secret_key: str) -> str:
    """Tạo chữ ký HMAC SHA512 cho VNPAY"""

    params.pop("vnp_SecureHash", None)  # Xóa chữ ký cũ nếu có
    sorted_params = sorted(params.items())  # Sắp xếp key A-Z
    query_string = "&".join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted_params)

    signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha512).hexdigest()
    return signature


def verify_vnpay_response(params: dict, secret_key: str) -> bool:
    """Xác thực chữ ký phản hồi từ VNPAY"""

    secure_hash = params.pop("vnp_SecureHash", None)
    generated_hash = generate_vnpay_signature(params, secret_key)
    return secure_hash.lower() == generated_hash.lower() if secure_hash else False
