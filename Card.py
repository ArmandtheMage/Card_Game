class Card:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self):
        if self.suit == '*':
            return self.value
        else:
            return str(self.value)
        
    def __eq__(self, obj: object) -> bool:
        if self.value == obj.value:
            return True
        else:
            return False
    
    # ! da valutare se va bene o se in futuro potrebbe essere utile
    # settato ad uno per le addizioni nei set
    def __len__(self):
        return 1
    

class FrenchCard(Card):
    """
    Carte Francesi, comunemente utilizzate per poker, burraco, etc
    """
    SUITS_REFERENCE = ['Cuori', 'Quadri', 'Fiori', 'Picche']
    SUITS_UNICODE_SIMBOL = [chr(0x2665), chr(0x2666), chr(0x2663), chr(0x2660)]
    # Non necessario nella nuova versione
    SUITS = {}
    for elem in zip(SUITS_REFERENCE, SUITS_UNICODE_SIMBOL):
        SUITS.update({elem[0] : elem[1]})

    CARD_VALUES = list(range(2, 11)) + ['J', 'Q', 'K', 'A']
    
    # ! Jolly hanno valore -1
    WILD_CARD_VALUE = "Jolly"
    WILD_CARD_SUIT = '*'
        
    def __init__(self, value, suit) -> None:
        super().__init__(value)
        # ? gestire la creazione da numero o char invece che solo numero
        self.suit = suit
        if self.value < 0:
            self.name = self.WILD_CARD_VALUE
        else:
            self.name = str(self.CARD_VALUES[self.value]) +\
                    " di " + self.SUITS_REFERENCE[self.suit]
        
    def __str__(self):
        if self.value < 0:
            return self.WILD_CARD_VALUE
        else:
            return str(self.CARD_VALUES[self.value]) + self.SUITS_UNICODE_SIMBOL[self.suit]
        
    def __eq__(self, obj: object) -> bool:
        return super().__eq__(obj) and self.suit == obj.suit
    

class Hieroglyp_Khepri(Card):
    """
    Carte geroglifico per il gioco Khepri.
    Sono caratterizzate da un colore, un simbolo e un valore di risorsa.
    """
    SIMBOLS = ["Occhio", "Sciacallo", "Falco", "Scarabeo", "Gatto", "Anubi", "Ankh"]
    COLORS = ["Rosso", "Blu", "Giallo", "Verde", "Marrone"]

    def __init__(self, value, simbol, color) -> None:
        super().__init__(value)
        self.simbol = simbol
        self.color = color

    def __str__(self):
        return self.SIMBOLS[self.simbol] + " " + self.COLORS[self.color]
    
    def __eq__(self, obj: object) -> bool:
        return self.simbol == obj.simbol and self.color == obj.color


class Scribe_Khepri(Card):
    """
    Carte scriba per il gioco Khepri.
    Sono caratterizzate da una lista di colori chiamate 'competenze',
    una lista di simboli chiamata 'sequenza', un potere e opzionale
    un simbolo di riferimento
    """
    def __init__(self, value, competence:list[str], sequence:list) -> None:
        super().__init__(value) # value = power
        self.competence = competence
        self.sequence = sequence
        
        

if __name__ == "__main__":
    card = FrenchCard(2, 2)
    c1 = FrenchCard(2, 2)
    c2 = FrenchCard(-1, '*')
    print(card)
    print(c1)
    print(c1 == card)
    print(c1 == c2)
    #c1 = CardKhepri(2, 'P', 4)
    #c2 = CardKhepri(3, 'P', 4)
