import requests
import re
import csv
import json
import os
from dotenv import load_dotenv 

load_dotenv()

headline = "NASA confirms discovery of new exoplanet"
description = ""
domain = "https://chatgpt.com"
text = 'app iz good'

def help(headline, description, domain):
    counter = {
        "Clickbait": 0,
        "Emotionally Charged": 0,
        "Manipulative": 0,
        "Domain": 0,
        "Grammar Errors": 0
    }
    
    content = (headline + ' ' + description).lower()

    def keyword_check(content, counter):
        file_path = './keywords.json'
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        for category, keywords in json_data.items():
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in content:
                    print(f"Matched: {keyword} in category: {category}")
                    if category in counter:
                        counter[category] += 1
                    else:
                        print(f"Warning: '{category}' not found in counter!")
        
        print("Updated counter:", counter)
        return counter


    def domain_check(domain, counter):
        pattern = r'https?://(?:www\.)?([^/\s]+)'
        match = re.search(pattern, domain)
        if match:
            d = match.group(1)
            with open("details.csv", newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    first_column = row[0].strip()
                    if d == first_column: 
                        counter["Domain"] += 40
        
        return counter

    def check_grammar_languagetool(text, counter):
        url = "https://api.languagetoolplus.com/v2/check"
        payload = {
            "text": text,
            "language": "en-US"
        }
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                result = response.json()
                matches = result.get("matches", [])
                errors = [{
                    "error_type": m["rule"]["issueType"]
                } for m in matches]
                for error in errors:
                    if error['error_type'] == 'misspelling':
                        counter["Grammar Errors"] += 1
            else:
                print(f"Error: Received status code {response.status_code}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        return counter

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

    def points(counter):
        counter["Clickbait"] = (counter["Clickbait"] // 3) * 3
        counter["Emotionally Charged"] = (counter["Emotionally Charged"] // 5) * 1
        counter["Manipulative"] = (counter["Manipulative"] // 5) * 2
        counter["Clickbait"] = min(counter["Clickbait"], 30)
        counter["Domain"] = min(counter["Domain"], 40) 
        counter["Grammar Errors"] = min(counter["Grammar Errors"], 10)
        return counter

    counter = keyword_check(content, counter)
    counter = domain_check(domain, counter)
    counter = check_grammar_languagetool(text, counter)
    counter = points(counter)

    score = sum(counter.values())
    score1=min(calculate_search_score(fetch_search_results(headline)) * 1.11, 100)
    return int(0.7 * score + 0.3 * score1)

c = help(headline, description, domain)
print(c)
