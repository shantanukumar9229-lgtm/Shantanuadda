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
    cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            poster_url TEXT NOT NULL,
            stream_url TEXT NOT NULL
        )''')
    cursor.execute("SELECT COUNT(*) FROM movies")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO movies (title, category, poster_url, stream_url) VALUES (?, ?, ?, ?)",
                       ("Pushpa 2: The Rule", "indian_release", "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0", "https://www.w3schools.com/html/mov_bbb.mp4"))
    conn.commit()
    conn.close()

def generate_html():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, poster_url, stream_url FROM movies WHERE category='indian_release'")
    indian_releases = cursor.fetchall()
    conn.close()

    indian_html = "".join([f'<div class="movie-card"><img src="{m[1]}" style="width:100%"><p>{m[0]}</p></div>' for m in indian_releases])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Shantanu Adda</title></head>
    <body style="background:#111; color:white; text-align:center;">
        <h1>SHANTANU ADDA</h1>
        <div style="display:flex; justify-content:center; gap:20px;">{indian_html}</div>
    </body>
    </html>
    """

@app.route('/')
def home():
    return generate_html()

# Initialize Database
init_db()

if __name__ == "__main__":
    app.run()
