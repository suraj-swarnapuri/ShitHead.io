class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return "{0} of {1}".format(self.rank,self.suit)

def make_deck():
    suits = ["Diamonds","Spades","Hearts","Clovers"]
    rank = ["A","1","2","3","4","5","6","7","8","9","10","J","Q","K"]
    deck = []
    for suite in suits:
        for r in rank:
            deck.append(Card(suite,r))
    return deck