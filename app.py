
# --- Flask Backend for Malicious URL Detector ---
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import re
from urllib.parse import urlparse

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.pkl')

# Whitelist of known safe domains
SAFE_DOMAINS = set([
    'google.com', 'www.google.com', 'youtube.com', 'www.youtube.com',
    'facebook.com', 'www.facebook.com', 'twitter.com', 'www.twitter.com',
    'microsoft.com', 'www.microsoft.com', 'github.com', 'www.github.com',
    'wikipedia.org', 'www.wikipedia.org', 'amazon.com', 'www.amazon.com','redit.com', 'www.reddit.com',
    'linkedin.com', 'www.linkedin.com', 'apple.com', 'www.apple.com', 'instagram.com', 'www.instagram.com',
    'pinterest.com', 'www.pinterest.com', 'yahoo.com', 'www.yahoo.com', 'bing.com', 'www.bing.com',
    'stackoverflow.com', 'www.stackoverflow.com', 'quora.com', 'www.quora.com',
    'cnn.com', 'www.cnn.com', 'bbc.com', 'www.bbc.com', 'nytimes.com', 'www.nytimes.com',
    'reddit.com', 'www.reddit.com', 'whatsapp.com', 'www.whatsapp.com', 'tiktok.com', 'www.tiktok.com',
    'paypal.com', 'www.paypal.com', 'ebay.com', 'www.ebay.com', 'craigslist.org', 'www.craigslist.org',
    'dropbox.com', 'www.dropbox.com', 'spotify.com', 'www.spotify.com', 'netflix.com', 'www.netflix.com',
    'zoom.us', 'www.zoom.us', 'slack.com', 'www.slack.com', 'discord.com', 'www.discord.com',
    'githubusercontent.com', 'www.githubusercontent.com', 'bitbucket.org', 'www.bitbucket.org',
    'medium.com', 'www.medium.com', 'wordpress.com', 'www.wordpress.com'
])

def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path
    features = {}
    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['has_ip'] = 1 if re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', url) else 0
    features['has_at'] = 1 if '@' in url else 0
    features['has_hyphen'] = 1 if '-' in url else 0
    features['has_https'] = 1 if url.lower().startswith('https') else 0
    features['domain_length'] = len(domain)
    features['path_length'] = len(path)
    features['num_slash'] = url.count('/')
    features['num_params'] = url.count('=')
    keywords = ['login', 'update', 'verify', 'secure', 'account', 'banking']
    features['has_suspicious_keyword'] = 1 if any(k in url.lower() for k in keywords) else 0
    return pd.DataFrame([features])

@app.route('/')
def home():
    return '<h2>Malicious URL Detector API is running.</h2>'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Whitelist check
    domain = urlparse(url).netloc.lower()
    if domain in SAFE_DOMAINS:
        return jsonify({'url': url, 'prediction': 'benign', 'note': 'Domain is whitelisted.'})

    features = extract_features(url)
    prediction = model.predict(features)[0]
    result = 'benign' if prediction == 0 else 'malicious'
    return jsonify({'url': url, 'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)

