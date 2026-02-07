document.addEventListener('DOMContentLoaded', () => {
    const display = document.getElementById('floor-display');
    const floors = ['5', '4', '3', '2', '1', 'B1', 'B2', 'r00m'];
    let idx = 0;

    // Total time 12s. We have ~8 steps? 
    // Or just count down numbers.
    // 12000ms.
    // Step interval = 12000 / floors.length
    const intervalTime = 12000 / floors.length;

    const interval = setInterval(() => {
        idx++;
        if (idx < floors.length) {
            display.textContent = floors[idx];
            // Play optional click sound here if allowed
        } else {
            clearInterval(interval);
            // Complete
            setTimeout(() => {
                window.location.href = '/room';
            }, 500);
        }
    }, intervalTime);
});
