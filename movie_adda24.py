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
            title TEXT, category TEXT, poster_url TEXT, stream_url TEXT)''')
    cursor.execute("SELECT COUNT(*) FROM movies")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO movies (title, category, poster_url, stream_url) VALUES (?, ?, ?, ?)",
                       ("Pushpa 2: The Rule", "indian_release", "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0", "https://www.w3schools.com/html/mov_bbb.mp4"))
    conn.commit()
    conn.close()

def generate_html():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, poster_url, stream_url FROM movies")
    movies = cursor.fetchall()
    conn.close()

    movie_cards = ""
    for m in movies:
        movie_cards += f'''
        <div style="background:#222; padding:10px; border-radius:10px; width:150px; cursor:pointer;" 
             onclick="document.getElementById('vid').src='{m[2]}'; document.getElementById('player').style.display='block';">
            <img src="{m[1]}" style="width:100%; border-radius:5px;">
            <p style="font-size:12px; margin-top:10px;">{m[0]}</p>
        </div>'''
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Shantanu Adda</title></head>
    <body style="background:#111; color:white; font-family:sans-serif; text-align:center;">
        <h1 style="color:#E50914;">SHANTANU ADDA</h1>
        <div id="player" style="display:none; margin:20px;">
            <video id="vid" controls style="width:80%; border:2px solid #E50914;"></video>
        </div>
        <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:20px; padding:20px;">
            {movie_cards}
        </div>
    </body>
    </html>
    """

@app.route('/')
def home():
    return generate_html()

init_db()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
