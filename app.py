from flask import Flask, render_template_string, request, redirect
import requests
import os

app = Flask(__name__)

HTML_TASARIM = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formatman | Python Global Engine</title>
    <style>
        :root {
            --bg-color: #06070d;
            --card-bg: #0b0d19;
            --purple-neon: #a855f7;
            --green-neon: #22c55e;
            --text-main: #ffffff;
            --text-muted: #64748b;
            --border-glow: rgba(168, 85, 247, 0.25);
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
            background-image: radial-gradient(circle at 50% 50%, #120e2e 0%, #06070d 100%);
        }
        
        .container {
            width: 100%;
            max-width: 520px;
            background: var(--card-bg);
            border-radius: 24px;
            padding: 40px 30px;
            border: 1px solid rgba(168, 85, 247, 0.2);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 40px var(--border-glow);
            text-align: center;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--purple-neon), #6366f1, var(--green-neon));
        }
        
        h1 {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #c084fc, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 3px;
            margin-bottom: 5px;
            text-transform: uppercase;
            text-shadow: 0 0 20px rgba(168, 85, 247, 0.4);
        }
        
        .subtitle {
            color: var(--text-muted);
            font-size: 13px;
            margin-bottom: 35px;
            letter-spacing: 2px;
            font-weight: 700;
            text-transform: uppercase;
        }
        
        .input-group {
            margin-bottom: 30px;
            text-align: left;
        }
        
        label {
            display: block;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            color: var(--purple-neon);
            margin-bottom: 12px;
            letter-spacing: 1.5px;
        }
        
        .url-input {
            width: 100%;
            padding: 18px 20px;
            background: #030408;
            border: 2px solid #1e2238;
            border-radius: 16px;
            color: white;
            font-size: 15px;
            outline: none;
            transition: all 0.3s ease;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
        }
        
        .url-input:focus {
            border-color: var(--purple-neon);
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.35), inset 0 2px 4px rgba(0,0,0,0.5);
        }
        
        .action-btns {
            display: flex;
            gap: 15px;
        }
        
        .convert-btn {
            flex: 1;
            padding: 18px;
            border: none;
            border-radius: 16px;
            color: white;
            font-size: 15px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .convert-btn:hover {
            transform: translateY(-3px);
        }
        
        .convert-btn:active {
            transform: translateY(1px);
        }
        
        .btn-mp3 {
            background: linear-gradient(135deg, #a855f7, #4f46e5);
            box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);
        }
        
        .btn-mp3:hover {
            box-shadow: 0 6px 25px rgba(168, 85, 247, 0.6);
        }
        
        .btn-mp4 {
            background: linear-gradient(135deg, #22c55e, #15803d);
            box-shadow: 0 4px 20px rgba(34, 197, 94, 0.4);
        }
        
        .btn-mp4:hover {
            box-shadow: 0 6px 25px rgba(34, 197, 94, 0.6);
        }
        
        .footer-credit {
            margin-top: 35px;
            font-size: 11px;
            color: #475569;
            letter-spacing: 1px;
            font-weight: 600;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Formatman</h1>
        <div class="subtitle">Python Global Media Engine</div>
        
        <form action="/indir" method="POST">
            <div class="input-group">
                <label for="mediaUrl">Medya Bağlantısı</label>
                <input type="url" id="mediaUrl" name="url" class="url-input" placeholder="YouTube linkini buraya yapıştırın..." required autocomplete="off">
            </div>
            
            <div class="action-btns">
                <button type="submit" name="format" value="mp3" class="convert-btn btn-mp3">🎵 MP3 Ses</button>
                <button type="submit" name="format" value="mp4" class="convert-btn btn-mp4">📺 MP4 Video</button>
            </div>
        </form>
        
        <div class="footer-credit">POWERED BY EYMENCRAFT & PYTHON</div>
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
    format_secimi = request.form.get('format')
    
    try:
        # Yeni ve süper hızlı alternatif tünel API'si
        api_url = "https://api.ddownr.com/v1/create"
        
        # İstek başlıkları
        headerlar = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Seçilen formata göre kaliteyi ayarlıyoruz
        kalite = "mp3" if format_secimi == "mp3" else "720"
        
        veri = {
            "url": url,
            "format": kalite
        }
        
        cevap = requests.post(api_url, json=veri, headers=headerlar)
        sonuc = cevap.json()
        
        # ddownr API'si bazen 'url' yerine doğrudan indirme id'si veya linki döner
        if "url" in sonuc:
            return redirect(sonuc["url"])
        elif "downloadUrl" in sonuc:
            return redirect(sonuc["downloadUrl"])
        else:
            # Yedek hızlı yöntem (Eğer JSON patlarsa direkt yönlendirme tüneli)
            backup_url = f"https://loader.to/api/button/?url={url}&f={kalite}"
            return redirect(backup_url)
            
    except Exception as e:
        # Hata anında bile kullanıcıyı boş bırakmıyoruz, yedek indirme tüneline fırlatıyoruz
        kalite = "mp3" if format_secimi == "mp3" else "720"
        return redirect(f"https://loader.to/api/button/?url={url}&f={kalite}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
