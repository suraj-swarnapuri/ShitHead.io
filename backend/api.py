from flask import Flask,request
import json
from models.game import Game, GameSerializer
from models.card import CardSerializer, Deck
from models.player import Player, PlayerSerialzer

app = Flask(__name__)
player_map = dict()
total_game = 0
game_map = dict()

@app.route('/player/create', methods = ['POST'])
def create_player():
    user = request.form.get('user')
    player = Player(user)
    if player.user in player_map:
        return{
            "status_code": "400",
            "msg": "Player already exists"
        }
    player_map[player.user] = player
    return {
        "status_code": "204"
    }
    
   
@app.route('/player/<username>')
def get_player(username):
    ps = PlayerSerialzer()
    if username in player_map:
        return {
            "status_code": "200",
            "player": ps.serialize(player_map[username])  
        }
    return {
        "status_code": "400",
        "msg": "player could not be found"
    }

@app.route('/game/create', methods=['POST'])
def create_game():
    user = request.form.get('user')
    ps = PlayerSerialzer()
    cs = CardSerializer()
    if user not in player_map:
        return {
            "status_code": "400",
            "msg" : "player not found"
        }

    player = player_map[user]
    global total_game
    game = Game(total_game)
    
    game.shuffle_deck()
    hand = Deck(game.draw_pile.cards[0:3])
    table = Deck(game.draw_pile.cards[3:7])
    game.draw_pile.cards = game.draw_pile.cards[7:]
    player.hand = hand
    player.table = table
    game_map[total_game] = game
    return{
        "status_code": "200",
        "hand" : cs.serialize_deck(player.hand),
        "table": cs.serialize_deck(Deck(table.cards[0:2])),
        "gameid": total_game,
        "token": game.turn_token

    }


@app.route('/game/join', methods=['POST'])
def join_game(gameid):
    user = request.form.get('playerid')
    gameid = request.form.get('gameid')
    ps = PlayerSerialzer()
    cs = CardSerializer()
    if user not in player_map:
        return {
            "status_code": "400",
            "msg" : "player not found"
        }
    player = player_map[user]
    game = game_map[int(gameid)]
    game.join_game(player.user)
    hand = Deck(game.draw_pile.cards[0:3])
    table = Deck(game.draw_pile.cards[3:7])
    game.draw_pile.cards = game.draw_pile.cards[7:]
    player.hand = hand
    player.table = table
    return{
        "status_code": "200",
        "hand" : cs.serialize_deck(player.hand),
        "table": cs.serialize_deck(Deck(table.cards[0:2])),
        "gameid": game.id,
    }
    


