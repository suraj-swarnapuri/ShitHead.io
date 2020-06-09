from flask import Flask, request, jsonify
import json
from models.game import Game, GameSerializer
from models.card import CardSerializer, Deck
from models.player import Player, PlayerSerialzer

app = Flask(__name__)
player_map = dict()
total_game = 0
game_map = dict()
test_val = 0

# Player api


@app.route('/player/create', methods=['POST'])
def create_player():
    user = request.form.get('user')
    player = Player(user)
    if user == None:
        return jsonify({
            "status_code": "400",
            "msg": "User not defined"
        })
    if player.user in player_map:
        return jsonify({
            "status_code": "400",
            "msg": "Player already exists"
        })
    player_map[player.user] = player
    return jsonify({
        "status_code": "204"
    })


@app.route('/player/players')
def get_players():
    ps = PlayerSerialzer()
    player_list = [ps.serialize(p) for p in list(player_map.values())]
    return jsonify({
        "status_code": "200",
        "players": player_list
    })


@app.route('/player/<username>')
def get_player(username):
    ps = PlayerSerialzer()
    if username in player_map:
        return jsonify({
            "status_code": "200",
            "player": ps.serialize(player_map[username])
        })
    return jsonify({
        "status_code": "400",
        "msg": "player {0} could not be found".format(username)
    })

# Game api


@app.route('/game/create', methods=['POST'])
def create_game():
    user = request.form.get('user')
    ps = PlayerSerialzer()
    cs = CardSerializer()
    if user not in player_map:
        return jsonify({
            "status_code": "400",
            "msg": "player not found"
        })

    player = player_map[user]
    global total_game
    # set up game
    game = Game(total_game)
    game.shuffle_deck()
    # pass out cards
    


@app.route('/game/join', methods=['POST'])
def join_game():
    user = request.form.get('user')
    gameid = request.form.get('gameid')
    ps = PlayerSerialzer()
    cs = CardSerializer()
    if user not in player_map:
        return jsonify({
            "status_code": "400",
            "msg": "player not found"
        })
    player = player_map[user]
    game = game_map[int(gameid)]
    if len(game.players) > 7:
        return jsonify({
            "status_code": "400",
            "msg": "Game is full sorry"
        })
    if game.join_game(player.user) == False:
        return jsonify({
            "status_code": "400",
            "msg": "user already in game"
        })
    hand = Deck(game.draw_pile.cards[0:3])
    table = Deck(game.draw_pile.cards[3:7])
    game.draw_pile.cards = game.draw_pile.cards[7:]
    player.hand = hand
    player.table = table
    return jsonify({
        "status_code": "200",
        "hand": cs.serialize_deck(player.hand),
        "table": cs.serialize_deck(Deck(table.cards[0:2])),
        "gameid": game.id,
    })


@app.route('/game/<gameid>/turn', methods=['POST', 'GET'])
def game_turn(gameid):
    user = request.args.get('user')
    if request.method == 'GET':
        return _get_turn(int(gameid), user)
    else:
        payload = request.form.get('payload')

        return _post_turn(int(gameid), user, json.loads(payload))


def _get_turn(gameid, user):
    # helper method for GET:/game/<gameid>/turn
    cs = CardSerializer()
    ps = PlayerSerialzer()
    if user not in player_map:
        return jsonify({
            "status_code": "400",
            "msg": "player not found"
        })
    if gameid not in game_map:
        return jsonify({
            "status_code": "400",
            "msg": "game not found"
        })
    game = game_map[gameid]
    player = player_map[user]
    if game.is_turn(player):
        current_card = cs.serialize(game.get_current())
        return jsonify({
            "status_code": "200",
            "current_card": current_card,
            "hand": cs.serialize_deck(player.hand),
            "table": cs.serialize_deck(Deck(player.table.cards[0:2])),
            "gameid": game.id,
        })
    return jsonify({
        "status_code": "400",
        "msg": "it is not your turn yet"
    })


def _post_turn(gameid, user, payload):
    # helper method for POST:/game/<gameid>/turn
    cs = CardSerializer()
    ps = PlayerSerialzer()
    if user not in player_map:
        return jsonify({
            "status_code": "400",
            "msg": "player not found"
        })
    if gameid not in game_map:
        return jsonify({
            "status_code": "400",
            "msg": "game not found"
        })
    game = game_map[gameid]
    player = player_map[user]
    if game.is_turn(player):
        submit = cs.deserialize_dec(payload['submit'])

@app.route('/test/concurrency')
def test_con():
    global test_val
    test_val+=1
    return jsonify({
        "val": test_val
    })