# leeterz
leetcode x stompers webapp

# resources compilation (chronological diary)
 work session 1:
- learning how to use flask. created a venv. 
starter flask code:
https://www.geeksforgeeks.org/python/flask-creating-first-simple-application/
- learning how to use beautifulsoup to scrape webdata from leetcode:
https://www.geeksforgeeks.org/python/implementing-web-scraping-python-beautiful-soup/
- found out web scraping is against leetcode's tos (oops!). instead, i plan to make a small browser extension that reads what the user sees and sends the data to the backend.
- i read up a bit on DOM manipulation (odin project), since i treat the lc webpage as a DOM. then, i read about how browser extensions work (manifest.json, content.js script, fetch())
https://www.youtube.com/watch?v=y17RuWkWdn8&ab_channel=WebDevSimplified 
https://developer.chrome.com/docs/extensions/reference/manifest#inject-a-content-script
https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts#functionality
https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
- created a working chrome extension reads the leetcode submissions page and sends data to flask backend
 
summary:
right now, i can navigate to my own lc submissions and upon the submissions page loading, the extension automatically runs to collect the leetcodes i did today.

next steps:
- multiple users can log in, add eachother as friends, and see eachother on the leaderboard

work session 2:
- working on log in and authentication. chatgpt suggested i use "Flask’s session management and Werkzeug’s password hashing" for minimal dependencies. i chose to go this route since i wanted this to be a simple project
https://flask.palletsprojects.com/en/stable/quickstart/#sessions
the repo i referenced for flask logins: 
https://github.com/partner0307/flask-login-system?
- dumb mistakes: did an oopsie by not having venv on, had an enter key on postman causing a 405 error

rundown:
in powershell
- venv\Scripts\activate
- $env:FLASK_APP = "app.py"
- flask run 

got registration working

work session 3
https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security

goals:
- multiple user login:
1. profile page
2. add friends button (to search for friends via username)

- create leaderboard


how to use
- python init_db.p 
creates database.db
- python app.py
starts server
- load extension
- login in localhost
sets session cookie for browser
- open lc submissions page
matches pattern in manifest.json will run content.js. sends data to api/update-today
 - view results in leaderboard

another oops: i used the wrong interpreter haha, not the venv

my goal:
- get the lc submissions working with the leaderboard