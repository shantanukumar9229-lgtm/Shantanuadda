import http.server
import socketserver
import webbrowser
import threading
import time
import sqlite3
import urllib.request
import json

PORT = 8000
API_KEY = "a8e06b05"  # Aapki OMDb API Key

# 💾 DATABASE & OMDb INTEGRATION
def add_movie_via_api(title, category, stream_url):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    try:
        formatted_title = urllib.parse.quote(title)
        api_url = f"http://www.omdbapi.com/?t={formatted_title}&apikey={API_KEY}"
        
        response = urllib.request.urlopen(api_url)
        data = json.loads(response.read().decode())
        
        if data.get("Response") == "True":
            poster_url = data.get("Poster", "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=400")
            real_title = data.get("Title", title)
        else:
            poster_url = "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=400"
            real_title = title
            
    except Exception as e:
        print(f"Error fetching from API: {e}")
        poster_url = "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=400"
        real_title = title

    cursor.execute("INSERT INTO movies (title, category, poster_url, stream_url) VALUES (?, ?, ?, ?)",
                   (real_title, category, poster_url, stream_url))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            poster_url TEXT NOT NULL,
            stream_url TEXT NOT NULL
        )
    ''')
    conn.close()
    
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM movies")
    if cursor.fetchone()[0] == 0:
        conn.close()
        add_movie_via_api("Pushpa 2: The Rule", "indian_release", "https://www.w3schools.com/html/mov_bbb.mp4")
        add_movie_via_api("Singham Again", "indian_release", "https://www.w3schools.com/html/mov_bbb.mp4")
        add_movie_via_api("Kalki 2898 AD", "indian_release", "https://www.w3schools.com/html/mov_bbb.mp4")
        add_movie_via_api("Avatar: The Way of Water", "hollywood", "https://www.w3schools.com/html/mov_bbb.mp4")
        add_movie_via_api("Guardians of the Galaxy Vol. 2", "hollywood", "https://www.w3schools.com/html/mov_bbb.mp4")
    else:
        conn.close()

def generate_html():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT title, poster_url, stream_url FROM movies WHERE category='indian_release' ORDER BY id DESC")
    indian_releases = cursor.fetchall()
    
    cursor.execute("SELECT title, poster_url, stream_url FROM movies WHERE category='hollywood' ORDER BY id DESC")
    hollywood_movies = cursor.fetchall()
    conn.close()

    indian_html = ""
    for movie in indian_releases:
        title, poster, stream = movie[0], movie[1], movie[2]
        indian_html += f"""
        <div class="movie-card" onclick="openModal('{title}', '{stream}')">
            <img class="movie-img" src="{poster}" alt="{title}">
            <div class="card-overlay">
                <div class="movie-title">{title}</div>
                <div class="watch-badge">NEW INDIAN</div>
            </div>
        </div>
        """

    hollywood_html = ""
    for movie in hollywood_movies:
        title, poster, stream = movie[0], movie[1], movie[2]
        hollywood_html += f"""
        <div class="movie-card" onclick="openModal('{title}', '{stream}')">
            <img class="movie-img" src="{poster}" alt="{title}">
            <div class="card-overlay">
                <div class="movie-title">{title}</div>
                <div class="watch-badge">HINDI DUBBED</div>
            </div>
        </div>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shantanu Adda - Premium Free Streams</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ background-color: #111; color: white; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; overflow-x: hidden; }}
            
            /* Navbar me Shantanu Bhai ka branding */
            .navbar {{ display: flex; justify-content: space-between; align-items: center; padding: 15px 4%; position: sticky; top: 0; z-index: 100; background-color: #111; border-bottom: 1px solid #222; }}
            .logo {{ color: #E50914; font-size: 26px; font-weight: bold; letter-spacing: 1px; font-family: 'Impact', sans-serif; }}
            .owner-badge {{ font-size: 11px; background: #222; color: #aaa; padding: 3px 8px; border-radius: 4px; margin-left: 10px; border: 1px solid #333; vertical-align: middle; }}
            
            .search-bar {{ padding: 8px 15px; border-radius: 20px; border: 1px solid #444; background-color: #222; color: white; width: 220px; outline: none; }}
            .player-container {{ display: none; width: 100%; max-width: 800px; margin: 20px auto; padding: 0 10px; background: #000; border-radius: 8px; overflow: hidden; border: 2px solid #E50914; }}
            video {{ width: 100%; height: auto; display: block; }}
            .player-title {{ font-size: 20px; font-weight: bold; padding: 10px 0; color: #fff; text-align: center; border-top: 1px solid #222; }}
            .row {{ padding: 0 4%; margin-bottom: 35px; }}
            .row-title {{ font-size: 19px; font-weight: bold; margin-bottom: 15px; color: #fff; }}
            .row-title span {{ color: #E50914; }}
            .posters-container {{ display: flex; gap: 20px; overflow-x: auto; padding: 10px 5px; }}
            .movie-card {{ min-width: 160px; width: 160px; height: 250px; background-color: #1f1f1f; border-radius: 8px; position: relative; overflow: hidden; cursor: pointer; transition: all 0.4s; border: 1px solid #292929; }}
            .movie-card:hover {{ transform: scale(1.05); border-color: #E50914; }}
            .movie-img {{ width: 100%; height: 100%; object-fit: cover; }}
            .card-overlay {{ position: absolute; bottom: 0; left: 0; width: 100%; padding: 15px 10px; background: linear-gradient(to top, rgba(0,0,0,1), rgba(0,0,0,0)); display: flex; flex-direction: column; }}
            .movie-title {{ font-size: 14px; font-weight: bold; color: #fff; margin-bottom: 5px; }}
            .watch-badge {{ font-size: 10px; background: #E50914; color: white; padding: 2px 8px; border-radius: 3px; align-self: flex-start; font-weight: bold; }}
            
            /* Footer Styling */
            .footer {{ text-align: center; padding: 30px 10px; font-size: 13px; color: #555; border-top: 1px solid #222; margin-top: 5px; }}
            .footer span {{ color: #E50914; font-weight: bold; }}

            .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); justify-content: center; align-items: center; z-index: 1000; backdrop-filter: blur(8px); }}
            .modal-content {{ background: #181818; padding: 30px; border-radius: 16px; border: 1px solid #2b2b2b; text-align: center; max-width: 440px; width: 92%; }}
            .modal-title {{ font-size: 22px; color: #fff; font-weight: bold; margin-bottom: 10px; }}
            .modal-movie-target {{ color: #E50914; font-size: 18px; font-weight: bold; margin-bottom: 15px; display: block; }}
            .refer-box {{ background: #111; padding: 12px; border-radius: 8px; font-size: 13px; border: 1px dashed #444; color: #0084FF; word-break: break-all; margin: 15px 0; font-family: monospace; }}
            .action-btn {{ display: block; width: 100%; padding: 12px; border: none; border-radius: 6px; font-size: 15px; font-weight: bold; cursor: pointer; color: white; margin-top: 15px; text-decoration: none; text-align: center; }}
            .btn-verify {{ background-color: #E50914; }}
            .btn-telegram {{ background-color: #0088cc; }}
            .btn-close {{ background: transparent; color: #666; font-size: 13px; border: none; margin-top: 15px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <div class="logo">SHANTANU ADDA <span class="owner-badge">OWNER</span></div>
            <input type="text" class="search-bar" placeholder="🔍 Search movies...">
        </div>

        <div class="player-container" id="videoPlayerBox">
            <video id="mainVideoPlayer" controls controlsList="nodownload">
                <source id="videoSource" src="" type="video/mp4">
            </video>
            <div class="player-title" id="playingMovieTitle">Now Streaming</div>
        </div>

        <div class="row">
            <div class="row-title"><span>🔴</span> Recent Indian Releases</div>
            <div class="posters-container">
                {indian_html}
            </div>
        </div>

        <div class="row">
            <div class="row-title"><span>🎬</span> Hollywood (Hindi Dubbed)</div>
            <div class="posters-container">
                {hollywood_html}
            </div>
        </div>

        <div class="footer">
            © 2026 <span>SHANTANU ADDA</span>. All Rights Reserved. <br>
            <span style="color: #666; font-weight: normal;">Designed for Premium Experience | Powered by OMDb API</span>
        </div>

        <div id="premiumModal" class="modal">
            <div class="modal-content">
                <div class="modal-title">🎁 Unlock Free Movie</div>
                <span class="modal-movie-target" id="modalMovieName">Movie Name</span>
                <p style="font-size: 14px; color: #ccc;">Is film ko free me dekhne ke liye apna referral link 3 dosto ko share karein:</p>
                <div class="refer-box">https://t.me/MOVIEADDA24709?start=refer_user_id</div>
                <a href="https://t.me/MOVIEADDA24709" target="_blank" class="action-btn btn-telegram">🔗 Share on Telegram</a>
                <button class="action-btn btn-verify" onclick="simulateUnlock()">🚀 Check Referrals & Play Movie</button>
                <button class="btn-close" onclick="closeModal()">❌ Close</button>
            </div>
        </div>

        <script>
            let targetedMovie = ""; let targetedStreamUrl = "";
            function openModal(movieName, streamUrl) {{
                targetedMovie = movieName; targetedStreamUrl = streamUrl;
                document.getElementById('modalMovieName').innerText = "🎬 " + movieName;
                document.getElementById('premiumModal').style.display = 'flex';
            }}
            function closeModal() {{ document.getElementById('premiumModal').style.display = 'none'; }}
            
            function simulateUnlock() {{
                alert("🎉 Referrals Verified! Video player screen ke top par shuru ho gaya hai.");
                closeModal();
                document.getElementById('videoPlayerBox').style.display = "block";
                document.getElementById('playingMovieTitle').innerText = "🍿 Now Streaming: " + targetedMovie;
                const player = document.getElementById('mainVideoPlayer');
                const source = document.getElementById('videoSource');
                source.src = targetedStreamUrl;
                player.load(); player.play();
                document.getElementById('videoPlayerBox').scrollIntoView({{ behavior: 'smooth' }});
            }}
        </script>
    </body>
    </html>
    """
    return html_template

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(generate_html(), "utf8"))

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    init_db()
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}")
    while True:
        time.sleep(1)