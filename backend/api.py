#from flask import Flask
import json
from models.game import Game, GameSerializer
from models.player import Player
#app = Flask(__name__)


gs = GameSerializer()
game = Game(1)

data = gs.serialize(game)
json_data = json.loads(data)
json_data['id']=2
game2 = gs.deserialize(json.dumps(json_data))
print(gs.serialize(game2))




