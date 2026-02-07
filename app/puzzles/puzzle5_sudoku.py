from app.puzzles.base import Puzzle, register_puzzle
import math

class SudokuPuzzle(Puzzle):
    def validate(self, answer: list):
        # Expect 4x4 list of lists or flat list
        # Valid 4x4 sudokus use 1-4.
        
        # Flatten if needed
        if not answer:
             return {"ok": False}
             
        grid = []
        if isinstance(answer[0], list):
            for row in answer:
                grid.extend(row)
        else:
            grid = answer
            
        if len(grid) != 16:
            return {"ok": False, "hint": "Muss 4x4 Grid sein."}
            
        # Try convert to int
        try:
            grid = [int(x) for x in grid]
        except:
             return {"ok": False, "hint": "Nur Zahlen 1-4."}

        # Validate rows, cols, 2x2 blocks
        if self._check_valid(grid):
            return {"ok": True}
            
        return {"ok": False, "hint": "Jede Zeile, Spalte und 2x2 Block muss 1-4 einmal enthalten."}

    def _check_valid(self, grid):
        # Check rows
        for r in range(4):
            row = grid[r*4 : (r+1)*4]
            if len(set(row)) != 4 or not all(1 <= x <= 4 for x in row):
                return False
        
        # Check cols
        for c in range(4):
            col = [grid[r*4 + c] for r in range(4)]
            if len(set(col)) != 4:
                return False
                
        # Check 2x2 blocks
        # 0,1, 4,5 | 2,3, 6,7
        # 8,9, 12,13 | 10,11, 14,15
        blocks = [
            [0,1,4,5], [2,3,6,7],
            [8,9,12,13], [10,11,14,15]
        ]
        for b in blocks:
            vals = [grid[i] for i in b]
            if len(set(vals)) != 4:
                return False
                
        return True

register_puzzle(SudokuPuzzle(
    5, 
    "Data Matrix", 
    "Vervollständige das 4x4 Raster (Zahlen 1-4)."
))
