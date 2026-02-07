from app.puzzles.base import Puzzle, register_puzzle

class CipherPuzzle(Puzzle):
    def __init__(self, puzzle_id, name, desc):
        super().__init__(puzzle_id, name, desc)
        self.clear_text = "OPEN THE ROOM"
        self.shift = 12
        self.cipher_text = self._encrypt(self.clear_text, self.shift)
    
    def _encrypt(self, text, shift):
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                # (char - base + shift) % 26 + base
                result.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                result.append(char)
        return "".join(result)

    def validate(self, answer: str):
        clean = str(answer).upper().strip()
        if clean == self.clear_text:
            return {"ok": True}
        return {"ok": False, "hint": f"Verschlüsselt: {self.cipher_text}. Key: Zwölf."}

register_puzzle(CipherPuzzle(
    2, 
    "Shift Protocol", 
    "Entschlüssele den Zugangscode. Shift 12."
))
