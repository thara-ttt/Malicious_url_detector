import re
import pandas as pd
from urllib.parse import urlparse

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

