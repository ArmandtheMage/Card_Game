import random

from Card import Card

SEEDS = ['C', 'Q', 'F', 'P']
CARD_VALUES = list(range(2, 11))
CARD_VALUES.extend(['J', 'Q', 'K', 'A'])

class Deck:
    def __init__(self, card_type:str="Francese"):
        # ? gestirlo in modo differente ?
        if card_type == "Francese":
            self.pile = []
            for seed in SEEDS:
                for value in CARD_VALUES:
                    card = Card(value, seed)
                    self.pile.append(card)
            self.pile.append(Card("Jolly", '*'))
            self.pile.append(Card("Jolly", '*'))
        else:
            self.pile = []
            print(f"{card_type} not supported")
        self.graveyard = []

    def __str__(self):
        string = ""
        if len(self.pile) > 0:
            for card in self.pile:
                string += f"{card}, "
            
            string = string[::-1].replace(',', '~' * 3, 1)
            string = string[::-1]
        else:
            string += '~' * 3

        if len(self.graveyard) > 0:
            string = string[:-1]
            for card in self.graveyard:    
                string += f"{card}, "
                slice_index = -2
        elif string == "~~~":
            slice_index = None
        else:
            return string[:-1]
        
        return string[:slice_index]

    def show(self):
        for i, card in enumerate(self.pile):
            print(f"La carta {i + 1}-esima è: {card}")
        for i, card in enumerate(self.graveyard):
            print(f"La {i + 1}-esima carta degli scarti è: {card}")

    def shuffle(self, full=False):
        if not full:
            self.pile.extend(self.graveyard)
            self.graveyard = []

        random.shuffle(self.pile)
        return self


    def draw(self, n:int, shuffle_when_empty=False,
             jolly_redraw=False) -> list:
        #TODO inserire controllo se si vuole pescare più del mazzo
        if n > 0:
            cards = []
            for i in range(n):
                try:
                    cards.append(self.pile.pop(0))
                except IndexError as e:
                    if shuffle_when_empty:
                        self.shuffle(full=True)
                        cards.append(self.pile.pop(0))
                    else:
                        print("Carte Finite")

                if str(cards[-1]) == "Jolly" and jolly_redraw:
                    print("Estratto un Jolly pesco una carta extra!")
                    cards.append(self.pile.pop(0))
            return cards
        else:
            print("Seleziona un numero positivo!")
        
    def add_graveyard(self, cards:object | list):
        if cards.__class__ == Card:
            cards = [cards]
        for card in cards:
            self.graveyard.insert(0, card)
            #print(f"Scartato {card}")



if __name__ == "__main__":
    prova = Deck("Francese")
    print(prova)
    t = prova.shuffle().draw(20)
    prova.add_graveyard(t)
    print(prova)
    t = prova.shuffle().draw(20)
    prova.add_graveyard(t)
    print(prova)
    t = prova.shuffle().draw(20, True)
    prova.add_graveyard(t)
    print(prova)
