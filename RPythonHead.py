from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode


# Reddit account information

app = Flask(__name__)
ask = Ask(app,'/')

def headlineGet():
    user_info = {'user': 'neko_nyan',
                 'passwd': 'poopnugget',
                 'api_type' : 'json'}
    session = requests.Session()
    session.headers.update({'User-Agent':'Alexa Skill build: neko_nyan'}) # insert reddit username
    session.post('https://www.reddit.com/dev/api', data = user_info)
    time.sleep(1)
    url = 'https://www.reddit.com/r/python/.json?limit=10'
    html = session.get(url)
    data = json.loads(html.content.decode('utf-8'))
    listTitle = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    listTitle = '...'.join(listTitle)
    return listTitle

@app.route('/')
def index():
    return 'Welcome to the homepage.'

@ask.launch
def launched():
    launch_q = 'Want me to tell you the headlines for reddit\'s python subreddit?'
    return question(launch_q)

@ask.intent('YesIntent')
def head_speak():
    headlines = headlineGet()
    Yes_Speak = 'The headlines for today are {}'.format(headlines)
    return statement(Yes_Speak)

@ask.intent('NoIntent')
def no_speak():
    goodbye = 'Okay then. Good bye'
    return statement(goodbye)

if __name__ == '__main__':
    app.run(debug = True)