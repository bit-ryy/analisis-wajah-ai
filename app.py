import os
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('deteksi muka.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"status": "error", "message": "Cuy, fotonya mana?"}), 400

        # Bikin base skor acak tapi realistis
        base_skor = round(random.uniform(5.0, 8.8), 1)
        
        # Generate Skor Kategori
        k = {
            "simetri": max(1.0, min(10.0, round(base_skor + random.uniform(-1.5, 1.5), 1))),
            "proporsi": max(1.0, min(10.0, round(base_skor + random.uniform(-1.0, 1.2), 1))),
            "mata": max(1.0, min(10.0, round(base_skor + random.uniform(-1.5, 1.5), 1))),
            "hidung": max(1.0, min(10.0, round(base_skor + random.uniform(-1.5, 1.0), 1))),
            "bibir": max(1.0, min(10.0, round(base_skor + random.uniform(-1.2, 1.2), 1))),
            "rahang": max(1.0, min(10.0, round(base_skor + random.uniform(-1.5, 1.5), 1))),
            "kulit": max(1.0, min(10.0, round(base_skor + random.uniform(-2.0, 1.5), 1))),
            "harmoni": base_skor
        }

        # Fungsi pintar pembuat kalimat otomatis berdasarkan skor
        def get_text(fitur, skor):
            if skor >= 8.0:
                texts = [f"Bentuk {fitur} terlihat sangat proporsional dan estetik.", f"{fitur.capitalize()} memberikan karakter yang sangat kuat pada wajah.", f"Garis {fitur} sangat tajam dan mendominasi secara positif."]
            elif skor >= 6.0:
                texts = [f"{fitur.capitalize()} terlihat wajar, natural, dan seimbang.", f"Proporsi {fitur} cukup standar namun tetap mendukung harmoni wajah.", f"Kondisi {fitur} cukup baik, pencahayaan foto mungkin sedikit memengaruhi."]
            else:
                texts = [f"Sudut pengambilan foto mungkin membuat {fitur} terlihat kurang simetris.", f"Perlu pencahayaan atau *angle* yang lebih baik untuk mempertegas {fitur}.", f"{fitur.capitalize()} memiliki bentuk yang unik dan *anti-mainstream*."]
            return random.choice(texts)

        # Rangkai list analisis agar persis seperti yang kamu minta
        analisis_list = [
            f"Mata ({k['mata']}/10): {get_text('mata', k['mata'])}",
            f"Hidung ({k['hidung']}/10): {get_text('hidung', k['hidung'])}",
            f"Bibir ({k['bibir']}/10): {get_text('bibir', k['bibir'])}",
            f"Garis Rahang ({k['rahang']}/10): {get_text('garis rahang', k['rahang'])}",
            f"Kualitas Kulit ({k['kulit']}/10): {get_text('tekstur kulit', k['kulit'])}"
        ]

        paket_data = {
            "status": "success",
            "skor": base_skor,
            "kategori": k,
            "analisis_teks": analisis_list
        }

        return jsonify(paket_data)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)