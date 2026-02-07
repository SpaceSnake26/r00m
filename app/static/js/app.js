// Common helpers
async function fetchStatus() {
    try {
        const res = await fetch('/api/status');
        return await res.json();
    } catch (e) {
        console.error(e);
        return null;
    }
}

function updateStatusBar(status) {
    const el = document.getElementById('status-text');
    if (el && status) {
        if (status.cooldown_until > Date.now() / 1000) {
            el.textContent = "SYSTEM LOCKDOWN";
            el.style.color = "red";
        } else {
            el.textContent = `ATTEMPTS: ${status.attempts || 0}`;
            el.style.color = "#666";
        }
    }
}
