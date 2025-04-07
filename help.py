import re
import csv
import requests
import numpy as np

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
    
    # Domain check
    domain_score = dommain_check(domain)
    
    # Grammar check
    grammar_errors = check_grammar_languagetool(description)
    
    # Combine features into a single array
    features = np.array(keyword_scores + [domain_score] + [grammar_errors])
    
    return features
