from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

HTML_TASARIM = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Formatman | Python Limitsiz Web</title>
    <style>
        body { background: #090a0f; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .box { background: #131522; padding: 40px; border-radius: 20px; border: 1px solid rgba(168,85,247,0.2); text-align: center; width: 100%; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h1 { background: linear-gradient(135deg, #a855f7, #6366f1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; margin: 0; font-weight: 900; }
        input { width: 100%; padding: 15px; background: #0d0e16; border: 2px solid #222538; border-radius: 10px; color: white; margin: 20px 0; box-sizing: border-box; }
        button { width: 100%; padding: 15px; border: none; border-radius: 10px; color: white; font-weight: bold; cursor: pointer; text-transform: uppercase; background: linear-gradient(135deg, #a855f7, #6366f1); }
    </style>
</head>
<body>
    <div class="box">
        <h1>FORMATMAN</h1>
        <p style="color: #94a3b8; font-weight: bold;">%100 PYTHON TABANLI WEB MOTORU</p>
        <form action="/indir" method="POST">
            <input type="text" name="url" placeholder="YouTube Linkini Yapıştırın..." required>
            <button type="submit">🎵 MP3 Olarak Python İle Üret</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def ana_sayfa():
    return render_template_string(HTML_TASARIM)

@app.route('/indir', methods=['POST'])
def indir():
    url = request.form.get('url')
    gecici_klasor = tempfile.gettempdir()
    dosya_taslagi = os.path.join(gecici_klasor, '%(title)s.%(ext)s')
    
    ydl_opts = {
        'outtmpl': dosya_taslagi,
        'restrictfilenames': True,
        'quiet': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            indirilen_dosya = ydl.prepare_filename(info)
            indirilen_dosya = os.path.splitext(indirilen_dosya)[0] + '.mp3'
        return send_file(indirilen_dosya, as_attachment=True)
    except Exception as e:
        return f"❌ Python Hatası: {e}"

if __name__ == '__main__':
    # Render sunucusu için port ayarı
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)