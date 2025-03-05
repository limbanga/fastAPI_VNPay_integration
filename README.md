# FastAPI VNPAY Integration

## Description
This project integrates VNPAY with FastAPI to handle online payments.

## Installation Guide
1. Install Python 3.9+.
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```
3. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the `.env` file:
   ```env
   VNPAY_URL=<VNPAY URL>
   VNPAY_TMN_CODE=<TMN Code>
   VNPAY_HASH_SECRET=<Secret Key>
   VNPAY_RETURN_URL=<Callback URL>
   ```
5. Run the application with FastAPI:
   ```sh
   uvicorn main:app --reload
   ```

## How to Create a VNPAY Account (Sandbox)

**Access the VNPAY Sandbox Page**

1. Register an account by providing your **email** and necessary details.
2. After successful registration, you will receive the required credentials:
   - **vnp_TmnCode**: Test merchant site code.
   - **vnp_HashSecret**: Secret key for data encryption.
   - **API Endpoint**: Test payment API endpoint.

## API Endpoints
- `GET /create_payment?amount=100000&order_desc=Order Payment`
- `GET /vnpay_return` - Receive transaction results from VNPAY

## Workflow Diagram
```mermaid
sequenceDiagram
    participant User
    participant Website
    participant VNPAY
    
    User->>Website: 1. Request payment
    Website->>VNPAY: 2. Send transaction request
    VNPAY-->>Website: 3. Return payment URL
    Website->>User: 4. Redirect to VNPAY
    User->>VNPAY: 5. Enter payment details
    VNPAY-->>Website: 6. Send transaction result
    Website->>User: 7. Display transaction result
```

## Test Results

**Request Payment**

![create_payment_url_endpoint](images/previews/create_payment_url_endpoint.png)

**Server redirects to VNPAY's payment URL**

![VNPAY_payment_url](images/previews/VNPAY_payment_url.png)

**Enter Card Information**

[Link: Test Payment Account](https://sandbox.vnpayment.vn/apis/vnpay-demo/)

![VNPAY_form](images/previews/VNPAY_form.png)

**Payment Result**

*Modify the logic to match your application needs*

![vnpay_return_result](images/previews/vnpay_return_result.png)

## Notes
If you encounter any issues, feel free to reach out for support!

