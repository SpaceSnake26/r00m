import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_puzzles():
    s = requests.Session()
    # 1. Start Session
    res = s.post(f"{BASE_URL}/api/start")
    print(f"Start: {res.status_code}")
    assert res.status_code == 200

    # 2. Test Puzzle 3 (Dict payload)
    # Payload: {"answer": {"moves": [0, 3]}}
    # Note: Correct answer for [0, 0, 0, 0] -> [1, 1, 1, 1] is [0, 3] based on my earlier analysis.
    # 0 toggles [1, 1, 0, 0]. 3 toggles [0, 0, 1, 1]. Sum = [1, 1, 1, 1].
    p3_payload = {"answer": {"moves": [0, 3]}}
    res = s.post(f"{BASE_URL}/api/puzzle/3/solve", json=p3_payload)
    print(f"Puzzle 3 (Dict): {res.status_code} - {res.json()}")
    assert res.status_code == 200
    assert res.json().get("ok") == True

    # 3. Test Puzzle 5 (List payload)
    # Logic: 4x4 grid. 
    # 1 2 3 4
    # 3 4 1 2
    # 2 1 4 3
    # 4 3 2 1
    # Let's construct a valid grid.
    grid = [
        1, 2, 3, 4,
        3, 4, 1, 2,
        2, 1, 4, 3,
        4, 3, 2, 1
    ]
    p5_payload = {"answer": grid}
    res = s.post(f"{BASE_URL}/api/puzzle/5/solve", json=p5_payload)
    print(f"Puzzle 5 (List): {res.status_code} - {res.json()}")
    assert res.status_code == 200
    assert res.json().get("ok") == True

if __name__ == "__main__":
    try:
        test_puzzles()
        print("ALL TESTS PASSED")
    except Exception as e:
        print(f"TEST FAILED: {e}")
