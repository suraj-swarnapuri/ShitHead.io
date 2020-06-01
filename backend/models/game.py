import random
import json
from models.card import Deck
class Game():
    def __init__(self, id, players=[],current_stack=[], draw_pile=[], turn_token="TOKEN"):
        if not draw_pile:
            self.draw_pile = Deck()
        else:
            self.draw_pile= draw_pile
        
        self.players = players
        self.turn_token = turn_token
        self.current_stack = current_stack
        self.id = id

    def shuffle_deck(self):
        #shuffles deck
        random.shuffle(self.draw_pile.cards)
    def join_game(self,player):
        self.players.append(player)
    def is_turn(self,player_id):
        return self.players[0].id == player_id
    def get_card(self):
        return self.draw_pile.pop
    
class GameSerializer():
    def serialize(self, game):
        json_data = json.dumps(game, default=lambda  o: o.__dict__,indent=4)
        return json.loads(json_data)
    def deserialize(self,json_data):
        game = Game(**json.loads(json_data))
        return game
