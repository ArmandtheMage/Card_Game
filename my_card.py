import pyrule


class Card:
    def __init__(self, name:str) -> None:
        self.name = name

    def __str__(self):
        return self.name
        
    def __eq__(self, obj: object) -> bool:
        if self.name == obj.name:
            return True
        else:
            return False
    
    # ! da valutare se va bene o se in futuro potrebbe essere utile
    # ! settato ad uno per le addizioni nei set
    def __len__(self):
        return 1
    
    def copy(self):
        name = self.name
        return Card(name)
    

class FrenchCard(Card, pyrule.PokerRules):
    """
    Carte Francesi, comunemente utilizzate per poker, burraco, etc
    """
    SUITS_REFERENCE = ['Cuori', 'Quadri', 'Fiori', 'Picche']
    SUITS_UNICODE_SIMBOL = [chr(0x2665), chr(0x2666), chr(0x2663), chr(0x2660)]
    # Non necessario nella nuova versione
    SUITS = {}
    for elem in zip(SUITS_REFERENCE, SUITS_UNICODE_SIMBOL):
        SUITS.update({elem[0] : elem[1]})
    
    CARD_VALUES = list(range(2, 11)) + ['Jack', 'Queen', 'King', 'Ace']

    
    # ! Jolly hanno valore -1
    WILD_CARD_VALUE = "Jolly"
    WILD_CARD_SUIT = '*'
        
    def __init__(self, value, suit) -> None:
        # ? gestire la creazione da numero o char invece che solo numero
        self.value = value
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
        return self.value == obj.value and self.suit == obj.suit
    

    def clear(self): # ! check if is good
        self = None

    def copy(self):
        value = self.value
        suit = self.suit
        return FrenchCard(value, suit)

class HieroglypKhepri(Card):
    """
    Carte geroglifico per il gioco Khepri.
    Sono caratterizzate da un colore, un simbolo e un valore di risorsa.
    """
    SIMBOLS = ["Occhio", "Sciacallo", "Falco", "Scarabeo", "Gatto", "Anubi", "Ankh"]
    COLORS = ["Rosso", "Blu", "Giallo", "Verde", "Marrone"]

    def __init__(self, resource, simbol, color) -> None:
        self.resource = resource 
        self.simbol = simbol
        self.color = color
        self.name = self.SIMBOLS[self.simbol] + " " + self.COLORS[color]

    
    def __eq__(self, obj: object) -> bool:
        return self.simbol == obj.simbol and self.color == obj.color
    
    def copy(self):
        return HieroglypKhepri(self.resource, self.simbol, self.color)


class ScribeKhepri(Card):
    """
    Carte scriba per il gioco Khepri.
    Sono caratterizzate da una lista di colori chiamate 'competenze',
    una lista di simboli chiamata 'sequenza', un potere e opzionale
    un simbolo di riferimento
    """
    def __init__(self, competence:list[str], power:int, sequence:list) -> None:
        self.power = power
        self.competence = competence
        self.sequence = sequence
        self.name = ... # TODO lista di poteri e nomi

    def __str__(self):
        return f"Scriba n {self.power}"

if __name__ == "__main__":
    card = FrenchCard(2, 2)
    c1 = FrenchCard(2, 2)
    c2 = FrenchCard(-1, '*')
    print(id(card.CARD_SUITS_SIMBOL))
    print(id(c1))
    print(c1 == card)
    print(c1 == c2)
    #c1 = CardKhepri(2, 'P', 4)
    #c2 = CardKhepri(3, 'P', 4)
    c3 = FrenchCard(0, 3)
    c4 = FrenchCard(0, 1)
    x = [c1, c3, c4]
    for card in x:
        print(card)
    x.sort(key=lambda z: z.value)

    print("###################")
    for card in x:
        print(card)