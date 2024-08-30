

SUITS_REFERENCE = ['C', 'Q', 'F', 'P']
SUITS_UNICODE_SIMBOL = [chr(0x2665), chr(0x2666), chr(0x2663), chr(0x2660)]
SUITS = {}
for elem in zip(SUITS_REFERENCE, SUITS_UNICODE_SIMBOL):
    #SUITS[element[0]] = element[1]
    SUITS.update({elem[0] : elem[1]})
CARD_VALUES = list(range(2, 11))
CARD_VALUES.extend(['J', 'Q', 'K', 'A'])
WILD_CARD_SEED = '*'
WILD_CARD_VALUE = "Jolly"

class Card:
    def __init__(self, value, suit) -> None:
        self.value = value
        self.suit = suit

    def __str__(self):
        if self.suit == '*':
            return self.value
        else:
            suit = SUITS[self.suit]
            return str(self.value) + suit
        
    def __eq__(self, value: object) -> bool:
        if self.value == value.value and self.suit == value.suit:
            return True
        else:
            return False
        
class Hand:
    def __init__(self, initial_hand=[], hand_limit:int=-1) -> None:
        self.limit = hand_limit
        self.cards = initial_hand
    
    def reveal(self, subset:list, random:int=0):
        if random == 0:
            for card in self.cards:
                print(card)
        elif random > 0:
            ...
        else:
            print("Valore random non settato correttamente")

    def add_cards(self, cards:list):
        self.cards.exted(cards)

    def is_playable(self, cards:list):
        isPlayable = True
        n = 0

        while(isPlayable and n < len(cards)):
            if cards[0] in self.hand:
                n += 1
            else:
                isPlayable = False
        
        return isPlayable
    
if __name__ == "__main__":
    card = Card(2,'P')
    print(card)
