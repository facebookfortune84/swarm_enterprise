import os
import json
import stripe
import logging
from fastapi import APIRouter, Request, Header, HTTPException
from backend.db.linear_engine import swarm_db
from backend.api.routes import create_company_bundle
from agents.tools.email_tools import EmailTools

router = APIRouter(prefix="/api/webhooks", tags=["Monetization"])
logger = logging.getLogger("SwarmWebhooks")

# These keys are verified as present in your .env
stripe.api_key = os.getenv("STRIPE_API_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/stripe")
async def stripe_webhook(request: Request, x_stripe_signature: str = Header(None)):
    """
    The Revenue Gate:
    Validates Stripe signatures and triggers the autonomous delivery of 'The Box'.
    """
    payload = await request.body()
    
    try:
        # 1. Cryptographic Verification of the request source
        event = stripe.Webhook.construct_event(
            payload, x_stripe_signature, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        logger.error(f"WEBHOOK_ERROR: Invalid payload. {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"WEBHOOK_ERROR: Signature verification failed. {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # 2. Handle the 'Checkout Session Completed' event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_details', {}).get('email')
        
        logger.info(f"PAYMENT_SUCCESS: Order received from {customer_email}")

        # 3. Trigger Autonomous Delivery
        # We leverage the existing Replicator logic to birth a new Company instance
        bundle_result = await create_company_bundle(request)
        download_url = bundle_result.get("download_url")

        # 4. Use the Swarm's Email Tool to deliver the asset
        email_sender = EmailTools()
        subject = "Your Programmable Company is Ready for Deployment"
        body = f"""
        <h1>Welcome to the Swarm, {customer_email}</h1>
        <p>Your purchase of Swarm Enterprise OS v1.0 was successful.</p>
        <p><strong>Your Digital Factory:</strong> <a href='{download_url}'>Download ZIP</a></p>
        <p>To launch, extract the ZIP and run 'START_COMPANY.bat' as Administrator.</p>
        <br/>
        <p>Best Regards,</p>
        <p>Realms2Riches Autonomous Fulfillment Swarm</p>
        """
        
        delivery_status = email_sender.send_email(
            target_email=customer_email,
            subject=subject,
            body=body
        )
        
        # 5. Log the event in the Linear Engine for audit
        logger.info(f"FULFILLMENT_STATUS: {delivery_status}")

    return {"status": "success"}