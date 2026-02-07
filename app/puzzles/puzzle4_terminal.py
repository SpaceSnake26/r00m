from app.puzzles.base import Puzzle, register_puzzle

class TerminalPuzzle(Puzzle):
    def validate(self, answer: str):
        # The user has to find the token in the 'fake' terminal.
        # The token is hidden in a file.
        # The solution submitted should be the token itself or the final command?
        # Requirement: "Backend validiert, dass am Ende unlock mit korrektem TOKEN ausgeführt wurde."
        # So we expect the "TOKEN" as answer.
        # Let's set the token.
        token = "LIFT-ACCESS-0512"
        
        clean = str(answer).strip().upper()
        if clean == token:
            return {"ok": True}
        return {"ok": False, "hint": "Finde den Token in note.txt und führe unlock <TOKEN> aus."}

register_puzzle(TerminalPuzzle(
    4, 
    "Mainframe", 
    "Hacke das Terminal. Finde den Unlock-Code."
))
