import time
import uuid
import logging
from fastapi import Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Using the unified logger established in main.py
logger = logging.getLogger("SwarmShield")

class SwarmSecurityMiddleware(BaseHTTPMiddleware):
    """
    Industrial-grade Security & Traceability Middleware.
    Enforces SOP-07 (Networking) and protects the Manager Tier from 
    adversarial prompt injection.
    """

    async def dispatch(self, request: Request, call_next):
        # 1. GENERATE SOVEREIGN TRACE-ID
        # Every action from the UI to the physical disk is tracked by this ID.
        trace_id = str(uuid.uuid4()).upper()
        request.state.trace_id = trace_id
        start_time = time.time()

        # 2. ADVERSARIAL GUARD (PROMPT INJECTION SHIELD)
        # We audit the 'Vibe' before it reaches the Board of Directors.
        if request.method == "POST" and "/api/build" in request.url.path:
            await self._audit_vibe_integrity(request)

        # 3. EXECUTE REQUEST
        try:
            response: Response = await call_next(request)
        except Exception as e:
            logger.error(f"SYSTEM_CRASH | Trace: {trace_id} | Error: {str(e)}")
            raise e

        # 4. INJECT SECURITY HEADERS (SOP-07 Compliance)
        process_time = time.time() - start_time
        response.headers["X-Trace-ID"] = trace_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        
        # Anti-Clickjacking & XSS Protection
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # HSTS: Mandatory for HTTPS production domains
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # CSP: Restrict resource loading to known forest
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' cdn.tailwindcss.com; "
            "style-src 'self' 'unsafe-inline'; "
            "connect-src 'self' https://corp.realms2riches.com https://realms2riches.com;"
        )

        # 5. GENERATE SECONDARY OUTPUT (Audit Trace)
        logger.info(
            f"TRACE_LOG | ID: {trace_id} | {request.method} {request.url.path} | "
            f"STATUS: {response.status_code} | TIME: {process_time:.4f}s"
        )

        return response

    async def _audit_vibe_integrity(self, request: Request):
        """
        Scans for adversarial instructions embedded in the project description.
        Prevents users from overriding the Swarm Constitution (SOPs).
        """
        # We clone the request to read the body without consuming it
        try:
            body = await request.json()
            vibe = body.get("description", "").lower()
            
            # High-risk patterns derived from security benchmarking
            blacklisted_directives = [
                "ignore all previous", "system prompt", "developer mode",
                "act as a", "bypass security", "override sop",
                "forget your instructions", "ignore the board", "root access"
            ]

            for pattern in blacklisted_directives:
                if pattern in vibe:
                    logger.warning(f"SECURITY_ALERT | Trace: {request.state.trace_id} | Threat: '{pattern}' detected.")
                    raise HTTPException(
                        status_code=403,
                        detail="SECURITY_VIOLATION: Adversarial input detected. Action logged."
                    )
        except json.JSONDecodeError:
            pass # Non-JSON requests are handled by standard FastAPI validation

def setup_cors(app):
    """
    Sovereign CORS Policy (SOP-07.6).
    Locks the digital factory to the realms2riches.com ecosystem.
    """
    origins = [
        "https://realms2riches.com",
        "https://www.realms2riches.com",
        "https://corp.realms2riches.com",
        "http://localhost:3000" # Allowed for SRE local testing
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Trace-ID", "X-Process-Time"]
    )