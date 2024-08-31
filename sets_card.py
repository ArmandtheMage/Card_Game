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
        self.loop_index = 0
        # ? inserire un parametro per la visibilità

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
                self.cards = self.cards + obj.cards
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
        return x[:-2]
    
    def __len__(self) -> int:
        return len(self.cards)

    @classmethod
    def which_kind(self) -> str:
        return TYPES_OF_SETS[self.kind]

    def __iter__(self):
        self.loop_index = 0
        return self
    
    def __next__(self):
        try:
            item = self.cards[self.loop_index]
            self.loop_index += 1
            return item
        except IndexError:
            raise StopIteration
 
    def __getitem__(self, n):
        if isinstance(n, slice):
            cards2return = Set_of_Cards()
            
            if n.start == None:
                sta = 0
            elif n.start < 0 :
                sta = len(self) + n.start
            else:
                sta = n.start

            if n.stop == None:
                sto = len(self)
            elif n.stop < 0:
                sto = len(self) + n.stop
            else:
                sto = n.stop

            if n.step == None:
                ste = 1
            else:
                ste = n.step

            cards2return.cards = []
            for i in range(sta, sto, ste):
                item = self.cards[i]
                cards2return += item
            return cards2return
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


    def reveal(self, rand_or_sub = 0):
        """
        Rivela carte.

        rand_or_sub
            Se è un numero positivo rivela quel numero di carte a caso dalla
            mano. Se è 0 rivela la mano. Se è un 'Set_of_Cards' nel caso sia
            presente nella mano lo rivela. default = 0
        """
        if isinstance(rand_or_sub, int):
            if rand_or_sub == 0:
                print(self)
            elif 0 < rand_or_sub < len(self.cards):
                card2show = Set_of_Cards(random.sample(self.cards, rand_or_sub))
                print(card2show)
            else:
                raise ValueError("Provato a rivelare un numero non positivo di carte")
        elif isinstance(rand_or_sub, Set_of_Cards) or isinstance(rand_or_sub, Card):
            if rand_or_sub in self:
                print(rand_or_sub)
            else:
                # ? raise error
                print("Carta o set di carte non trovato")
        else:
            raise TypeError(f"Provato a rivelare {type(rand_or_sub)} da un {self.__class__.__name__}")

    def draw(self, number = 1, mode:int = 1):
        """
        Recupera carte dal set di carte.

        number
            numero di carte da pescare.
        mode
            modalità di pesca: 1 dal primo elemento, -1 dall'ultimo,
            0 in maniera randomica
        """
        if 0 < number <= len(self):
            card2draw = Set_of_Cards([]) # il default gli da problemi
            if mode == 1:
                for i in range(number):
                    card2draw += self.cards.pop(0)
            elif mode == 0:
                card2draw = Set_of_Cards(random.sample(self.cards, number))
                for card in card2draw:
                    self.cards.remove(card)
            elif mode == -1:
                for i in range(number):
                    card2draw += self.cards.pop()
            else:
                raise ValueError(mode, "Modalità selezionata non gestita")
        else:
            raise IndexError("Provato a pescare più carte di quante ne hai")
        
        return card2draw
            
    def index(self, cards):
        if cards in self:
            if isinstance(cards, Card):
                return self.cards.index(cards)
            elif isinstance(Set_of_Cards):
                index = []
                for card in cards:
                    index.append(self.cards.index(card))
            else:
                raise TypeError("Tipo non riconosciuto")
        else:
            raise ValueError(f"{cards} non presenti")
        

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
                self.cards = obj.cards + self.cards
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
        #if len(self) > number:
        #    card2take = Set_of_Cards(self[:number])
        #else:
        #    raise IndexError("Hai provato a pescare più carte del quante ce ne sono")
        #
        #return card2take
        return self.draw(number=number, mode=1)

class Hand(Set_of_Cards): # probabilmente gestita da gioco
    def __init__(self, cards: list = [],
                 hand_limit: int = -1,
                 ) -> None:
        """cards
            sono le carte che rappresentano il set
        hand_limit
            numero massimo di carte in mano"""
        super().__init__(cards, hand_limit)


    def is_playable(self, cards:Set_of_Cards | Card) -> bool: # sostituita da in
        #is_playable = True
        #n = 0
#
        if len(self) < len(cards):
            raise IndexError("Stai giocando troppe carte")
        #
        #while(is_playable and n < len(cards)):
        #    if cards[n] in self.cards:
        #        n += 1
        #    else:
        #        is_playable = False
        #
        #return is_playable
        
        return cards in self


class CardQueue(Set_of_Cards):
    """Queue of Cards, make your queue"""
    kind = 2

    def __init__(self, cards: list = [], limit = -1) -> None:
        """
        Crea una 'queue' set of cards.
        cards
            sono le carte che rappresentano la coda o queue
        limit
            determina un limite alle carte che possono essere in questo set
            -1 non c'è limite
        """
        super().__init__(cards, limit)
        
    def __sub__(self, obj: object):
        return super().__sub__(obj)


    def take(self, number = 1):
        """"
        Prende carte dalle prime aggiunte, quindi le più vecchie e a sx.
        number
            numero di carte da prendere. default 1.
        """
        return self.draw(number=number, mode=1)


if __name__ == "__main__":
    c1 = Card(2, 'Q')
    c2 = Card(4, 'Q')
    c3 = Card(7, 'P')
    c4 = Card('A', 'C')

    s = Set_of_Cards([c2, c1])
    h = Hand([c1, c2, c3], hand_limit=7)
    p = CardStack([c3, c4])
    q = CardQueue([c4, c3, c1, c4, c2, c2])

    #h.reveal(p)
    q += h
    q += c1
    t = Set_of_Cards()
    print(f"hand: {h}\ntest: {t}\nqueue: {q}\n\n")
    mode = 0
    t = q.take(2)
    print(f"hand: {h}\ntest: {t}\nqueue: {q}\n\n")
    x = q.take(3)
    t = x
    print(f"hand: {h}\ntest: {t}\nqueue: {q}\n\nx: {x}")
    q -= s
    print(f"hand: {h}\ntest: {t}\nqueue: {q}\n\ns: {s}")
