from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.session import get_session, sign_session, COOKIE_NAME
from app.api import get_status
from app.puzzles.base import PUZZLE_REGISTRY

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Start Screen: Outside the Lift Doors."""
    session = get_session(request)
    if session.get("solved"):
        return RedirectResponse(url="/room")
    # New concept: No 'intro' page, just 'start' which is the outer doors.
    # If they already started but not solved, maybe redirect to lift?
    # Requirement: "Wenn nicht gestartet: umleiten auf /" (handled here by serving start)
    # "Wenn im Lift (started)...": Let's optionally redirect to /lift if they clicked enter before.
    if session.get("started"):
        return RedirectResponse(url="/lift")
        
    return templates.TemplateResponse("start.html", {"request": request})

@router.get("/lift", response_class=HTMLResponse)
def lift_interior(request: Request):
    """The Lift Interior: Puzzle Hub."""
    session = get_session(request)
    
    # 1. Solved -> Room
    if session.get("solved"):
        return RedirectResponse(url="/room")
        
    # 2. Not started -> Start (Security/Flow check)
    if not session.get("started"):
        return RedirectResponse(url="/")
        
    return templates.TemplateResponse("lift.html", {
        "request": request, 
        "puzzles": PUZZLE_REGISTRY.values()
    })

@router.get("/room", response_class=HTMLResponse)
def room_view(request: Request):
    """Success Room: WiFi Credentials."""
    session = get_session(request)
    
    # Security: Access only if solved
    if not session.get("solved"):
        return RedirectResponse(url="/lift") if session.get("started") else RedirectResponse(url="/")
        
    from app.config import config
    return templates.TemplateResponse("room.html", {
        "request": request,
        "ssid": config.WIFI_SSID,
        "password": config.WIFI_PASSWORD
    })

@router.get("/puzzles/{puzzle_id}", response_class=HTMLResponse)
def puzzle_view(request: Request, puzzle_id: int):
    """Specific Puzzle View (Lift Panel)."""
    session = get_session(request)
    if not session.get("started"):
        return RedirectResponse(url="/")
        
    puzzle = PUZZLE_REGISTRY.get(puzzle_id)
    if not puzzle:
         raise HTTPException(status_code=404, detail="Puzzle not found")
         
    return templates.TemplateResponse("puzzle_detail.html", {
        "request": request,
        "puzzle": puzzle
    })

@router.get("/reset")

def reset_session(request: Request):
    """Reset the session (debug/demo purpose)."""
    response = RedirectResponse(url="/")
    response.delete_cookie(key=COOKIE_NAME)
    return response



