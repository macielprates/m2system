// M2 Sistema - JavaScript Principal v3

// Relogio na statusbar
function updateClock() {
    const el = document.getElementById('clock');
    if (el) {
        const now = new Date();
        el.textContent = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }
}
updateClock();
setInterval(updateClock, 1000);

// Auto-dismiss flash messages
document.querySelectorAll('.flash-msg').forEach(msg => {
    setTimeout(() => {
        msg.style.opacity = '0';
        msg.style.transform = 'translateY(-10px)';
        msg.style.transition = 'all 0.3s';
        setTimeout(() => msg.remove(), 300);
    }, 5000);
});

// Nav dropdown toggle (para mobile)
function toggleNavDropdown(btn) {
    const menu = btn.nextElementSibling;
    if (menu) menu.classList.toggle('show');
}
