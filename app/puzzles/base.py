from typing import Dict, Any, Optional

class Puzzle:
    def __init__(self, puzzle_id: int, name: str, description: str):
        self.id = puzzle_id
        self.name = name
        self.description = description
    
    def validate(self, answer: Any) -> Dict[str, Any]:
        """
        Validates the answer.
        Returns dict with keys:
          - ok: bool
          - message: str (optional success/failure message)
          - hint: str (optional hint if wrong)
        """
        raise NotImplementedError("Subclasses must implement validate")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

# Registry to hold all puzzles
PUZZLE_REGISTRY = {}

def register_puzzle(puzzle: Puzzle):
    PUZZLE_REGISTRY[puzzle.id] = puzzle

def get_puzzle(puzzle_id: int) -> Optional[Puzzle]:
    return PUZZLE_REGISTRY.get(puzzle_id)
