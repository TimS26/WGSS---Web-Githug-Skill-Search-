from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import uuid
import os
import requests

app = Flask(__name__)

# Словарь иконок для навыков
tool_icons = {
    "Python": "🐍",
    "HTML": "🌐",
    "Flask": "🔥",
    "CSS": "🎨",
    "JavaScript": "✨",
    "SQL": "🗄️",
    "Django": "🦄",
    "C++": "💻",
    "C#": "🔷",
    "Java": "☕",
    "React": "⚛️",
    "Vue": "🟩",
    "Figma": "🎨",
    "Git": "🔧",
    "Linux": "🐧",
    "Docker": "🐳",
    "FastAPI": "⚡",
    "TypeScript": "🔵",
    "Node.js": "🌲",
    "Go": "🐹",
    "Kotlin": "🅺",
    "Swift": "🦅",
    "PHP": "🐘",
    "Ruby": "💎",
    "Rust": "🦀",
    "Other": "🔹"
}

def init_db():
    conn = sqlite3.connect('portfolios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE,
            name TEXT,
            bio TEXT,
            github TEXT,
            telegram TEXT,
            avatar TEXT,
            skills TEXT
        )
    ''')
    conn.commit()
    conn.close()

def test_user():
    conn = sqlite3.connect('portfolios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM portfolio WHERE uuid = ?", ('123',))
    if cursor.fetchone() is None:
        cursor.execute('''
            INSERT INTO portfolio (uuid, name, bio, github, telegram, avatar, skills)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            '123',
            'Ivan Ivanov',
            'Frontend-developer',
            'https://github.com/example',
            'https://t.me/example',
            'placeholder.png',
            'Python, HTML, CSS'
        ))
        conn.commit()
    conn.close()

def get_theme():
    theme = request.cookies.get('theme')
    if theme not in ['dark', 'light']:
        theme = 'dark'
    return theme

@app.route('/set_theme/<theme>')
def set_theme(theme):
    if theme not in ['dark', 'light']:
        theme = 'dark'
    resp = make_response(redirect(request.referrer or url_for('index')))
    resp.set_cookie('theme', theme, max_age=60*60*24*365)
    return resp

def get_github_repos(username):
    if not username:
        return []
    if username.startswith('http'):
        username = username.rstrip('/').split('/')[-1]
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

init_db()
test_user()

@app.route('/')
def index():
    filter_skill = request.args.get('skill')
    filter_skill = filter_skill.lower() if filter_skill else None

    conn = sqlite3.connect('portfolios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM portfolio")
    raw_data = cursor.fetchall()
    conn.close()

    portfolios = []
    for row in raw_data:
        skills = [s.strip() for s in (row[7] or '').split(',') if s.strip()]
        skills_lower = [s.lower() for s in skills]
        if not filter_skill or filter_skill in skills_lower:
            portfolios.append({
                'uuid': row[1],
                'name': row[2],
                'bio': row[3],
                'github': row[4],
                'telegram': row[5],
                'avatar': row[6],
                'skills': skills
            })
    theme = get_theme()
    return render_template(
        "all_portfolios.html",
        portfolios=portfolios,
        tool_icons=tool_icons,
        current_skill=filter_skill or "",
        theme=theme
    )

@app.route('/create', methods=['GET', 'POST'])
def create_portfolio():
    if request.method == 'POST':
        name = request.form['name']
        bio = request.form['bio']
        github = request.form['github']
        telegram = request.form['telegram']
        skills = request.form['skills']
        user_uuid = str(uuid.uuid4())

        avatar_file = request.files.get('avatar')
        if avatar_file and avatar_file.filename:
            avatar_filename = f"{user_uuid}_{avatar_file.filename}"
            avatar_path = os.path.join('static', avatar_filename)
            avatar_file.save(avatar_path)
        else:
            avatar_filename = 'placeholder.png'

        conn = sqlite3.connect('portfolios.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO portfolio (uuid, name, bio, github, telegram, avatar, skills)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_uuid, name, bio, github, telegram, avatar_filename, skills))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    theme = get_theme()
    return render_template('create_portfolio.html', theme=theme)

@app.route('/portfolio/<user_uuid>')
def portfolio_detail(user_uuid):
    conn = sqlite3.connect('portfolios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM portfolio WHERE uuid = ?", (user_uuid,))
    user = cursor.fetchone()
    conn.close()
    if user:
        github_username = user[4]
        repos = get_github_repos(github_username)
        theme = get_theme()
        return render_template('portfolio_detail.html', user=user, repos=repos, theme=theme)
    else:
        return "Портфолио не найдено", 404

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # регистрация пользователя (логика по желанию)
        return redirect(url_for('index'))
    theme = get_theme()
    return render_template('register.html', theme=theme)

if __name__ == '__main__':
    app.run(debug=True)