
class Rule():
    """Defines ther rules of the game"""
    def __init__(self) -> None:
        pass

    def get_attributes(self):
        pass

    @staticmethod
    def check_occurrency(values) -> list:
        """
        Conta quante volte è presente l'elemento in una lista.
        """
        counts = []
        for i in range(len(values)):
            counts.append(values.count(values[i]))
        
        return counts


class PokerRules(Rule):
    """Rules for Poker Texas Holdem"""
    CARD_VALUES = list(range(2,11)) + ["Jack", "Queen", "King", "Ace"]
    CARD_SUITS = ["Cuori", "Quadri", "Fiori", "Piove"]
    CARD_SUITS_SIMBOL = [chr(0x2665), chr(0x2666), chr(0x2663), chr(0x2660)]

    def __init__(self) -> None:
        pass

    @staticmethod
    def check_score(hand):
        if len(hand) == 5:
            suits = []
            values = []
            for card in hand:
                suits.append(card.suit)
                values.append(card.value)

            
            is_flush = Rule.check_occurrency(suits)[0] == 5

            values_count = Rule.check_occurrency(values)

            Z = zip(values_count, values, hand)
            sorted_values = sorted(Z, key=lambda t : (t[0], t[1]), reverse=True)

            values = [element for _, element, __ in sorted_values]

            if sorted_values[0][0] == 4:
                score = [7, sorted_values[0][1], sorted_values[-1][1]]
                #print(f"Poker di {sorted_values[0][1]} -> punteggio {score[0]}")

            elif sorted_values[0][0] == 3:
                if sorted_values[-1][0] == 2:
                    score = [6, sorted_values[0][1], sorted_values[-1][1]]
                #    print(f"Full di {sorted_values[0][1]} e {sorted_values[-1][1]} -> punteggio {score[0]}")
                
                else:
                    score = [3, sorted_values[0][1], sorted_values[-2][1], sorted_values[-1][1]]
                #    print(f"Tris di {sorted_values[0][1]} -> punteggio {score[0]}")

            elif sorted_values[0][0] == 2:
                if sorted_values[2][0] == 2:
                    score = [2, sorted_values[0][1], sorted_values[2][1], sorted_values[-1][1]]
                #    print(f"Doppia Coppia di {sorted_values[0][1]} e {sorted_values[2][1]} -> punteggio {score[0]}")
                    
                else:
                    score = [1, sorted_values[0][1], sorted_values[2][1], sorted_values[3][1], sorted_values[4][1]]
                #    print(f"Coppia di {PokerRules.CARD_VALUES[score[1]]} -> punteggio {score[0]}: da {sorted_values[0][2]} e {sorted_values[1][2]}")

            elif PokerRules.check_sequence(values):
                if is_flush:
                    score = [8] + values
                #    print(f"Scala Reale -> punteggio {score[0]}")
                    
                else:
                    #score = [4, sorted_values[0][1], sorted_values[1][1], sorted_values[2][1], sorted_values[3][1], sorted_values[4][1]]
                #    print(f"Scala -> punteggio {score[0]}")
                    score = [4] + values

            elif is_flush:
                #score = [5, sorted_values[0][1], sorted_values[1][1], sorted_values[2][1], sorted_values[3][1], sorted_values[4][1]]
                score = [5] + values
                #print(f"Colore -> punteggio {score[0]}")
            else:
                #score = [0, sorted_values[0][1], sorted_values[1][1], sorted_values[2][1], sorted_values[3][1], sorted_values[4][1]]
                score =  [0] + values
                #print(f"Spera nella carta alta {score[1]} -> punteggio {score[0]}")
            
            
        else:
            raise ValueError("A poker si gioca con 5 carte!")
            
        return score
    
    @staticmethod
    #def check_sequence(values):
    #    values.sort()
    #    i = 1
    #    straigth_value = values[0]
    #    while i < len(values):
    #        straigth_value += 1
    #        if values[i] == straigth_value:
    #            i += 1
    #        elif values[i] == len(PokerRules.CARD_VALUES) -1 and values[0] == 0:
    #            i += 1
    #        else:
    #            return False
    #    return True
    
    @staticmethod
    def check_sequence(values):
        if values[0] == 12:
            values.pop(0)
            values.append(-1)

        i = 1
        is_straight = True        
        straigth_value = values[0]

        while i < len(values) and is_straight:
            straigth_value -= 1
            if values[i] == straigth_value:
                i += 1
            else:
                is_straight = False
                if -1 in values:
                    values.remove(-1)
                    values.insert(0, 12)

        return is_straight
    

if __name__ == "__main__":
    x = [10, 34, 1, -78, -2, 3]

    y = ["peppe", 1, "nope", False, 0, -3]

    #sor = [k for m, k in sorted(zip(y,x))]
    #print(sor)
    Z = zip(x,y)

    z = sorted(zip(x,y))
    print(x)
    print(y)
    x = [element for element, _ in z]
    y = [element for _, element in z]
    print(x)
    print(y)

    