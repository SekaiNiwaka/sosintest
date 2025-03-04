from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# SQLiteデータベースのセットアップ
DATABASE = 'text_data.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# テキストを保存する関数
def save_text(content):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO texts (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()

# 最後のテキストを取得する関数
def load_text():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT content FROM texts ORDER BY id DESC LIMIT 1')
    result = c.fetchone()
    conn.close()
    return result[0] if result else "No data available"

# サーバー起動時にDB初期化
init_db()

# ホームページのルート
@app.route('/')
def index():
    # 最新のテキストを取得して表示
    latest_text = load_text()
    return render_template('index.html', latest_text=latest_text)

# テキストを送信するためのルート
@app.route('/submit', methods=['POST'])
def submit():
    # フォームから送信されたテキストを取得
    text_content = request.form['text_content']
    save_text(text_content)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
