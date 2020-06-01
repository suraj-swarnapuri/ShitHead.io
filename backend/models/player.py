import json
class Player():
    def __init__(self,user,password=None, hand=None, table=None):
        self.user = user
        self.password = password

        self.hand = hand
        self.table = table
       
class PlayerSerialzer():
    def serialize(self,player):
        if player.table != None:
            player.table.cards = player.table.cards[0:2]
        json_data = json.dumps(player,default=lambda o: o.__dict__,indent=4) 
        return json.loads(json_data)
    def deserialize(self,json_data):
        player = Player(**json.loads(json_data))
        return player