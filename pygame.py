import my_player
import my_deck
import pyrule

class Game:
    def __init__(self, number_player, rules: list | pyrule.Rule) -> None:
        self.rules = rules
        self.n_player = number_player

    def play(self):
        pass


class Poker(Game):
    def __init__(self):
        pass