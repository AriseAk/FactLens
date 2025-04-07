import requests
import re
import csv

headline='Deepika disaster Padukone paints the town red in power suit extravaganza! Mustshare'
description=" Indian film star, Deepika Padukone turned heads with her bold and vibrant red pantsuit at her foundation's event, showcasing the power of a statement ensemble. The actress opted for a fiery red power suit from the brand URA, exuding confidence and elegance. The oversized blazer, crafted from a luxurious crepe-silk fabric, featured padded shoulders and notch lapels, giving it a structured yet sophisticated look. Paired with matching red trousers, Deepika made a strong fashion statement with this perfectly coordinated outfit."
counter=[0,0,0,0,0]
content=(headline+description).split()
keys=['Clickbait','Emotionally charged','Manipulative']
val=[["You won't believe", "This will blow your mind", "What happens next is shocking"],['Disaster', 'Horrific', 'Outrageous', 'Fake'],["Mustshare", "Wake up!", "The truth they don't want you to know"]]
domain="https://worldnewsdailyreport.com"
text='app iz good'
fdomains=['notiziepericolose.blogspot.it','worldnewsdailyreport.com']
title="You Won't Believe What This Politician Said About Vaccines!"

def keyword_check(content,keys,val,counter):
    for j in range(len(keys)):
        for k in range(len(val[j])):
            for i in content:
                word=i.lower()
                if word ==val[j][k].lower():
                    counter[j]+=1
    return counter

def dommain_check(domain,counter):
    pattern = r'https?://(?:www\.)?([^/\s]+)'
    match = re.search(pattern, domain)
    d=match.group(1)
    with open("details.csv",newline='') as file:
        reader=csv.reader(file)
        for row in reader:
            first_column=row[0]
            if d == first_column:
                counter[3]+=50
                return counter

def check_grammar_languagetool(text,counter):
    url = "https://api.languagetoolplus.com/v2/check"
    payload = {
        "text": text,
        "language": "en-US"
    }
    response = requests.post(url, data=payload)
    result = response.json()
    matches = result.get("matches", [])
    errors = [{
        "error_type": m["rule"]["issueType"]
    } for m in matches]
    for i in errors:
        if i['error_type']=='misspelling':
            counter[4]+=1
    return counter

def points(counter):
    counter[0]=(counter[0]//3)*30
    counter[1]=(counter[1]//5)*10
    counter[2]=(counter[2]//5)*20
    counter[4]=(counter[4]//2)*10
    return counter

check_grammar_languagetool(text,counter)
keyword_check(content,keys,val,counter)
dommain_check(domain,counter)
points(counter) 
print(counter)

