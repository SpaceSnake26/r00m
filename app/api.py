from fastapi import APIRouter, Request, Response, HTTPException
from pydantic import BaseModel
from typing import Optional, Any
from app.session import get_session, sign_session, check_rate_limit, record_attempt, COOKIE_NAME
from app.puzzles.base import get_puzzle, PUZZLE_REGISTRY
import qrcode
import io
import base64

router = APIRouter()

class SolveRequest(BaseModel):
    answer: Any

@router.get("/status")
def get_status(request: Request):
    session = get_session(request)
    return {
        "solved": session.get("solved", False),
        "attempts": session.get("attempts", 0),
        "cooldown_until": session.get("cooldown_until", 0)
    }

@router.post("/start")
def start_game(request: Request, response: Response):
    session = get_session(request)
    session["started"] = True
    # Reset abuse counters on fresh start? Maybe not to prevent spam refresh.
    # Keep attempts/cooldown persistent.
    token = sign_session(session)
    response.set_cookie(key=COOKIE_NAME, value=token, httponly=True, samesite='lax')
    return {"ok": True}

@router.post("/puzzle/{puzzle_id}/solve")
def solve_puzzle(puzzle_id: int, solve_req: SolveRequest, request: Request, response: Response):
    session = get_session(request)
    
    if not session.get("started"):
         raise HTTPException(status_code=403, detail="Session not started")

    
    # 1. Check Rate Limit
    allowed, msg = check_rate_limit(session)
    if not allowed:
        return {"ok": False, "message": msg, "cooldown": True}

    # 2. Get Puzzle
    puzzle = get_puzzle(puzzle_id)
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")

    # 3. Validate
    result = puzzle.validate(solve_req.answer)
    success = result.get("ok", False)

    # 4. Update Session
    session = record_attempt(session, success)
    if success:
        # lock this session to this puzzle? requirement says "once started, locked until solved or cooldown" 
        # but here we just mark solved.
        session["solved"] = True
    
    # Save session
    token = sign_session(session)
    response.set_cookie(key=COOKIE_NAME, value=token, httponly=True, samesite='lax')
    
    return result

@router.get("/qrcode")
def get_wifi_qrcode(request: Request):
    """
    Returns a base64 encoded PNG image data uri of the WiFi QR code.
    Protected: Only available if session.solved is True.
    """
    session = get_session(request)
    if not session.get("solved"):
         raise HTTPException(status_code=403, detail="Access denied")

    from app.config import config
    # Format: WIFI:T:WPA;S:sname;P:pass;;
    wifi_str = f"WIFI:T:WPA;S:{config.WIFI_SSID};P:{config.WIFI_PASSWORD};;"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(wifi_str)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return {"image_data": f"data:image/png;base64,{img_str}"}
