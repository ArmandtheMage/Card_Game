import my_deck as my_deck
import my_card as my_card
import sets_card as SoC

SEEDS = ['C', 'Q', 'F', 'P']
CARD_VALUES = list(range(2, 11))
CARD_VALUES.extend(['J', 'Q', 'K', 'A'])
WILD_CARD_SEED = '*'
WILD_CARD_VALUE = "Jolly"

class GameEntity:
    """
    Descrive una entità che prende parte al gioco.
    """
    def __init__(self, deck: my_deck.Deck,
                 area: SoC.Set_of_Cards | None) -> None:
        """
        Crea l'entità.
        deck
            mazzo legato all'entità.
        area
            sezione dedicata all'entità.
        """
        self.deck = deck
        self.area = area


class Player(GameEntity):
    """
    Definisce un giocatore.
    """
    id = 0
    def __init__(self, deck: my_deck.Deck,
                 area: SoC.Set_of_Cards | None = SoC.Set_of_Cards([]),
                 nickname: str = "",
                 hand: SoC.Set_of_Cards = SoC.Set_of_Cards([]),
                 initial_score = 0,
                 is_human: bool = True) -> None:
        """
        Creazione del giocatore.
        deck
            mazzo del giocatore o condiviso.
        area
            area dedicata al deploy carte del giocatore.
        nickname
            nome associato al giocatore.
        hand
            set di carte che rappresente le carte.
        initial_score
            punteggio del giocatore, che inizializza 'score'.
        """
        super().__init__(deck, area)
        Player.id += 1
        self.nickname = nickname
        self.hand = hand
        self.score = initial_score
        self.is_human = is_human
        #* da togliere
        self.is_allin = False
        self.jackpot = 0

    @classmethod
    def number_of_player(cls):
        """
        Restituisce il numero di giocatori esistenti.
        """
        return cls.id

    def change_nickname(self, new_name):
        self.nickname = new_name

    def draw_from(self, external_source: SoC.Set_of_Cards | my_card.Card,
                  number: int = 1, mode = None):
        """
        Pesca carte da una fonte esterna.
        """
        self.hand.draw(external_source, number, mode)

class Table(GameEntity):
    def __init__(self, deck: my_deck.Deck, area: SoC.Set_of_Cards) -> None:
        super().__init__(deck, area)

    def draw_from(self, external_source: SoC.Set_of_Cards | my_card.Card,
                  number: int = 1, mode = None):
        """
        Pesca carte da una fonte esterna.
        """
        self.area.draw(external_source, number, mode)

#class Player1:
#    def __init__(self, deck:my_deck.Deck, nickname:str="", initial_score=0) -> None:
#        self.deck = deck
#        self.nickname = nickname
#        self.score = initial_score
#        # TODO hand come classe
#        self.hand = []
#
#    def change_nickname(self, new_name:str):
#        self.nickname = new_name
#
#    def draw_cards(self, n:int=1):
#        drawed = self.deck.draw(n)
#        self.hand.extend(drawed)
#
#    def discard(self, cards:list):
#        self.deck.add_graveyard(cards=cards)
#
#    def play_cards(self, cards:list) -> list:
#        isPlayable = True
#        n = 0
#        while(isPlayable and n < len(cards)):
#            if cards[0] in self.hand:
#                n += 1
#            else:
#                isPlayable = False
#        if isPlayable:
#            check_results(cards)
#            self.discard()
#        else:
#            print("Carte non presenti nella mano")
#
#
#def check_results(played_cards):
#    if len(played_cards) > 1:
#        is_flush = check_flush(played_cards)
#        is_straight = check_straight(played_cards)
#        
#        if is_flush and is_straight:
#            print("Complimenti hai fatto Scala Reale!")
#        elif is_flush:
#            print("Complimenti hai fatto Colore")
#        elif is_straight:
#            print("Complimenti hai fatto Scala")
#        else:
#            print("Spiacente non hai fatto nulla, ritenta la prossima volta")
#
#    else:
#        print(f"Non sono state giocate un numero adatto di carte:"
#              f"gioca almeno 2 carte")
#
#def check_straight(cards:list, circular=True) -> bool:
#    if len(cards) > 14:
#        return False
#    
#    t_cards = cards
#
#    jollys = 0
#    cards_index = []
#
#    for card in t_cards:
#        try:
#            cards_index.append(CARD_VALUES.index(card.value))
#        except ValueError as e:
#            jollys += 1
#    
#    cards_index.sort()
#
#    is_straigth = are_in_line(cards_index, jollys)
#
#    if not is_straigth and (12 in cards_index):
#        cards_index.remove(12)
#        cards_index.insert(0, -1)
#    
#    is_straigth = are_in_line(cards_index, jollys)
#
#    return is_straigth
#    
#def are_in_line(sequence:list, n_wilds:int):
#    previous_value = sequence[0]
#    for i in range(1, len(sequence)):
#        if sequence[i] == previous_value + 1:
#            previous_value += 1
#        elif n_wilds > 0:
#            n_wilds -= 1
#            previous_value += 1
#        else:
#            return False
#    return True
#
#def check_flush(cards) -> bool:
#    is_flush = True
#
#    reference_seed = cards[0].seed
#    n = 1
#
#    while reference_seed == WILD_CARD_SEED and n < len(cards):
#        reference_seed = cards[n].seed
#        n += 1
#
#    if reference_seed != WILD_CARD_SEED:    
#        while(is_flush and n < len(cards)):
#            is_flush = cards[n].seed == reference_seed
#            n += 1
#    
#    return is_flush
#
#
if __name__ == "__main__":
    mazzo = my_deck.PokerDeck()
    p1 = Player(mazzo)
    p2 = Player(mazzo)

    print(Player.number_of_player())