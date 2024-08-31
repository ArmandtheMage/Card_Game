"""Definisce i set di carte in modo che possano essere gestiti"""
import random
from Card import Card

TYPES_OF_SETS = ["free", "stack", "queue"]

class Set_of_Cards():
    """Free set_of_Cards"""
    kind = 0

    def __init__(self, cards: list = [],
                 limit = -1) -> None:
        """
        Crea un 'free' set of cards.
        cards
            sono le carte che rappresentano il set
        limit
            determina un limite alle carte che possono essere in questo set
            -1 non c'è limite
        """
        self.cards = cards
        # ? limiti 0 come set senza limiti
        self.limit = limit

    # ? Chiamarla is_free_space
    def is_addable(self, obj: object):
        """"
        Definisce se obj può essere aggiunto al set, utile per gestire
        il limite della mano successivamente.
        """
        if isinstance(obj, Set_of_Cards) or isinstance(obj, Card):
            if len(self) + len(obj) <= self.limit or self.limit < 0:
                return True
            else:
                return False
        else:
            raise TypeError(f"Unsupported operand {type(obj)} for +")

    def __add__(self, obj: object):
        if self.is_addable(obj):
            if isinstance(obj, Set_of_Cards):
                self.cards.extend(obj.cards)
                return self
            elif isinstance(obj, Card):
                self.cards.append(obj)
                return self
        else:
            raise OverflowError("Non puoi sforare il limite imposto")
        
    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self) -> str: # or repr
        x = ""
        for element in self.cards:
            x += str(element) + ", "
        return x[: -2]
    
    def __len__(self) -> int:
        return len(self.cards)

    @classmethod
    def which_kind(self) -> str:
        return TYPES_OF_SETS[self.kind]

    def __iter__(self):
        return self
    
    def __next__(self):
        # ? valutare se è necessario fare una copia delle carte
        self.cards = self.cards
        if not self.cards:
            raise StopIteration
        else:
            return self.cards.pop(0)
        
    def __getitem__(self, n: int):
        return self.cards[n]
    
    def __contains__(self, obj: object):
        if isinstance(obj, Card):
            return obj in self.cards
        elif isinstance(obj, Set_of_Cards):
            are_in = True
            n = 0
            while are_in and n < len(obj):
                are_in = are_in and (obj[n] in self)
                n += 1
            return are_in

    # ! Non definire __rsub__, la rimozione non è commutativa
    def __sub__(self, obj: object):
        if len(self) > 0:
            if obj in self:
                if isinstance(obj, Set_of_Cards):
                    for card in obj:
                        self.cards.pop(self.cards.index(card))
                    return self
                elif isinstance(obj, Card):
                    self.cards.pop(self.cards.index(obj)) ##### definire una funzione per la ricerca?
                    return self
                else:
                    raise TypeError(f"Non puoi rimuovere {type(obj)} da {self.__class__.__name__}")
            else:
                raise ValueError(f"{str(obj)} non è presente in {self.__class__.__name__}")
        else:
            raise IndexError("Non puoi eliminare carte da un set vuoto")


class CardStack(Set_of_Cards):
    """Stack of Cards, make your piles"""
    kind = 1

    def __init__(self, cards: list = [], limit = -1) -> None:
        """
        Crea un 'stack' set of cards.
        cards
            sono le carte che rappresentano la pila o stack
        limit
            determina un limite alle carte che possono essere in questo set
            -1 non c'è limite
        """
        super().__init__(cards, limit)

    def __add__(self, obj: object):
        if self.is_addable(obj):
            if isinstance(obj, Set_of_Cards):
                obj.cards.extend(self.cards)
                self.cards = obj.cards
                return self
            elif isinstance(obj, Card):
                self.cards.insert(0, obj)
                return self
        else:
            raise OverflowError("Non puoi sforare il limite imposto")
        
    def __sub__(self, obj: object):
        return super().__sub__(obj)

    def take(self, number = 1):
        """"
        Prende carte dalla cima.
        number
            numero di carte da prendere. default 1.
        """
        if len(self) > number:
            card2take = Set_of_Cards()
            for i in range(number): # si potrebbe gestire con lo slicing
                card2take += self.cards.pop(0)
        else:
            raise IndexError("Hai provato a pescare più carte del quante ce ne sono")
        
        return card2take

class Hand(Set_of_Cards):
    def __init__(self, cards: list = [],
                 hand_limit: int = -1,
                 ) -> None:
        """cards
            sono le carte che rappresentano il set
        hand_limit
            numero massimo di carte in mano"""
        super().__init__(cards, hand_limit)


    def reveal(self, rand_or_sub: int | Set_of_Cards = 0):
        if isinstance(rand_or_sub, int) and rand_or_sub == 0 :
            print(self)
        
        elif isinstance(rand_or_sub, int) and\
                0 < rand_or_sub < len(self.cards):
            card2show = Set_of_Cards(random.sample(self.cards, rand_or_sub))
            print(card2show)
        
        elif self.is_playable(rand_or_sub):
            print(rand_or_sub)
        
        else:
            raise TypeError("Provato a rivelare un numero non positivo di carte\
                            o non un 'Set_of_Cards'")


    def old_reveal(self, n_random = -1, subset: Set_of_Cards = Set_of_Cards()):
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
        
        elif n_random == 0 and self.is_playable(subset):
            print(subset)
        
        else:
            print("ERROR: ---")


    def is_playable(self, cards:Set_of_Cards) -> bool: # sostituita da in
        is_playable = True
        n = 0

        if len(self) < len(cards):
            raise IndexError("Stai giocando troppe carte")
        
        while(is_playable and n < len(cards)):
            if cards[n] in self.cards:
                n += 1
            else:
                is_playable = False
        
        return is_playable


if __name__ == "__main__":
    c1 = Card(2, 'Q')
    c2 = Card(4, 'Q')
    c3 = Card(7, 'P')
    c4 = Card('A', 'C')

    s = Set_of_Cards([c2, c1])
    h = Hand([c1, c2, c3], hand_limit=7)
    p = CardStack([c3, c4])

    print(p)
    p += h
    print(f"{p} -> del tipo {type(p)}")
    p -= s
    print(p)
    print(p.take(2))
    print(p)
    h.reveal()
