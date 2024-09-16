import my_player
import my_deck
import pyrule
import sets_card
import random
from itertools import combinations
import my_card

class Game:
    def __init__(self, number_player, rules: list | pyrule.Rule = None) -> None:
        self.rules = rules
        self.n_player = number_player

    def play(self):
        pass


class Poker(Game):
    initial_bet = 100
    SCORE = ["Carta alta",      #0
             "Coppia",          #1
             "Doppia Coppia",   #2
             "Tris",            #3
             "Scala",           #4
             "Colore",          #5
             "Full",            #6
             "Poker",           #7
             "Scala Reale"]     #8
    
    def __init__(self, number_player, rules = None):
        super().__init__(number_player, rules)
        self.deck = my_deck.PokerDeck()
        Poker.table = my_player.Table(self.deck, sets_card.Set_of_Cards([], 5, -1))
        self.players: list[my_player.Player] = []
        self.current_round = 0
        
        for i in range(self.n_player):
            dummy_name = "Giocatore_" + str(i +1)
            self.players.append(my_player.Player(self.deck, area=None,
                                                 nickname=dummy_name,
                                                 hand=sets_card.Set_of_Cards([], 2, 0),
                                                 initial_score=10000))
        
        
        self.current_dealer = random.randint(0, self.n_player -1)
        self.jackpot = 0
        self.players_allin = []

    def puntata(self):
        #players_in_game = [True for x in range(0, self.n_player)]
        #bets = [0 if x else -1 for x in players_in_game]
        bets = [0 for x in range(self.n_player)]

        if self.current_round == 0:
            # ! cambiare n_player
            talk_idx = (self.current_dealer + 3) % (self.n_player)
            bets[(self.current_dealer + 1) % (self.n_player)] = self.initial_bet // 2
            bets[(self.current_dealer + 2) % (self.n_player)] = self.initial_bet
            max_bet = self.initial_bet
            da_pagare = True
        else:
            talk_idx = ((self.current_dealer + 1) % (self.n_player))
            max_bet = 0
            da_pagare = False

        call_count = 0
        fould_count = 0
        

        while call_count + fould_count < self.n_player:
            #scegli quanto puntare
            # 3 possibilità 0, -1, > 0
            if bets[talk_idx] < 0: #giocatore in fould
                talk_idx = (talk_idx + 1) % self.n_player
                continue
            
            player: my_player.Player = self.players[talk_idx]
            print(f"è il turno del {player.nickname} che è il {talk_idx} al tavolo")
            
            if player.is_allin:
                call_count += 1
                print(f"{player.nickname} è all in")
                continue

            if da_pagare:
                if talk_idx == (self.current_dealer + 1) % (self.n_player):
                    print(f"Sei lo small blind hai già pagato {bets[talk_idx]}")
                    self.jackpot += bets[talk_idx]
                    player.score -= bets[talk_idx]
                    player.jackpot = bets[talk_idx]
                elif talk_idx == (self.current_dealer + 2) % (self.n_player):
                    print(f"Sei il big blind hai già pagato {bets[talk_idx]}")
                    self.jackpot += bets[talk_idx]
                    player.score -= bets[talk_idx]
                    player.jackpot = bets[talk_idx]
                    da_pagare = False

            if player.is_human:
                print(f"{player.nickname} decidi quanto puntare.\
                      \nHai a disposizione {player.score}\
                      \nLa puntata attuale è {max_bet} - Puntata minima {Poker.initial_bet}")
                choise = int(input("0 per call, -1 per fold, *valore* per puntare: "))
                if choise > 0:
                    choise = choise // self.initial_bet * self.initial_bet
            else:
                print(f"{player.nickname} decide quanto puntare.\
                      \nHa a disposizione {player.score}")
                extract = random.randint(1,10)
                if 5 < extract < 9:
                    choise = (extract - 5) * self.initial_bet * random.randint(1, 5)
                elif 8 < extract < 11:
                    choise = -1
                else:
                    choise = 0

            #if choise == -1:
            #    print(f"{player.nickname}: Fould -> discart the cards")
            #    bets[talk_idx] = -1
            #    fould_count += 1
            #    player.deck.add_graveyard(player.hand)
            #    # ? da eliminare
            #    players_in_game[talk_idx] = False
            #elif choise == 0:
            #    if max_bet == 0:
            #        print(f"{player.nickname}: busso o Check -> vede la giocata")
            #        
            #    else:
            #        print(f"{player.nickname}: Call -> segue la giocata")
            #        relative_bet = max_bet - bets[talk_idx] # vedi quanto manca per pareggiare
#
            #        if relative_bet > player.score: # questo non dovrebbe essere consentito dalle regole
            #            print(f"{player.nickname} è all in!")
            #            player.is_allin = True # parametro per skip
            #            bet = player.score + bets[talk_idx] # puntata di riferimento
            #            #aggiorno nel caso ci sono persone all_in 
            #            # ! riscrivere eliminando bet
            #            for p_all_in in self.players_allin:
            #                relative_allin_bet = bet - p_all_in[1]
            #                if relative_allin_bet > 0: # sto puntando di più del tizio all_in
            #                    p_all_in[2] += relative_allin_bet
            #                else:
            #                    p_all_in[2] += (bet - bets[talk_idx]) # metto il mio score
            #            #aggiungo me stesso ai giocatori all_in
            #            self.players_allin.append([talk_idx, bet, self.jackpot + player.score])
            #            self.jackpot += player.score
            #            
            #            bets[talk_idx] += player.score
            #            
            #            player.score = 0
            #            
            #        else:
            #            for p_all_in in self.players_allin:
            #                p_all_in[2] += p_all_in[1] - bets[talk_idx]
#
            #            player.score -= relative_bet
            #            self.jackpot += relative_bet
            #        
            #            bets[talk_idx] = max_bet
            #    
            #    call_count += 1
            #else:
            #    print(f"{player.nickname}: Raise -> {choise}")
            #    relative_bet = max_bet - bets[talk_idx] # quanto mancava da dare
            #    if choise + relative_bet > player.score:
            #        print(f"{player.nickname} è all in!")
            #        player.is_allin = True
            #        # ! relative_bet + player.score non va bene 
            #        for p_all_in in self.players_allin:
            #            if relative_bet + player.score > p_all_in[1]:
            #                p_all_in[2] += p_all_in[1] - bets[talk_idx] # ci potrebbe essere un caso in cui è negativa?
            #            else:
            #                p_all_in[2] += relative_bet + player.score
#
            #        self.players_allin.append([talk_idx, relative_bet + player.score, self.jackpot + relative_bet + player.score])
            #        self.jackpot += player.score
            #        player.score = 0
            #        
            #        
            #    else:
            #        player.score -= (choise + relative_bet)
            #        self.jackpot += choise + relative_bet
#
            #    max_bet = bets[talk_idx] + choise +relative_bet
            #    bets[talk_idx] = max_bet
            #    call_count = 0

            # ! NEW
            if choise < 0:
                #Fould
                bets[talk_idx] = -1
                fould_count += 1
                self.deck.add_graveyard(player.hand)

            else:
                choise = choise // self.initial_bet * self.initial_bet
                
                if choise == 0:
                    # check or call
                    call_count += 1
                    ...
                else:
                    # raise
                    call_count = 0
                    ...
                
                # per essere in pari con la puntata
                to_be_good = max_bet - bets[talk_idx]

                actual_bet = to_be_good + choise

                # x giocatori all in
                # ? pensare a come non dover ciclare
                for p_all_in in self.players_allin:
                    if bets[talk_idx] > p_all_in[1]: # se ho già messo la mia parte salta
                        continue
                    
                    bet_difference = p_all_in[1] - bets[talk_idx] # quanto bisogna aggiungere al montepremi del tizio x all_in
                    # * to check
                    # aggiungi al montepremi la differenza o tutto quello che hai se è di meno
                    to_add = bet_difference if actual_bet > bet_difference  else actual_bet
                    p_all_in[2] += to_add

                if actual_bet >= player.score:
                    player.is_allin = True
                    actual_bet = player.score
                    self.players_allin.append([talk_idx,
                                               bets[talk_idx] + actual_bet,
                                               self.jackpot + actual_bet])

                else:
                    ...
                
                bets[talk_idx] += actual_bet
                self.jackpot += actual_bet
                player.score -= actual_bet
                
                # aggiorno la puntata massima che al massimo è uguale
                max_bet = bets[talk_idx] if bets[talk_idx] > max_bet else max_bet
                
            talk_idx = (talk_idx + 1) % (self.n_player)

        if max_bet == 0:
            print("Carta gratis")
        
        # ! da rivedere questa logica
        players_in_game = [self.players[k] if bets[k] >= 0 else -1 for k in range(self.n_player)]
        for i in range(players_in_game.count(-1)):
            players_in_game.remove(-1)
        print("\nSono in gioco:")
        for player in players_in_game:
            print(f"{player.nickname}")
        #
        #players_in_game = []
        #for i, bet in enumerate(bets):
        #    if bet < 0:
        #        continue
        #    else:
        #        players_in_game.append(self.players[i])
#
        return players_in_game


    def dealing_card(self):
        if self.current_round == 0:
            for player in self.players:
                player.draw_from(self.deck.pile, 2)
                print(f"{player.nickname} ha ricevuto:")
                player.hand.reveal()
        elif self.current_round == 1:
            print("Flop down, fate il vostro gioco")
            self.deck.add_graveyard(self.deck.draw())
            Poker.table.draw_from(self.deck.pile, 3)
            Poker.table.area.reveal()

        elif self.current_round == 2:
            print("Turn down, fate il vostro gioco")
            self.deck.add_graveyard(self.deck.draw())
            Poker.table.draw_from(self.deck.pile)
            Poker.table.area.reveal()
            
        elif self.current_round == 3:
            print("Rivers out, fate il vostro gioco")
            self.deck.add_graveyard(self.deck.draw())
            Poker.table.draw_from(self.deck.pile)
            Poker.table.area.reveal()
        else:
            print("Showdown!")
    
    def valuta_punti(self):
        player_best_score = []
        for player in self.players:
            best_score = [0, 0]
            extended_card = player.hand.cards + Poker.table.area.cards

            list_comb = list(combinations(extended_card, 5))

            for combination in list_comb:
                x = []
                [x.append(card) for card in combination]
                    
                possible_cards = sets_card.Set_of_Cards(x)
                actual_score = pyrule.PokerRules.check_score(possible_cards)

                if actual_score[0] > best_score[0]:
                    best_score = actual_score
                elif actual_score[0] == best_score[0]:
                    if actual_score[1] > best_score[1]: #copre carta alta e scala
                        best_score = actual_score
                    elif actual_score[0] == 2:
                        actual_score[2] > best_score[2]
                    elif actual_score[0] == 6:
                        if actual_score[2] > best_score[2]:
                            best_score = actual_score
                
            print(f"{player.nickname} ha fatto {self.SCORE[best_score[0]]}")
            player_best_score.append(best_score)
        best_player = len(player_best_score) -1

        for i, score in enumerate(player_best_score):
            #saltare l'ultimo numero
            if score[0] > best_score[0]:
                best_score = score
                best_player = i
            elif score[0] == best_score[0]:
                if score[1] > best_score[1]:
                    best_score = score
                    best_player = i
                elif score[0] == 2:
                    score[2] > best_score[2]
                    best_player = i
                elif score[0] == 6:
                    if score[2] > best_score[2]:
                        best_score = score
                        best_player = i

        print(f"La mano è vinta dal giocatore {best_player} con -> {self.SCORE[best_score[0]]}")
        return best_player

    def handle_turn(self):
        print("Altro girno nuove puntate")
        self.jackpot = 0
        self.current_round = 0
        self.dealing_card()
        self.puntata()
        winner_turn = self.valuta_punti()
        self.players[winner_turn].score += self.jackpot

    
    def who_broke(self):
        for player in self.players[::-1]:
            if player.score < self.initial_bet:
                idx = self.players.index(player)
                self.players.remove(player)
                self.n_player -= 1
                print(f"{player.nickname} abbandona il gioco per mancanza di fondi")
                if idx <= self.current_dealer:
                    self.current_dealer = (self.current_dealer -1) % self.n_player
            else:
                print(f"Il {player.nickname} continua a sfidare la sorte")

    def show_winner(self):
        print("Solo 2 giocatori rimasti -> il cheap leader è il vincintore.")
        if self.players[0].score == self.players[1].score:
            print("lancio della moneta per capire chi è il cheap leader")
            winner = random.randint(0, 1)
        elif self.players[0].score > self.players[1].score:
            winner = 0
        else:
            winner = 1
        print(f"Vince {self.players[winner].nickname} con {self.players[winner].score} fiches")


    def play(self):
        gameover = False
        while not gameover:
            if self.n_player > 2:
                self.handle_turn()
                
            else:
                self.show_winner()
                gameover = True


if __name__ == "__main__":
    game = Poker(4)
    game.deck.shuffle()


    #x = random.sample(list(range(game.n_player)), 2)
    #print(x)
    #for i, player in enumerate(game.players):
    #    if i in x:
    #        player.is_human = False
    #    
    #    print(player.is_human)

    for i in range(4):
        game.dealing_card()
        game.current_round += 1


    game.players[0].score = 1000
    game.players[1].score = 5000
    game.players[2].score = 300
    game.players[3].score = 2000

    game.puntata()

    game.valuta_punti()

    out_game = random.sample(list(range(game.n_player)), 2)

    #print(f"\n{out_game}")
    #for idx in out_game:
    #    game.players[idx].score = random.randint(-1000, 0)

    print()
    print(f"Il dealer è il {game.players[game.current_dealer].nickname}")
    game.who_broke()
    print(f"Il dealer è il {game.players[game.current_dealer].nickname}")
    #extended_card = p1.hand.cards + Poker.table.area.cards
#
    #list_comb = list(combinations(extended_card, 5))
#
    #for combination in list_comb:
    #    x = []
    #    [x.append(card) for card in combination]
    #        
    #    possible_cards = sets_card.Set_of_Cards(x)
    #    pyrule.PokerRules.check_score(possible_cards)
    #    print(f"La mano del giocatore dopo che ha giocato è {p1.hand}")

    
    