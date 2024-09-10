import random
import my_card
import sets_card as sets

SEEDS = ['C', 'Q', 'F', 'P']
CARD_VALUES = list(range(2, 11))
CARD_VALUES.extend(['J', 'Q', 'K', 'A'])


class Deck:
    """
    Definisce un mazzo. Il mazzo ha una pila di pesca, una pila degli
    scarti, e definisce.
    """
    # ? capire se game deve esserci oppure creare un erede per gioco
    def __init__(self, game = None) -> None:
        self.pile = sets.CardStack([])
        self.graveyard = sets.CardStack([])

    def __str__(self) -> str:
        return str(self.pile) + "~~~" + str(self.graveyard)
    
    def __len__(self):
        return len(self.pile)
    

    def shuffle(self, full = False):
        """
        Mescola il mazzo.
        full
            booleano che indica se bisogna mescolare anche gli scarti.
            default a 'False'
        """
        if full:
            self.pile += self.graveyard # ricontrollare se da problemi
            self.graveyard.clear()
        random.shuffle(self.pile)
        return self

    # ? mettere un add mode????
    def draw(self, number = 1, shuffle_when_empty = False):
        """
        Funzione che pesca carte dalla cima del mazzo.
        number
            numero di carte da pescare . defaul 1
        shuffle_when_empty
            booleano che indica se in caso il mazzo sia vuoto rimescola
            gli scarti formando una nuova pila degli scarti e continua
            a pescare.
        """
        if number > 0:
            cards_left = 0
            if number > len(self):
                cards_left = number - len(self)
                number = len(self)
            card_drawed = sets.Set_of_Cards([]) # ? mettere un valore di add logic
            card_drawed.draw(self.pile, number)
            if shuffle_when_empty and len(self) == 0: # Non contemplo la possibilità in cui pesco più di tutto il mezzo e anche gli scarti
                if len(self.graveyard) > 0: # ! forse va
                    self.shuffle(True)
                    card_drawed += self.draw(cards_left, shuffle_when_empty)
                else:
                    raise ValueError(cards_left, "Ma sei stronzo a voler pescare tutto il mondo")
            elif not shuffle_when_empty and len(self) == 0:
                print(f"Hai finito il mazzo, dovresti pescare ancora: {cards_left} carte")
            
            return card_drawed
        else:
            raise ValueError("Solo numeri positivi")

    
    def add_graveyard(self, cards: sets.Set_of_Cards | my_card.Card):
        """
        Aggiunge la carta o il set di carte alla pila degli scarti.
        """
        self.graveyard += cards
        cards.clear()
    

class PokerDeck(Deck):
    def __init__(self, game = None) -> None:
        super().__init__(game)
        for value in range(len(my_card.FrenchCard.CARD_VALUES)):
            for suit in range(len(my_card.FrenchCard.SUITS)):
                self.pile += my_card.FrenchCard(value, suit)


class Deck1:  # non buttare draw
    def __init__(self, card_type:str="Francese"):
        # ? gestirlo in modo differente ?
        if card_type == "Francese":
            self.pile = []
            for seed in SEEDS:
                for value in CARD_VALUES:
                    card = my_card.Card(value, seed)
                    self.pile.append(card)
            self.pile.append(my_card.Card("Jolly", '*'))
            self.pile.append(my_card.Card("Jolly", '*'))
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
        if cards.__class__ == my_card:
            cards = [cards]
        for card in cards:
            self.graveyard.insert(0, card)
            #print(f"Scartato {card}")



if __name__ == "__main__":
    prova = PokerDeck()
    print(prova)
    prova.shuffle()
    t = prova.draw(20, True)
    prova.add_graveyard(t)
    print(prova)
    t = prova.draw(20, True)
    prova.add_graveyard(t)
    print(prova)
    t = prova.draw(20, True)
    print(f"\nHo una mano di {len(t)} ed è:\n{t}")
    prova.add_graveyard(t)
    print(prova)
