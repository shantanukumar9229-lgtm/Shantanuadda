import sqlite3
import urllib.request
import urllib.parse
import json
import os
from flask import Flask, render_template_string

app = Flask(__name__)
API_KEY = "a8e06b05"

def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS movies 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT, poster_url TEXT, stream_url TEXT)''')
    cursor.execute("SELECT COUNT(*) FROM movies")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO movies (title, category, poster_url, stream_url) VALUES (?, ?, ?, ?)",
                       ("Pushpa 2", "indian_release", "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0", "https://www.w3schools.com/html/mov_bbb.mp4"))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, poster_url, stream_url FROM movies")
    movies = cursor.fetchall()
    conn.close()
    
    # Yahan wahi purana HTML logic daalna hai (generate_html function wala)
    # Main abhi shortcut mein samjha raha hoon
    return "<h1>Shantanu Adda Live!</h1>" # Yahan aap apna HTML template return karoge

init_db()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
