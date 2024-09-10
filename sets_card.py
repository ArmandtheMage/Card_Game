"""Definisce i set di carte in modo che possano essere gestiti"""
import random
import my_card
#import stackcard as sc

TYPES_OF_SETS = ["free", "stack", "queue"]

#### ! l'addizione va bene anche a più fattori
#### ! il += solo 1
#### ! per ora l'add_mode non è utilizzato perchè ogni classe specializza il suo add
class Set_of_Cards():
    """Free set_of_Cards"""
    kind = 0

    def __init__(self, cards: list[my_card.Card] = [],
                 limit = -1, draw_logic:int = 0,
                 add_mode = -1, remove_mode = 1) -> None:
        """
        Crea un 'free' set of cards.
        cards
            sono le carte che rappresentano il set
        limit
            determina un limite alle carte che possono essere in questo set
            -1 non c'è limite
        draw_logic
            determina la logica di gestione di limite di mano quando
            si pescano carte. 0 pesca fino a riempire il set. 1 pesca
            ignorando il limite, questo implica che deve ci dovrà essere
            un controllo dopo. -1 non pescare se superi il limite.
        add_mode & remove_mode
            determina dove aggiunge o toglie carte: 1 dal primo elemento,
            -1 dall'ultimo, 0 (solo remove) in maniera randomica.
            default add -1, remove 1. -> aggiungo in coda prendo dalla testa.
        """
        self.cards = cards
        # ? limiti 0 come set senza limiti
        self.limit = limit
        self.loop_index = 0
        self.draw_logic = draw_logic
        self.add_mode = add_mode
        self.remove_mode = remove_mode
        # ? inserire un parametro per la visibilità
    
    def __add__(self, obj: object):
        if isinstance(obj, my_card.Card) :
            drawable = self.how_many_add(1)
            if drawable > 0:
                self.cards.append(obj)
        
        elif isinstance(obj, Set_of_Cards):
            drawable = self.how_many_add(len(obj))
            self.cards += obj.cards[:drawable]
        else:
            raise TypeError("Solo carte o set")
        return self

    def __radd__(self, other):
        #x = Set_of_Cards(self.cards, self.limit, self.draw_logic)
        #return x.__add__(other)
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

    def same_type(self):
        return Set_of_Cards([], self.limit, self.draw_logic,
                            self.add_mode, self.remove_mode)

    def __getitem__(self, n):
        if isinstance(n, slice):
            cards2return = self.same_type()
            
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
                if ste < 0:
                    tmp = sta
                    sta = sto -1
                    sto = tmp -1

            for i in range(sta, sto, ste):
                item = self.cards[i]
                cards2return += item
            return cards2return 
        return self.cards[n]
    
# * Set Item fa quello che vuoi ma solo su attributi
    def __setitem__(self, idx, obj):
        if isinstance(obj, my_card.Card):
            x = obj.copy()
            self.cards[idx] = x
        else:
            raise TypeError("Only Cards can be assigned to set of cards")

    def __contains__(self, obj: object):
        if isinstance(obj, my_card.Card):
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
                #* considerare
                #if self.default_mode == -1:
                #    self.cards = self.cards[::-1]
                if isinstance(obj, Set_of_Cards):
                    for card in obj:
                        self.cards.pop(self.cards.index(card))
                elif isinstance(obj, my_card.Card):
                    self.cards.pop(self.cards.index(obj))
                else:
                    raise TypeError(f"Non puoi rimuovere {type(obj)} da {self.__class__.__name__}")
                #if self.default_mode == -1:
                #    self.cards = self.cards[::-1]
                return self
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
        elif isinstance(rand_or_sub, Set_of_Cards) or isinstance(rand_or_sub, my_card.Card):
            if rand_or_sub in self:
                print(rand_or_sub)
            else:
                # ? raise error
                print("Carta o set di carte non trovato")
        else:
            raise TypeError(f"Provato a rivelare {type(rand_or_sub)} da un {self.__class__.__name__}")

    # ! da eliminare
    def has_free_space(self, obj: object):
        """"
        Definisce se obj può essere aggiunto al set, utile per gestire
        il limite della mano successivamente.
        """
        if isinstance(obj, Set_of_Cards) or isinstance(obj, my_card.Card):
            drawable_card = len(self) + len(obj) - self.limit
            if drawable_card > 0 or self.limit < 0:
                return True
            else:
                if drawable_card < 0:
                    drawable_card = 0
                raise ValueError(drawable_card, "Non hai abbastanza spazio")
        else:
            raise TypeError(f"Unsupported operand {type(obj)} for +")

    def how_many_add(self, number) -> int:
        """
        definisce se posso aggiungere delle carte al mio set,
        in caso contrario ritorna il numero massimo.
        """
        if number > 0:
            free_space = self.limit - len(self)
            if self.draw_logic == 1 or free_space >= number or self.limit < 0:
                return number
            elif self.draw_logic == 0:
                return free_space
            elif self.draw_logic == -1:
                return 0
            else:
                raise TypeError("Tipo o valore non corretto")
        else:
            raise ValueError("Non puoi aggiungere un numero negativo di carte")


    def get_cards(self, number: int, mode = None):
        """
        Recupera una copia delle carte dal set di carte.

        number
            numero di carte da pescare.
        mode
            modalità di pesca: 1 dal primo elemento, -1 dall'ultimo,
            0 in maniera randomica
        """
        if 0 < number <= len(self):
            if mode == None:
                mode = self.remove_mode

            if number > 1:
                if mode == 1:
                    card2draw = Set_of_Cards(self.cards[:number])

                elif mode == 0:
                    card2draw = Set_of_Cards(random.sample(self.cards, number))
                
                elif mode == -1:
                    card2draw = Set_of_Cards(self.cards[-number:])
                
                else:
                    raise TypeError(mode, "Modalità selezionata non gestita")
                return card2draw
            else:
                if mode == 1:
                    card2draw = self[0]
                elif mode == 0:
                    card2draw = self[random.randint(0, len(self) -1)]
                else:
                    card2draw = self[-1]
        else:
            if number > 0:
                raise ValueError(len(self), "Vuoi più carte di quante ne hai")
            

    def draw(self, target, number: int = 1, mode = None):
        """
        Pesca carte da un bersaglio e le aggiunge a se stesso.
        target
            card o Set of Cards bersaglio da cui pescare le carte.
        number
            numero di carte da pescare. default 1
        mode
            modalità di pesca: 1 dal primo elemento, -1 dall'ultimo,
            0 in maniera randomica. default 'None'
            Nota: sovrascrive le logiche se indicata
        """
        drawable_card = self.how_many_add(number)
        
        if drawable_card > 0:
            if mode == None:
                remove_mode = target.remove_mode
            else:
                remove_mode = mode
            try:
                card2draw = target.get_cards(drawable_card, remove_mode)
            except ValueError as e:
                drawable_card = e.args[0]
                card2draw = target.get_cards(drawable_card, remove_mode)
                print("Pesco fino a consumare il target")
            
            # ? fare una funzione che gira il set di carte
            # * adesso si può scrivere anche: target = targhet[::-1]
            if mode != self.add_mode and self.add_mode == 1:
                self.cards = self.cards[::-1]
                print("override the draw")
            self += card2draw

            if mode != self.add_mode and self.add_mode == 1:
                self.cards = self.cards[::-1]

            # ? Considerare se inserirlo nella sub 
            if remove_mode == -1:
                target.cards = target.cards[::-1]

            target -= card2draw
            
            if remove_mode == -1:
                target.cards = target.cards[::-1]


    def index(self, cards) -> int | list[int]:
        """
        Recupera l'indice della carta o una lista di indici.
        card
            un selemento di tipo 'Card' o 'Set_of_card'
        """
        if isinstance(cards, list):
            cards = Set_of_Cards(cards)
        if cards in self:
            if isinstance(cards, my_card.Card):
                return self.cards.index(cards)
            elif isinstance(cards, Set_of_Cards):
                index = []
                for card in cards:
                    index.append(self.cards.index(card))
                return index
            else:
                raise TypeError("Tipo non riconosciuto")
        else:
            raise ValueError(f"{cards} non presenti")
        
    def clear(self):
        self.cards.clear()
    
    def revert(self):
        return self[::-1] # ? fare una copia


class CardStack(Set_of_Cards):
    """Stack of Cards, make your piles"""
    kind = 1

    def __init__(self, cards: list = [], limit = -1, draw_logic = 1) -> None:
        """
        Crea un 'stack' set of cards.
        cards
            sono le carte che rappresentano la pila o stack.
        limit
            determina un limite alle carte che possono essere in questo set
            -1 non c'è limite.
        draw_logic
            determina la logica di gestione di limite di mano quando
            si pescano carte. 0 pesca fino a riempire il set. 1 pesca
            ignorando il limite, questo implica che deve ci dovrà essere
            un controllo dopo. -1 non pescare se superi il limite.
        """
        super().__init__(cards, limit, draw_logic, add_mode=1, remove_mode=1)

    def same_type(self):
        return CardStack([], self.limit, self.draw_logic)

    def __add__(self, obj: object):
        """
        Aggiunge in testa, nelle posizioni iniziali
        """
        if isinstance(obj, my_card.Card) :
            drawable = self.how_many_add(1)
            if drawable > 0:
                self.cards.insert(0, obj)
        
        elif isinstance(obj, Set_of_Cards):
            drawable = self.how_many_add(len(obj))
            # ? da valutare se aggiungere [::-1]
            self.cards = obj.cards[:drawable] + self.cards
        else:
            raise TypeError("Solo carte o set")
        return self

    def draw(self, target, number: int = 1):
        """
        Pesca carte da un bersaglio e le aggiunge a se stesso.
        target
            card o Set of Cards bersaglio da cui pescare le carte.
        number
            numero di carte da pescare. default 1
        mode
            modalità di pesca: 1 dal primo elemento, -1 dall'ultimo,
            0 in maniera randomica. default 1
        """
        return super().draw(target, number)

# ! Da rifare Hand
class Hand(Set_of_Cards): # probabilmente gestita da gioco
    def __init__(self, cards: list = [],
                 hand_limit: int = -1,
                 draw_logic:int = 0
                 ) -> None:
        """cards
            sono le carte che rappresentano il set
        hand_limit
            numero massimo di carte in mano"""
        super().__init__(cards, hand_limit, draw_logic)


    def is_playable(self, cards:Set_of_Cards | my_card.Card) -> bool: # sostituita da in
        if len(self) < len(cards):
            raise IndexError("Stai giocando troppe carte")
        return cards in self


class CardQueue(Set_of_Cards):
    """Queue of Cards, make your queue"""
    kind = 2

    def __init__(self, cards: list = [], limit = -1, draw_logic = 1, default_mode = 0) -> None:
        """
        Crea una 'queue' set of cards.
        cards
            sono le carte che rappresentano la coda o queue.
        limit
            determina un limite alle carte che possono essere in questo set
            -1 non c'è limite.
        draw_logic
            determina la logica di gestione di limite di mano quando
            si pescano carte. 0 pesca fino a riempire il set. 1 pesca
            ignorando il limite, questo implica che deve ci dovrà essere
            un controllo dopo. -1 non pescare se superi il limite.
        """
        super().__init__(cards, limit, draw_logic,
                         add_mode=-1, remove_mode=1)

    def same_type(self):
        return CardQueue([], self.limit, self.draw_logic, self.default_mode)

    def draw(self, target, number: int = 1):
        """
        Pesca carte da un bersaglio e le aggiunge a se stesso.
        target
            card o Set of Cards bersaglio da cui pescare le carte.
        number
            numero di carte da pescare. default 1
        mode
            modalità di pesca: 1 dal primo elemento, -1 dall'ultimo,
            0 in maniera randomica. default 1
        """
        return super().draw(target, number)


if __name__ == "__main__":
    c1 = my_card.FrenchCard(2, 1)
    c2 = my_card.FrenchCard(4, 1)
    c3 = my_card.FrenchCard(7, 3)
    c4 = my_card.FrenchCard(12, 0)
    c5 = my_card.FrenchCard(8, 2)
    c6 = my_card.HieroglypKhepri(4, 4, 3)

    s = Set_of_Cards([c2, c1])
    h = Set_of_Cards([c1, c2, c3], limit=7, draw_logic=1)
    p = CardStack([c3, c4])
    q = CardQueue([c4, c3, c1, c4, c2, c2])

    print(f"h:{h}")
    print(f"q:{q}")
    print(f"s:{s}")
    p = p +q + h + s
    s[1] = c5
    print()
    print(f"h:{h}")
    print(f"s:{s}")
    print(f"q:{q}")
    p = p + s + c4
    h[2] = c6
    print()
    print(f"h:{h}")
    print(f"q:{q}")
    print(f"s:{s}")

    x = Set_of_Cards([], limit=9, draw_logic=1)
    print(f"#################\n# draw_logic: {x.draw_logic} #\n#################")
    print(f"q: {q}")
    print(f"x: {x}")
    print()
    x.draw(p, 3)
    print(f"q: {q}")
    print(f"x: {x}")
    x.draw(p, 5, 0)
    print()
    print(f"q: {q}")
    print(f"x: {x}")
    x.draw(p, 2)
    print()
    print(f"q: {q}")
    print(f"x: {x}")
