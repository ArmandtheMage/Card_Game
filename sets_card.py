"""Definisce i set di carte in modo che possano essere gestiti"""
import random
from Card import Card

TYPES_OF_SETS = ["free", "stack", "queue"]

class Set_of_Cards():
    def __init__(self, cards: list = [],
                 typeofset: int = 0) -> None:
        """cards\n
            sono le carte che rappresentano il set
        typeofset\n
            0 -> 'free' per non avere vincoli, 1 -> 'stack' definisce
            una logica filo, 2 -> 'queue' una logica fifo
        """
        self.cards = cards
        self.type = typeofset
        
    def add(self, card:Card):
        self.cards.append(card)


    def __str__(self) -> str: # or repr
        x = ""
        for element in self.cards:
            x += str(element) + ", "
        return x[: -2]
    
    def __len__(self):
        return len(self.cards)


class Hand(Set_of_Cards):
    def __init__(self, cards: list = [],
                 hand_limit: int = -1,
                 typeofset: int = 0,
                 ) -> None:
        """cards
            sono le carte che rappresentano il set
        typeofset
            0 -> 'free' per non avere vincoli, 1 -> 'stack' definisce
            una logica filo, 2 -> 'queue' una logica fifo
        hand_limit
            numero massimo di carte"""
        super().__init__(cards, typeofset)
        self.limit = hand_limit

    def reveal2(self, rand_or_sub: int |Set_of_Cards = 0):
        if type(rand_or_sub) == int and rand_or_sub == 0 :
            print(self)
        
        elif type(rand_or_sub) == int and 0 < rand_or_sub < len(self.cards):
            card2show = Set_of_Cards(random.sample(self.cards, rand_or_sub))
            print(card2show)
        
        elif self.isPlayable(rand_or_sub):
            print(rand_or_sub)
        
        else:
            # TODO sostituire con un raise
            print("ERROR: ---")


    def reveal(self, n_random = -1, subset: Set_of_Cards = Set_of_Cards()):
    
        """Reveal cards from the hand
        
        n_random
            -1 ---> show the hand
            0 ---> show the input 'subset'
            n > 0 ---> show n random card in the hand
        subset
            a 'Set_of_Cards' to show if random is 0
        """

        if n_random < 0:
            print(self)
        
        elif 0 < n_random < len(self.cards):
            card2show = Set_of_Cards(random.sample(self.cards, n_random))
            print(card2show)
        
        elif n_random == 0 and self.isPlayable(subset):
            print(subset)
        
        else:
            # TODO sostituire con un raise
            print("ERROR: ---")

    # ? cards as Set_of_Cards
    def isPlayable(self, cards:Set_of_Cards) -> bool:
        isPlayable = True
        n = 0
        if len(self) < len(cards):
            print("Stai giocando troppe carte")
            return False
        while(isPlayable and n < len(cards.cards)):
            if cards.cards[n] in self.cards:
                n += 1
            else:
                isPlayable = False
        
        return isPlayable


if __name__ == "__main__":
    c1 = Card(2, 'Q')
    c2 = Card(4, 'Q')
    c3 = Card(7, 'P')
    c4 = Card('A', 'C')

    s = Set_of_Cards([c1, c2], 2)
    h = Hand([c1, c2, c3], 7)

    h.isPlayable(s)
    h.reveal2(0)
