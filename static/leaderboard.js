async function loadLeaderboard() {
  const res = await fetch('/api/leaderboard', {
    credentials: 'include',
  });

  if (!res.ok) {
    alert('Not authorized or failed to load leaderboard');
    window.location.href = '/index.html';
    return;
  }

  const data = await res.json();
  const list = document.getElementById('leaderboardList');
  list.innerHTML = '';

  data.forEach(entry => {
    const li = document.createElement('li');
    li.textContent = `${entry.username}: ${entry.count} problems`;
    list.appendChild(li);
  });
}

document.addEventListener('DOMContentLoaded', loadLeaderboard);
