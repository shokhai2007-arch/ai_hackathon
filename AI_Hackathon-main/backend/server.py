import os
import json
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
import httpx

env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    with open(env_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

app = Flask(__name__, static_folder=None)
FRONTEND_DIR = Path(__file__).resolve().parent / 'frontend'

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data or 'context' not in data:
        return jsonify({'error': 'message and context required'}), 400

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return jsonify({'error': 'API key not configured on server'}), 500

    full_prompt = f"{data['context']}\n\nFoydalanuvchi savoli: {data['message']}\n\nJavob:"

    model = "gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(url, json={
                'contents': [{'parts': [{'text': full_prompt}]}]
            })
            result = resp.json()

        if 'candidates' in result and len(result['candidates']) > 0:
            reply = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'reply': reply})

        return jsonify({'error': 'AI response failed', 'detail': result}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"  Frontend: {FRONTEND_DIR}")
    print(f"  Server:   http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
