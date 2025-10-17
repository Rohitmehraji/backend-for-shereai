import stripe
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import os

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/create-payment-intent-stripe")
async def create_stripe_payment_intent(request: Request):
    try:
        data = await request.json()
        amount = int(data.get("amount"))
        currency = data.get("currency", "usd")
        plan_name = data.get("plan_name")
        user_email = data.get("user_email")
        intent = stripe.PaymentIntent.create(
            amount=amount * 100,  # dollars to cents
            currency=currency,
            metadata={
                "plan_name": plan_name,
                "user_email": user_email
            },
            automatic_payment_methods={"enabled": True}
        )
        return JSONResponse({
            "success": True,
            "client_secret": intent.client_secret,
            "publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY")
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, 
            sig_header, 
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )
        if event["type"] == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]
            # Activate subscription, send confirmation
        elif event["type"] == "payment_intent.payment_failed":
            payment_intent = event["data"]["object"]
            # Handle failed payment, notify
        elif event["type"] == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            # Deactivate subscription
        return JSONResponse({"status": "success"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
