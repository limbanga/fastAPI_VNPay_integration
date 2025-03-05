from fastapi import FastAPI
from vnpay.routes import router as vnpay_router

app = FastAPI()

# Thêm các routes của VNPAY vào app
app.include_router(vnpay_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
