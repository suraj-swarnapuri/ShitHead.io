import random
import json
from card import Deck


class Game():
    def __init__(self,gameid, draw_pile=None,players=[],game_board=[],prev_turn=[] ):
        if not draw_pile:
            self.draw_pile = Deck()
            self.draw_pile.shuffle()
        else:
            self.draw_pile = draw_pile

        self.players = players
        self.game_board = game_board
        self.id = gameid
        self.prev_turn = prev_turn


    def deal_start(self):
        """
        deals the cards for the start of the game
        @return: tuple( hand:3Card deck table: 4 card Deck)
        """
        hand = Deck([])
        table = Deck([])
        for i in range(0,3):
            hand.cards.append(self.draw_pile.draw())
        for i in range(0,4):
            table.cards.append(self.draw_pile.draw())
        return (hand,table)

    def deal(self):
        """
        deals a card if permitted
        @return: None if there are no Cards, a Card off the top of the deck otherwise
        """
        if self.draw_pile.deck_length == 0:
            return None
        return self.draw_pile.draw()

    def join(self,player_user):
        """
        adds a player to the game
        @param: players username
        @return: False if player exists, True otherwise
        """
        if player_user in self.players:
            return False
        self.players.append(player_user)
        return True

    def burn_deck(self):
        """
        gets rid of the current game stack
        """
        self.game_board = []

    def process_turn(self, turn):
        """
        process turn for player
        @param: player_user: the username for the player
        @param: turn: the list of Cards submitted for a players turn
        @return: False if the turn couln't be processed, True otherwise
        """
        if len(turn) == 0:
            return False
        for card in turn:
            self.game_board.append(card)
        player = self.players.pop()
        self.players = [player]+self.players
        if len(self.game_board) >3:
            if self.game_board[-1].rank == self.game_board[-2].rank == self.game_board[-3].rank == self.game_board[-4].rank:
                self.burn_deck()
        return True



class GameSerializer():
    def serialize(self, game):
        """
        turns Game to json
        @param: game - Game object
        @return: json of Game attributes
        """
        json_data = json.dumps(game, default=lambda o: o.__dict__, indent=4)
        return json.loads(json_data)

    def deserialize(self, json_data):
        """
        loads json into Game
        @param: json_data - json of game attributes
        @return: game object
        """
        game = Game(**json.loads(json_data))
        return game


