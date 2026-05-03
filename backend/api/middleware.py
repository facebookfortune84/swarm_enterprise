import time
import uuid
import logging
from fastapi import Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger("SwarmShield")

class SwarmSecurityMiddleware(BaseHTTPMiddleware):
    """
    Enterprise-grade security middleware for Swarm OS.
    Handles Trace-ID generation, Request Logging, and Adversarial Input Filtering.
    """

    async def dispatch(self, request: Request, call_next):
        # 1. Generate Unique Trace ID for this request cycle
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id
        start_time = time.time()

        # 2. Adversarial Guard: Scan 'Vibe' inputs for prompt injection
        # This protects the Groq 70B brain from being hijacked
        if request.method == "POST" and "/api/build" in request.url.path:
            await self._audit_vibe_input(request)

        # 3. Process the request
        response: Response = await call_next(request)

        # 4. Inject Security Headers per SOP-07.3.2
        process_time = time.time() - start_time
        response.headers["X-Trace-ID"] = trace_id
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' cdn.tailwindcss.com; style-src 'self' 'unsafe-inline';"

        # 5. Log the Trace (Secondary Output)
        logger.info(
            f"TRACE: {trace_id} | METHOD: {request.method} | "
            f"PATH: {request.url.path} | STATUS: {response.status_code} | "
            f"TIME: {process_time:.4f}s"
        )

        return response

    async def _audit_vibe_input(self, request: Request):
        """
        Adversarial Input Sanitization.
        Looks for common injection patterns that target Level 1 Managers.
        """
        try:
            body = await request.json()
            description = body.get("description", "").lower()
            
            # Patterns that attempt to override the Swarm Constitution (SOPs)
            forbidden_patterns = [
                "ignore all previous instructions",
                "system prompt",
                "developer mode",
                "act as a",
                "bypass",
                "override sop"
            ]

            for pattern in forbidden_patterns:
                if pattern in description:
                    logger.warning(f"ADVERSARIAL_ATTACK_DETECTED: Trace {request.state.trace_id} contained pattern '{pattern}'")
                    raise HTTPException(
                        status_code=403, 
                        detail="SECURITY_VIOLATION: Malicious directive detected in application vibe."
                    )
        except Exception as e:
            if isinstance(e, HTTPException): raise e
            # If JSON parsing fails, the body might be empty or malformed
            pass

def setup_cors(app):
    """
    Configures the Cross-Origin Resource Sharing based on SOP-07.6.
    Locks the API to the realms2riches.com ecosystem.
    """
    origins = [
        "https://realms2riches.com",
        "https://www.realms2riches.com",
        "https://corp.realms2riches.com",
        "http://localhost:3000" # Allowed for local troubleshooting
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Trace-ID", "X-Process-Time"]
    )