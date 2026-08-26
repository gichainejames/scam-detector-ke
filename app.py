from flask import Flask, request, jsonify
from rules import check_scam

app = Flask(__name__)

# --- HTML WITH PWA HEAD ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="monetag" content="e6825a9f13a6698ce537cea6e863e2bf">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scam Detector KE 🛡️</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#00ff88">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <style>
        body { background: #0a0a0a; color: white; font-family: sans-serif; padding: 20px; max-width: 500px; margin: auto; }
        h1 { color: #00ff88; text-align: center; }
        input, textarea { width: 100%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #333; background: #1a1a1a; color: white; font-size: 16px; }
        button { width: 100%; padding: 14px; background: #00ff88; color: black; border: none; border-radius: 8px; font-weight: bold; font-size: 18px; cursor: pointer; }
        #result { margin-top: 20px; padding: 15px; border-radius: 8px; display: none; font-weight: bold; }
        .scam { background: #ff0040; }
        .safe { background: #00ff88; color: black; }
        small { color: #888; }
    </style>
</head>
<body>
    <h1>🛡️ Scam Detector KE</h1>
    <p style="text-align:center;"><small>Check M-PESA & fake messages instantly</small></p>
    
    <label>Sender Name (e.g. M-PESA, 0712345678):</label>
    <input type="text" id="sender" placeholder="M-PESA">

    <label>SMS Message:</label>
    <textarea id="message" rows="5" placeholder="e.g. Congratulations you won 50,000 KES click http://bit.ly/xyz"></textarea>

    <button onclick="check()">CHECK NOW</button>

    <div id="result"></div>

    <p style="text-align:center; margin-top:30px;"><small>Tip: On phone Chrome → Menu ⋮ → Add to Home Screen to install as app</small></p>

    <script>
        async function check(){
            const sender = document.getElementById('sender').value;
            const message = document.getElementById('message').value;
            const resDiv = document.getElementById('result');
            if(!message){ alert('Type message first'); return; }
            const res = await fetch('/check', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({sender, message})
            });
            const data = await res.json();
            resDiv.style.display = 'block';
            resDiv.textContent = (data.is_scam ? '🚨 SCAM: ' : '✅ SAFE: ') + data.reason;
            resDiv.className = data.is_scam ? 'scam' : 'safe';
        }

        // Register service worker for installable app
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/service-worker.js');
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    msg = data.get("message", "")
    sender = data.get("sender", "")
    is_scam, reason = check_scam(msg, sender)
    return jsonify({"is_scam": is_scam, "reason": reason})

@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name": "Scam Detector KE",
        "short_name": "ScamKE",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a0a0a",
        "theme_color": "#00ff88",
        "icons": [
            {"src": "https://cdn-icons-png.flaticon.com/512/3064/3064197.png", "sizes": "512x512", "type": "image/png"}
        ]
    })

@app.route("/service-worker.js")
def sw():
    return """
    self.addEventListener('install', e => self.skipWaiting());
    self.addEventListener('activate', e => self.clients.claim());
    self.addEventListener('fetch', e => e.respondWith(fetch(e.request)));
    """, 200, {'Content-Type': 'application/javascript'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
