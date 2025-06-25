console.log("content.js loaded");

let username = localStorage.getItem("leetcode_username");
if (!username) {
  username = prompt("Enter your Leetcode username:");
  localStorage.setItem("leetcode_username", username);
}


function isToday(text) {
  return !text.includes("day") && !text.includes("week");
}

function getTodayAccepted() {
  const rows = document.querySelectorAll("tbody tr");
  const titlesSet = new Set();

  rows.forEach(row => {
    const timeCell = row.querySelector("td:nth-child(1)");
    const titleCell = row.querySelector("td:nth-child(2)");
    const statusCell = row.querySelector("td:nth-child(3)");

    const status = statusCell?.innerText?.trim().toLowerCase();
    const time = timeCell?.innerText?.trim().toLowerCase();

    if (status === "accepted" && isToday(time)) {
      titlesSet.add(titleCell.innerText.trim());
    }
  });

  return Array.from(titlesSet);
}

function sendToBackend(data) {
  fetch("http://localhost:5000/api/update-today", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify(data)
  })
    .then(res => res.json())
    .then(res => console.log(res))
    .catch(err => console.error(err));
}

setTimeout(() => {
  const titles = getTodayAccepted();
  const payload = { count: titles.length, titles };
  console.log(payload);
  sendToBackend(payload);
}, 2000);
