import time
from itsdangerous import URLSafeSerializer, BadSignature
from app.config import config

# Initialize serializer for signed cookies
serializer = URLSafeSerializer(config.SECRET_KEY)

COOKIE_NAME = "r00m_session"

def get_session(request):
    """
    Retrieve and decode session data from signed cookie.
    Returns default dict if missing or invalid.
    """
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return _new_session()
    
    try:
        data = serializer.loads(token)
        return data
    except BadSignature:
        return _new_session()

def sign_session(data):
    """Sign the session dictionary to create a token."""
    return serializer.dumps(data)

def _new_session():
    return {
        "solved": False,
        "attempts": 0,
        "puzzle_id": None,
        "cooldown_until": 0,
        "start_time": time.time()
    }

def check_rate_limit(session):
    """
    Check if session is currently in cooldown.
    Returns (allowed: bool, message: str)
    """
    now = time.time()
    if session.get("cooldown_until") and now < session["cooldown_until"]:
        remaining = int(session["cooldown_until"] - now)
        return False, f"Zu viele Versuche. Warte {remaining // 60}m {remaining % 60}s."
    return True, ""

def record_attempt(session, success: bool):
    """
    Update session stats for an attempt.
    Returns updated session object (dict) - NOTE: caller must save it.
    """
    if success:
        session["solved"] = True
        session["attempts"] = 0 # Optional reset
    else:
        session["attempts"] = session.get("attempts", 0) + 1
        if session["attempts"] >= config.MAX_ATTEMPTS:
            session["cooldown_until"] = time.time() + config.COOLDOWN_SECONDS
            # Reset attempts after triggering cooldown so they have fresh start after wait? 
            # Or keep them high? Let's reset attempts but keep cooldown active.
            # Logic: If cooldown_until > now, they are blocked. Once time passes, they are free.
            session["attempts"] = 0 
            
    return session
