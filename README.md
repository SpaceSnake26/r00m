# r00m - The Lift

A cinematic captive portal experience where players enter a mysterious freight elevator, solve a security protocol, and gain access to the "Mancave" (WiFi credentials).

## Gameplay Flow
1.  **Start**: Authentischer "Lift Door" Screen. Klick auf "Eintreten" öffnet die Doppeltür.
2.  **Lift**: Im Inneren (Holzpaneele & Glas-Panel) wählt der Spieler ein Rätsel.
3.  **Puzzle**: Löse 1 von 5 Aufgaben (Pattern, Cipher, Switches, Terminal, Sudoku) direkt im Panel.
4.  **Success**: Nach Lösung öffnet sich die Tür zum Zielraum -> WiFi Credentials & QR Code.

## Tech Stack
-   **Backend**: Python FastAPI (Secure Sessions, Validation)
-   **Frontend**: HTML5/CSS3 (3D Transforms, Glassmorphism, Animations)
-   **No DB**: In-memory session logic (Cookie based).

## Setup
1.  Installieren: `pip install -r requirements.txt`
2.  Konfigurieren: `.env` (SSID/PASS)
3.  Starten: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Deployment
-   Docker: `docker-compose up -d --build`
