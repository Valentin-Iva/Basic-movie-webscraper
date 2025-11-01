from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import random
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    #process input
    user_input = request.form['user_input']
    user_input = (user_input.replace(" ", "-")).lower()

    #springfield URL
    url = f"https://www.springfieldspringfield.co.uk/movie_script.php?movie={user_input}"

    # Send request
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Process text 
    script_list = [t.get_text(strip=False) for t in soup.find_all("div", class_="scrolling-script-container")]

    script_text =(" ".join(script_list).replace("<br>", "@"))

    sentences = re.split(r'(?<=[.!?])', script_text)
    
    random_sentence = random.choice(sentences)
    if random_sentence==".":
        random_sentence = random.choice(sentences)
        random_sentence= '"'+ random_sentence +'"'
    elif random_sentence=="":
        random_sentence="(No results. Did you spell it right?)"
    else:
        random_sentence= '"'+ random_sentence +'"'
        
    return render_template('results.html', user_input=user_input, script=random_sentence)

if __name__ == '__main__':
    app.run(debug=True)