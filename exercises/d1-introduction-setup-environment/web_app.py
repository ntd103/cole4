from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cat-fact')
def get_cat_fact():
    try:
        response = requests.get('https://catfact.ninja/fact', timeout=10)
        if response.status_code == 200:
            fact_data = response.json()
            return jsonify({
                'success': True,
                'fact': fact_data['fact'],
                'length': fact_data['length'],
                'timestamp': datetime.now().isoformat()
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)