import os
import json
import base64
import io
import re
from dotenv import load_dotenv

load_dotenv() # Ini buat ngebaca file .env tadi

from PIL import Image
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
# INI IMPORT VERSI BARU
from google import genai 

app = Flask(__name__)
CORS(app) # Pindahin ke sini biar Flask nggak bingung

@app.route('/')
def home():
    return render_template('deteksi muka.html')

# INI CARA INISIALISASI VERSI BARU
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route('/analyze', methods=['POST'])
def analyze_face():
    try:
        data = request.json
        image_raw = data.get('image', '')
        
        # Penanganan aman kalau format base64 beda-beda
        if ',' in image_raw:
            image_data = image_raw.split(",")[1]
        else:
            image_data = image_raw
            
        image_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(image_bytes))

        print("Mengirim foto ke Cloud AI Generasi Baru...")

        # PROMPT MASTERPIECE KAMU (100% UTUH)
        prompt = """
        Anda adalah sistem AI penganalisis citra visual tingkat lanjut dengan kemampuan identifikasi multi-domain.
        
        TUGAS PERTAMA: Identifikasi subjek utama. Masuk ke kategori mana:
        1. Manusia (Normal / Ekspresi Konyol)
        2. Hewan (Normal / Meme)
        3. Kartun / Anime 
        4. Sosok Hantu / Cursed Image

        LOGIKA ANALISIS DAN PENGGUNAAN KATA BERDASARKAN KATEGORI:

        - JIKA MANUSIA: 
          1. PERKIRAKAN USIA subjek secara visual terlebih dahulu.
          2. SESUAIKAN GAYA BAHASA DENGAN ESTIMASI USIA: Jika anak-anak/remaja/lansia gunakan bahasa yang ramah, hangat, dan santai. Jika dewasa/mahasiswa gunakan bahasa profesional dan analitis.
          3. Gunakan logika Golden Ratio. Awalan kalimat WAJIB menggunakan: "Analisis Mata:", "Analisis Hidung:", "Analisis Bibir:", "Analisis Rahang:", dan "Analisis Kulit:". (DILARANG KERAS menggunakan kata "Bulu", "Moncong", atau "Tekstur" untuk manusia).
          
        - JIKA HEWAN: 
          Berikan skor kelucuan/kesehatan. Awalan kalimat WAJIB menggunakan: "Analisis Mata:", "Analisis Moncong/Hidung:", "Analisis Mulut:", "Analisis Struktur:", dan "Analisis Bulu/Sisik:".

        - JIKA KARTUN/ANIME: 
          Analisis estetika gambar. Awalan kalimat WAJIB menggunakan: "Analisis Visual:", "Analisis Hidung:", "Analisis Mulut:", "Analisis Struktur Garis:", dan "Analisis Tekstur/Warna:".

        - JIKA HANTU / CURSED IMAGE:
          SANGAT PENTING: Paksa "skor_akhir" menjadi SANGAT RENDAH (1.0 - 3.0) karena estetikanya hancur berantakan. JANGAN MENGANGGAP skor_akhir sebagai "skor keseraman" (jangan beri nilai tinggi!). Berikan reaksi panik/merinding pada teks.

        - JIKA MANUSIA EKSPRESI KONYOL:
          Berikan roasting komedi ringan (stand-up comedy style), JANGAN gunakan kata-kata kasar. SANGAT PENTING: Paksa "skor_akhir" dan skor kategori (simetri, proporsi, dll) menjadi RENDAH (berkisar 3.0 - 5.5). Ingat, ekspresi plenger ini MERUSAK Golden Ratio secara sengaja. Jangan berikan skor tinggi hanya karena fotonya lucu atau menghibur!

        - JIKA ADA FITUR TERHALANG (Pakai Kacamata, Masker, dll):
          Jika mata tertutup kacamata (termasuk kacamata anti-radiasi) atau ada fitur lain yang terhalang, jangan berikan skor hancur pada fitur tersebut. Berikan skor rata-rata/standar (sekitar 7.0 - 7.5), dan pada teks analisisnya, sebutkan bahwa fitur tersebut "Terlindungi oleh kacamata/aksesoris" sehingga tidak bisa dianalisis secara maksimal, tapi tetap terlihat proporsional.

        ATURAN MUTLAK FORMAT JSON (WAJIB PATUH ATAU SISTEM RUSAK):
        1. DILARANG KERAS menggunakan karakter tanda kutip dua (" ") di dalam nilai teks/kalimat! Jika butuh penekanan kata, gunakan tanda kutip tunggal (' ').
        2. Jangan gunakan enter (newline) berlebihan di dalam teks.

        WAJIB BERIKAN OUTPUT HANYA DALAM FORMAT JSON SAJA.
        {
            "skor_akhir": 9.5,
            "kategori": {
                "simetri": 8.0, "proporsi": 7.5, "mata": 8.2, "hidung": 8.1, "bibir": 7.9, "rahang": 8.3, "kulit": 8.6, "harmoni": 8.5
            },
            "analisis_teks": [
                "[Awalan Sesuai Kategori di Atas]: (Penjelasan)",
                "[Awalan Sesuai Kategori di Atas]: (Penjelasan)",
                "[Awalan Sesuai Kategori di Atas]: (Penjelasan)",
                "[Awalan Sesuai Kategori di Atas]: (Penjelasan)",
                "[Awalan Sesuai Kategori di Atas]: (Penjelasan)",
                "Analisis Keseluruhan: (Simpulan akhir tentang aura subjek)."
            ]
        }
        """

        # GANTI JADI BEGINI JALUR AJAIBNYA (Pakai gemini-1.5-flash yang super stabil)
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=[prompt, img]
        )
        
        # --- JURUS SAPU BERSIH JSON (Anti-Crash) ---
        response_text = response.text
        print(f"Mentahan dari Gemini: {response_text}") # Biar gampang dilacak di Vercel
        
        # Cari paksa blok JSON di dalam teks pakai Regex
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            clean_json = match.group(0)
        else:
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            
        hasil_ai = json.loads(clean_json)

        print(f"BERHASIL! Skor AI: {hasil_ai.get('skor_akhir', 'N/A')}")

        return jsonify({
            "status": "success",
            "skor": hasil_ai["skor_akhir"],
            "kategori": hasil_ai["kategori"],
            "analisis_teks": hasil_ai["analisis_teks"]
        })

    # NAH INI BAGIAN YANG TADI KEPOTONG
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

# INI JUGA PENTING BIAR SERVER FLASK NYALA
if __name__ == '__main__':
    # Render akan memberikan port secara otomatis, kita harus menangkapnya
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)