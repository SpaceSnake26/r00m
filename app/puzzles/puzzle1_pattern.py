from app.puzzles.base import Puzzle, register_puzzle

class PatternPuzzle(Puzzle):
    def validate(self, answer: str):
        # Expected: A1-B2-C3-D4-E5 or A1B2C3D4E5 etc.
        # Normalize: remove dashes, spaces, uppercase
        clean = str(answer).upper().replace("-", "").replace(" ", "").replace(">", "")
        target = "A1B2C3D4E5"
        
        if clean == target:
            return {"ok": True}
        return {"ok": False, "hint": "Der Lift bewegt sich von oben links nach unten rechts."}

register_puzzle(PatternPuzzle(
    1, 
    "Pattern Lock", 
    "Zeichne das korrekte Muster, um den Lift zu aktivieren."
))
