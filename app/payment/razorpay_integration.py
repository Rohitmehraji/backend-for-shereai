import razorpay
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import os

router = APIRouter()

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET"))
)

@router.post("/create-order-razorpay")
async def create_razorpay_order(request: Request):
    try:
        data = await request.json()
        amount = int(data.get("amount"))            # Amount in rupees
        currency = data.get("currency", "INR")
        plan_name = data.get("plan_name")
        user_email = data.get("user_email")
        order_data = {
            "amount": amount * 100,                 # Amount in paise
            "currency": currency,
            "receipt": f"receipt_{plan_name}_{user_email}",
            "notes": {
                "plan_name": plan_name,
                "user_email": user_email
            }
        }
        order = razorpay_client.order.create(data=order_data)
        return JSONResponse({
            "success": True,
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key_id": os.getenv("RAZORPAY_KEY_ID")
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify-payment-razorpay")
async def verify_razorpay_payment(request: Request):
    try:
        data = await request.json()
        params_dict = {
            'razorpay_order_id': data.get("razorpay_order_id"),
            'razorpay_payment_id': data.get("razorpay_payment_id"),
            'razorpay_signature': data.get("razorpay_signature")
        }
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            return JSONResponse({
                "success": True,
                "message": "Payment verified successfully",
                "payment_id": data.get("razorpay_payment_id")
            })
        except razorpay.errors.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid payment signature")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
