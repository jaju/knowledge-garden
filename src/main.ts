// Theme toggle: toggles .dark on <html> and persists preference
const html = document.documentElement;

function applyStoredTheme() {
  try {
    const v = localStorage.getItem('theme');
    if (v === 'dark') html.classList.add('dark');
    if (v === 'light') html.classList.remove('dark');
  } catch { }
}

document.addEventListener('DOMContentLoaded', () => {
  applyStoredTheme();
  const btn = document.querySelector('a[aria-label="Toggle theme"]');
  if (!btn) return;
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    html.classList.toggle('dark');
    try {
      localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
    } catch { }
  });
});
