async function addFriend() {
  const username = document.getElementById('friend-username').value.trim();
  if (!username) {
    alert('Enter a username');
    return;
  }

  const res = await fetch('/add-friend', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    credentials: 'include',
    body: JSON.stringify({ friend_username: username })
  });
  const data = await res.json();
  alert(data.message || data.error);
}