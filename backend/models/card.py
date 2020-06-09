import json
import random


class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{0} of {1}".format(self.rank, self.suit)

    def get_cardId(self):
        return "{0}{1}".format(self.suit[0], self.rank)


class CardSerializer():
    def serialize(self, card):
        json_data = json.dumps(card.__dict__, indent=2)
        return json.loads(json_data)

    def serialize_deck(self, deck):
        json_data = json.dumps(deck, default=lambda o: o.__dict__, indent=4)

        return json.loads(json_data)

    def deserialize_dec(self, json_data):
        deck = Deck(**json.loads(json_data))
        return deck


class Deck():
    def __init__(self, cards=None):
        # cards is a stack of Card's
        if cards == None:
            self.cards = make_deck()
        else:
            self.cards = cards
        self.deck_length = len(self.cards)
    def shuffle(self):
        random.shuffle(self.cards)
    def draw(self):
        if self.deck_length == 0:
            return None
        self.deck_length -=1
        return self.cards.pop()

def make_deck():
    suits = ["Diamonds", "Spades", "Hearts", "Clovers"]
    rank = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = []
    for suite in suits:
        for r in rank:
            deck.append(Card(suite, r))
    return deck
