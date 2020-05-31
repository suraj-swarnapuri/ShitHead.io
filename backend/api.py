from flask import Flask
from models.card import Card, make_deck
app = Flask(__name__)

@app.route('/')
def index():
    
    card = Card("d","1")
    return {
        'msg': str(card)
    }