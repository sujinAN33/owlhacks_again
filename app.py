from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'change-me-in-production'

# 업로드 설정
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# DB 초기화
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            vaccine TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 메인 페이지: 게시글 목록
@app.route("/")
def index():
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = c.fetchall()
    return render_template("index.html", posts=posts)

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/donation")
def donation():
    return render_template("donation.html")


# 글쓰기 페이지
@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        age = request.form.get("age")
        age = int(age) if age else None
        gender = request.form.get("gender")
        vaccine = request.form.get("vaccine")
        file = request.files.get("photo")

        if not title or not content or not file:
            flash("모든 필드를 채워주세요.")
            return redirect(url_for('write'))

        filename_orig = secure_filename(file.filename)
        ext = filename_orig.rsplit('.', 1)[1].lower() if '.' in filename_orig else ''
        if ext not in ALLOWED_EXTENSIONS:
            flash("허용되지 않는 파일 형식입니다.")
            return redirect(url_for('write'))

        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO posts (title, filename, content, age, gender, vaccine) VALUES (?, ?, ?, ?, ?, ?)",
                (title, filename, content, age, gender, vaccine)
            )
            conn.commit()

        return redirect(url_for('index'))

    return render_template("write.html")

if __name__ == "__main__":
    app.run(debug=True)
