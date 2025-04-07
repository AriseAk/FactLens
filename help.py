import re
import csv
import requests
import numpy as np
from flask import Flask, redirect, url_for, session, request, jsonify, render_template, flash, send_file
from dotenv import load_dotenv 
import os

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("API_KEY")
app.cx_id = os.getenv("YOUR_CX_ID")

def keyword_check(content, keys, val):
    counter = [0] * len(keys)
    for j in range(len(keys)):
        for k in range(len(val[j])):
            for word in content:
                if word.lower() == val[j][k].lower():
                    counter[j] += 1
    return counter

def dommain_check(domain):
    pattern = r'https?://(?:www\.)?([^/\s]+)'
    match = re.search(pattern, domain)
    if not match:
        return 0
    d = match.group(1)
    with open("details.csv", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if d == row[0]:
                return 40  # High score for suspicious domains
    return 0

def check_grammar_languagetool(text):
    url = "https://api.languagetoolplus.com/v2/check"
    payload = {"text": text, "language": "en-US"}
    response = requests.post(url, data=payload)
    result = response.json()
    matches = result.get("matches", [])
    errors = [m["rule"]["issueType"] for m in matches]
    return sum(1 for e in errors if e == 'misspelling')

def extract_features(headline, description, domain):
    content = (headline + description).split()
    
    # Keywords check
    keys = ['Clickbait', 'Emotionally charged', 'Manipulative']
    val = [["You won't believe", "This will blow your mind", "What happens next is shocking"],
           ['Disaster', 'Horrific', 'Outrageous', 'Fake'],
           ["Mustshare", "Wake up!", "The truth they don't want you to know"]]
    keyword_scores = keyword_check(content, keys, val)

    domain_score = dommain_check(domain)

    grammar_errors = check_grammar_languagetool(description)
    
    features = np.array(keyword_scores + [domain_score] + [grammar_errors])
    
    return features


def fetch_search_results(query):
    api_key = os.getenv("API_KEY")
    cx = os.getenv("YOUR_CX_ID")
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data=response.json()
        if data:
            for item in data.get("items", []):
                print(item["title"], "-", item["link"])
        return data
    else:
        print("Error:", response.status_code, response.text)
        return None
    
def calculate_search_score(results):
    if not results or "items" not in results:
        return 10  
    count=len(results["items"])

    if count>=5:
        return 90
    elif count>=3:
        return 70
    elif count>=1:
        return 40
    else:
        return 10

    
headline = "NASA confirms discovery of new exoplanet"
results = fetch_search_results(headline)
score=calculate_search_score(results)

print(results)
print(score)