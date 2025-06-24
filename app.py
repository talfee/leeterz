from flask import Flask, request, jsonify, session, render_template, redirect
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import json
import sqlite3
from db import get_conn


app = Flask(__name__)
# CORS(app)  
CORS(app, supports_credentials=True)
app.secret_key = 'replace_me'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    print("PRINT THIS IF REGISTER IS CALLED")
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing data'}), 400
    hashed = generate_password_hash(password)
    with get_conn() as conn:
        try:
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed)
            )
            conn.commit()
            return jsonify({'message': 'Registered'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username taken'}), 400
        
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing data'}), 400
    with get_conn() as conn:
        cur = conn.execute(
            'SELECT id, password FROM users WHERE username=?',
            (username,)
        )
        row = cur.fetchone()
    if row and check_password_hash(row['password'], password):
        session['user_id'] = row['id']
        return jsonify({'message': 'Logged in'})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'})

@app.route('/add-friend', methods=['POST'])
def add_friend():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json() or {}
    friend_username = data.get('friend_username')
    if not friend_username:
        return jsonify({'error': 'Missing data'}), 400
    with get_conn() as conn:
        cur = conn.execute('SELECT id FROM users WHERE username=?', (friend_username,))
        row = cur.fetchone()
        if not row:
            return jsonify({'error': 'User not found'}), 404
        friend_id = row['id']
        try:
            conn.execute(
                'INSERT INTO friends (user_id, friend_id) VALUES (?, ?)',
                (session['user_id'], friend_id)
            )
            conn.commit()
            return jsonify({'message': 'Friend added'})
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Already friends'}), 400

@app.route('/api/update-today', methods=['POST'])
def update_today():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json() or {}
    count = data.get('count', 0)
    titles = json.dumps(data.get('titles', []))
    today = date.today().isoformat()
    with get_conn() as conn:
        conn.execute(
            'INSERT OR REPLACE INTO stats (user_id, date, count, titles) VALUES (?, ?, ?, ?)',
            (session['user_id'], today, count, titles)
        )
        conn.commit()
    return jsonify({'status': 'ok'})

@app.route('/api/leaderboard')
def leaderboard_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    today = date.today().isoformat()
    with get_conn() as conn:
        friends = [row['friend_id'] for row in conn.execute(
            'SELECT friend_id FROM friends WHERE user_id=?',
            (session['user_id'],)
        )]
        ids = friends + [session['user_id']]
        placeholders = ','.join('?' for _ in ids)
        query = f'''
            SELECT u.username, IFNULL(s.count, 0) as count
            FROM users u
            LEFT JOIN stats s ON u.id = s.user_id AND s.date = ?
            WHERE u.id IN ({placeholders})
            ORDER BY count DESC
        '''
        cur = conn.execute(query, [today] + ids)
        rows = cur.fetchall()
    board = [{'username': r['username'], 'count': r['count']} for r in rows]
    return jsonify(board)

@app.route('/leaderboard')
def leaderboard_page():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('leaderboard.html')

@app.route('/profile')
def profile_page():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('profile.html')


#troubleshoot
@app.route('/routes')
def show_routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])

@app.route('/whoami')
def whoami():
    return jsonify({'user_id': session.get('user_id')})


def index():
    return jsonify({'status': 'running'})


if __name__ == '__main__':
    print("APP.PY RUNNING")
    print(app.url_map)
    app.run(debug=True)
