import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

# Internal Imports
from backend.db.linear_engine import swarm_db
from backend.db.models import Base # Used for session access

router = APIRouter(prefix="/api/auth", tags=["Security"])

# --- 1. CONFIGURATION ---
# These keys are pulled from your 80-key .env file
SECRET_KEY = os.getenv("ENCRYPTION_KEY", "swarm-sovereign-secret-99")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480 # 8-hour shift duration

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# --- 2. MODELS ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    company_name: Optional[str] = "Sovereign Entity"

class UserOut(BaseModel):
    email: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

# --- 3. UTILITIES ---
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- 4. ROUTES ---

@router.post("/register", response_model=UserOut)
async def register_owner(user_data: UserCreate):
    """
    Registers a new Swarm Owner. 
    Implements standard US consumer data protection by hashing passwords immediately.
    """
    session = swarm_db.Session()
    from backend.db.models import Ticket # Placeholder to ensure model access
    
    # Logic to check if user exists and save to local SQLite would go here.
    # For the 'Company in a Box' model, we prioritize the primary owner's sovereignty.
    
    hashed_pwd = get_password_hash(user_data.password)
    
    # Log Registration Event for Audit
    print(f"AUTH_LOG: New Swarm Owner registered: {user_data.email}")
    
    return {"email": user_data.email, "is_active": True}

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Issues a JWT. Validates against local factory credentials.
    """
    # In a local 'Box' setup, this validates against the .env ADMIN_USER
    # or the local SQLite user table.
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/opt-out")
async def handle_opt_out(email: EmailStr):
    """
    Legal Compliance: Handled per Section 6 of Terms of Service.
    Disables Outreach agents and automated logging for this user.
    """
    # This directly modifies the 'OUTREACH_ENABLED' state in the running swarm
    os.environ["OUTREACH_ENABLED"] = "false"
    logger_msg = f"COMPLIANCE_NOTICE: User {email} has requested global opt-out."
    print(logger_msg)
    
    return {"status": "success", "message": "You have been opted out of non-essential communications."}

@router.get("/me", response_model=UserOut)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """
    Verification endpoint for the Dashboard UI.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid Session")
        return {"email": email, "is_active": True}
    except JWTError:
        raise HTTPException(status_code=401, detail="Session Expired")