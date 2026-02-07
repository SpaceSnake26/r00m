from app.puzzles.base import Puzzle, register_puzzle
from typing import List

class SwitchPuzzle(Puzzle):
    def __init__(self, puzzle_id, name, desc):
        super().__init__(puzzle_id, name, desc)
        # 4 switches. Start: All OFF (0000). Target: All ON (1111).
        # Rules: Toggle i toggles i, i-1, i+1 (if exist).
        # We need a solution.
        # 0000 
        # Click 0 -> 1100
        # Click 1 -> 1010
        # Click 2 -> 0101
        # Click 3 -> 0011
        # Actually standard Lights Out is tricky. Let's do simple neighbor toggle.
        # Toggle i affects i and i+1? Or i-1, i, i+1?
        # Let's say we just simulate the moves provided by user.
        self.initial_state = [False, False, False, False]
        self.target_state = [True, True, True, True]

    def validate(self, answer: dict):
        # Expect answer to be list of indices clicked OR just the moves
        # Let's say answer is {"moves": [0, 2, 1...]}
        # Or simplistic: client sends the final state string? NO, that's insecure.
        # Better: Client sends the sequence of moves.
        if isinstance(answer, list):
            moves = answer
        elif isinstance(answer, dict):
            moves = answer.get("moves", [])
        else:
            return {"ok": False, "hint": "Invalid format"}
            
        state = list(self.initial_state)
        
        for move_idx in moves:
            try:
                idx = int(move_idx)
                if 0 <= idx < 4:
                    # Toggle logic: i and neighbors
                    # Let's do: Toggle Self and Right Neighbor (i, i+1) to be solvable simply?
                    # Or classic: i-1, i, i+1
                    self._toggle(state, idx)
            except:
                pass
        
        if state == self.target_state:
            return {"ok": True}
        return {"ok": False, "hint": "Alle Lichter müssen an sein."}

    def _toggle(self, state, idx):
        # Classic 1D lights out rule: toggle self and immediate neighbors
        for i in [idx - 1, idx, idx + 1]:
            if 0 <= i < len(state):
                state[i] = not state[i]

register_puzzle(SwitchPuzzle(
    3, 
    "Power Grid", 
    "Schalte alle 4 Generatoren ein."
))
