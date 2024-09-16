import random
import my_card
import sets_card as SoC

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
        self.pile = SoC.CardStack([])
        self.graveyard = SoC.CardStack([])

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
            card_drawed = SoC.Set_of_Cards([]) # ? mettere un valore di add logic
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

    
    def add_graveyard(self, cards: SoC.Set_of_Cards | my_card.Card):
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


if __name__ == "__main__":
    prova = PokerDeck()
    print(prova.pile[0])
    prova.shuffle()
    t = prova.draw(20, True)
    prova.add_graveyard(t)
    print(prova)
    prova.add_graveyard(prova.draw())
    print(f"\n{prova}\n")
    t = prova.draw(20, True)
    prova.add_graveyard(t)
    print(prova)
    t = prova.draw(20, True)
    print(f"\nHo una mano di {len(t)} ed è:\n{t}")
    prova.add_graveyard(t)
    print(prova)
    prova.add_graveyard(prova.draw())
    print(prova)