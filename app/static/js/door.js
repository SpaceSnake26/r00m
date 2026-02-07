async function openLift() {
    // 1. Notify Backend we are starting
    try {
        const res = await fetch('/api/start', { method: 'POST' });
        if (!res.ok) {
            console.error("Failed to start session");
            return;
        }
    } catch (e) { console.error(e); }

    // 2. Animate Doors Open
    const wrapper = document.getElementById('door-wrapper');
    wrapper.classList.add('doors-open');

    // 3. Wait for animation then redirect
    setTimeout(() => {
        window.location.href = "/lift";
    }, 1200); // 1.2s match CSS transition
}

// Logic for Lift Interior (if needed shared)
