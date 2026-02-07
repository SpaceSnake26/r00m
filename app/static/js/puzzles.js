// Base submission helper
async function solve(answer) {
    const errEl = document.getElementById('puzzle-error');
    errEl.textContent = "Verifying...";

    try {
        const res = await fetch(`/api/puzzle/${PUZZLE_ID}/solve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answer: answer })
        });
        const data = await res.json();

        if (data.ok) {
            // Optional: meaningful transition?
            // For now, direct redirect.
            window.location.href = "/room";
        } else {
            errEl.textContent = data.hint || "Zugriff verweigert.";
            // Update status bar attempts if needed, functionality not strictly required realtime but nice
            fetchStatus().then(updateStatusBar);
        }
    } catch (e) {
        errEl.textContent = "Verbindungsfehler.";
    }
}

function submitGeneric(inputId) {
    const val = document.getElementById(inputId).value;
    solve(val);
}

// Puzzle 1: Pattern
let p1Seq = [];
document.querySelectorAll('.p1-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const val = btn.dataset.val;
        if (!p1Seq.includes(val)) {
            p1Seq.push(val);
            document.getElementById('p1-input').value = p1Seq.join('-');
            btn.style.borderColor = "red";
        }
    });
});
function clearP1() {
    p1Seq = [];
    document.getElementById('p1-input').value = "";
    document.querySelectorAll('.p1-btn').forEach(b => b.style.borderColor = "var(--color-accent)");
}
function submitP1() {
    solve(document.getElementById('p1-input').value);
}

// Puzzle 3: Switches
let switchMoves = [];
let switchState = [false, false, false, false];

function toggleSwitch(idx) {
    // Record move
    switchMoves.push(idx);

    // Update local state visuals (Classic toggle self + neighbors? 
    // Wait, python implementation: "_toggle self, i-1, i+1".
    // We should match visual to logic.)
    const affected = [idx - 1, idx, idx + 1];
    affected.forEach(i => {
        if (i >= 0 && i < 4) {
            switchState[i] = !switchState[i];
            const el = document.getElementById(`sw-${i}`);
            if (switchState[i]) el.classList.add('switch-on');
            else el.classList.remove('switch-on');
        }
    });
}
function resetSwitches() {
    switchMoves = [];
    switchState = [false, false, false, false];
    for (let i = 0; i < 4; i++) {
        document.getElementById(`sw-${i}`).classList.remove('switch-on');
    }
}
function submitSwitches() {
    solve({ moves: switchMoves });
}

// Puzzle 4: Terminal
const termInput = document.getElementById('term-input');
if (termInput) {
    let currentDir = "~";
    const files = {
        "r00m": { "note.txt": "Sieh im Spind nach. Code: LIFT-ACCESS-0512" }
    };

    termInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const cmdLine = termInput.value.trim();
            termInput.value = "";
            log(`user@r00m:${currentDir}$ ${cmdLine}`);

            const parts = cmdLine.split(" ");
            const cmd = parts[0].toLowerCase();

            if (cmd === "ls") {
                if (currentDir === "~") log("r00m");
                else if (currentDir === "r00m") log("note.txt");
            } else if (cmd === "cd") {
                if (parts[1] === "r00m") currentDir = "r00m";
                else if (parts[1] === "..") currentDir = "~";
                else log(`cd: ${parts[1]}: No such directory`);
            } else if (cmd === "cat") {
                if (currentDir === "r00m" && parts[1] === "note.txt") {
                    log(files["r00m"]["note.txt"]);
                } else {
                    log("cat: file not found");
                }
            } else if (cmd === "unlock") {
                solve(parts[1]);
            } else if (cmd === "help") {
                log("Available commands: ls, cd, cat, unlock <TOKEN>");
            } else {
                log("Unknown command.");
            }

            // Auto scroll
            const out = document.getElementById('term-output');
            out.scrollTop = out.scrollHeight;
        }
    });

    function log(txt) {
        const div = document.createElement('div');
        div.textContent = txt;
        document.getElementById('term-output').appendChild(div);
    }
}

// Puzzle 5: Sudoku
function submitSudoku() {
    // Gather all inputs
    const inputs = document.querySelectorAll('.sudoku-cell'); // includes disabled ones
    // We need to reconstruct the grid.
    // DOM order is correct (0..15).
    let grid = [];
    inputs.forEach(inp => {
        grid.push(parseInt(inp.value) || 0);
    });
    solve(grid);
}

// Initial status check
fetchStatus().then(updateStatusBar);
