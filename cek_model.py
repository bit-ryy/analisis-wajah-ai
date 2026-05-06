from google import genai

# MASUKKAN API KEY KAMU YANG BARU DI SINI
client = genai.Client(api_key="AIzaSyC8pDykTGTIdThxGoMK7tT3ehCf1xGYtEU")

print("Daftar Otak AI yang tersedia untuk API Key kamu:")
for m in client.models.list():
    if 'generateContent' in m.supported_actions:
        print("-", m.name)