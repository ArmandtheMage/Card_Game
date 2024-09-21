from math import floor
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
        self.scary_player = False
        
        for i in range(self.n_player):
            dummy_name = "Giocatore_" + str(i +1)
            self.players.append(my_player.Player(self.deck, area=None,
                                                 nickname=dummy_name,
                                                 hand=sets_card.Set_of_Cards([], 2, 0),
                                                 initial_score=10000))
        
        
        self.current_dealer = random.randint(0, self.n_player -1)
        #self.jackpot = 0
        self.jackpots = []
        self.bets = []
        #self.players_allin = []

    def puntata(self):
        #players_in_game = [True for x in range(0, self.n_player)]
        #self.bets = [0 if x else -1 for x in players_in_game]
        self.bets = [0 for x in range(self.n_player)] # ? da portare fuori
        #self.players_in_game = [bet >= 0 for bet in self.bets] # inizio tutti True

        #* per debug
        #self.jackpots = [0 for x in self.bets]

        if self.current_round == 0:
            talk_idx = (self.current_dealer + 3) % (self.n_player)
            self.bets[(self.current_dealer + 1) % (self.n_player)] = self.initial_bet // 2
            self.bets[(self.current_dealer + 2) % (self.n_player)] = self.initial_bet
            max_bet = self.initial_bet
            #self.jackpots = [jackpot + floor(self.initial_bet * 1.5) for jackpot in self.jackpots]
            da_pagare = True
            fould_count = 0
        else:
            talk_idx = ((self.current_dealer + 1) % (self.n_player))

            max_bet = 0
            da_pagare = False
            fould_count = self.players_in_game.count(False)

        call_count = 0
        
        players_allin = [p.is_allin for p in self.players].count(True)

        while call_count + fould_count < self.n_player and players_allin < self.n_player:
            #scegli quanto puntare
            # 3 possibilità 0, -1, > 0
            #*if self.bets[talk_idx] < 0: #giocatore in fould
            if not self.players_in_game[talk_idx]:
                talk_idx = (talk_idx + 1) % self.n_player
                continue
            
            player: my_player.Player = self.players[talk_idx]
            print(f"è il turno del {player.nickname} che è il {talk_idx} al tavolo")
            
            if player.is_allin:
                call_count += 1
                talk_idx = (talk_idx + 1) % self.n_player
                print(f"{player.nickname} è all in")
                continue

            if da_pagare:
                if talk_idx == (self.current_dealer + 1) % (self.n_player):
                    print(f"Sei lo small blind hai già pagato {self.bets[talk_idx]}")
                    #self.jackpot += self.bets[talk_idx]
                    player.score -= self.bets[talk_idx]
                    #player.jackpot = self.bets[talk_idx]
                elif talk_idx == (self.current_dealer + 2) % (self.n_player):
                    print(f"Sei il big blind hai già pagato {self.bets[talk_idx]}")
                    #self.jackpot += self.bets[talk_idx]
                    player.score -= self.bets[talk_idx]
                    #player.jackpot = self.bets[talk_idx]
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

            if choise < 0:
                #Fould
                print("Fould")
                #*self.bets[talk_idx] = -1
                self.players_in_game[talk_idx] = False
                fould_count += 1
                #self.deck.add_graveyard(player.hand)

            else:
                choise = choise // self.initial_bet * self.initial_bet
                
                # per essere in pari con la puntata
                to_be_good = max_bet - self.bets[talk_idx]

                actual_bet = to_be_good + choise

                if player.score <= actual_bet:
                    player.is_allin = True
                    actual_bet = player.score

                if choise == 0 or player.score <= to_be_good:
                    # check or call
                    print(f"Call")
                    call_count += 1
                else:
                    # raise
                    print(f"Raise")
                    call_count = 1
                
                self.bets[talk_idx] += actual_bet
                player.score -= actual_bet
                
                # aggiorno la puntata massima che al massimo è uguale
                max_bet = self.bets[talk_idx] if self.bets[talk_idx] > max_bet else max_bet
                
            talk_idx = (talk_idx + 1) % (self.n_player)
            players_allin = [p.is_allin for p in self.players].count(True)

            if self.players_in_game.count(True) == 1:
                idx = self.players_in_game.index(True)
                print(f"Il {self.players[idx].nickname} è l'unico ancora in gioco quindi vince")
                self.scary_player = True #* Special Value
                break

        if max_bet == 0:
            print("Carta gratis")
        else:
            for i, jackpot in enumerate(self.jackpots):
                if self.players_in_game[i]:
                    for bet in self.bets:
                        self.jackpots[i] += bet if self.bets[i] > bet else self.bets[i]
                        #if self.bets[i] > bet:
                        #    jackpot += bet
                        #else:
                        #    jackpot += self.bets[i]

                else:
                    continue
        
        


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
        if self.scary_player:
            self.scary_player = False
            idx = self.players_in_game.index(True)
            self.players[idx].score += self.jackpots[idx]
            return []

        player_best_score = []
        new_player_best_score = []
        for i, player in enumerate(self.players):
            if not self.players_in_game[i]:
                continue
            best_score = [0, 0]
            extended_card = player.hand.cards + Poker.table.area.cards

            list_comb = list(combinations(extended_card, 5))

            new_eval_score = []
            for combination in list_comb:
                x = []
                [x.append(card) for card in combination]
                    
                possible_cards = sets_card.Set_of_Cards(x)
                actual_score = pyrule.PokerRules.check_score(possible_cards)
                new_eval_score.append(actual_score)

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
            new_eval_score.sort(reverse=True)
            print(new_eval_score[0])
            print(f"Controprova: {player.nickname} ha fatto secondo il nuovo metodo: {self.SCORE[new_eval_score[0][0]]}")
            player_best_score.append(best_score)
            new_player_best_score.append(new_eval_score[0])

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
        
        #new_player_best_score.sort()

        index_in_play = []
        for k in range(len(self.players_in_game)):
            if self.players_in_game[k]:
                index_in_play.append(k)
            else:
                self.jackpots[k] = 0

        out = [k if p else None for p in self.players_in_game]

        #Z = zip(new_player_best_score, list(range(len(self.players_in_game))))
        Z = zip(new_player_best_score, index_in_play)
        ranking = sorted(Z, key=lambda x : x[0], reverse=True)
        

        print(f"La mano è vinta dal giocatore {self.players[best_player].nickname} con -> {self.SCORE[best_score[0]]}")
        # TODO fix questa stampa + in pyrule
        #*print(f"Controprova: vince {self.players[out[1]].nickname} con: {self.SCORE[out[0][0][0]]}")
        return ranking


    def handle_turn(self):
        print("Altro girno nuove puntate")
        #self.jackpots = [self.initial_bet // 2 * 3 for x in self.players]
        self.jackpots = [0 for x in self.players]
        self.players_in_game = [True for x in self.players]
        self.current_round = 0
        ## ! DEBUG
        #self.current_round = 4
        #self.players_in_game[0] = False
        #self.players_in_game[1] = False
        ### ! per debug
        #self.jackpots[0] = 2200
        #self.jackpots[1] = 300
        #self.jackpots[2] = 1000
        #self.jackpots[3] = 1000
        ### ! fine variabili per debug
        ## ! GUBED

        while(self.current_round < 4 and not self.scary_player):
            self.dealing_card()
            self.puntata()
            self.current_round += 1
            
        winner_turn = self.valuta_punti()

        if winner_turn:
            # TODO riscrivere la parte di jackpot in valuta punti e rifare i riferimenti che sono obbrobbriosi
            all_paid = [jackpot > 0 for jackpot in self.jackpots]
            inizial_out = self.jackpots.count(0) # ! questo è da cambiare
            #* prova ad usare condizione dopo il for, qui filter non va bene
            #[jackpot > 0 for i, jackpot in enumerate(self.jackpots) if self.players_in_game[i]]

            win_report = [[win[0],
                        win[1],
                        self.jackpots[win[1]]]
                        for win in winner_turn]

            while all_paid.count(True) > 0: # se qualcuno deve ancora ricevere la vincita
                winners = []
                split_pot = 0 # con quanti devo dividere
                #win_score = winner_turn[0][0][0]
                winners.append(win_report[split_pot][1]) # lista di vincitori
                #i = 0
                
                while split_pot < all_paid.count(True) -1 and win_report[split_pot][0] == win_report[split_pot + 1][0]:
                    split_pot += 1
                    winners.append(win_report[split_pot][1])

                if split_pot > 0:
                    msg = "Il piatto è condiviso tra: "
                else:
                    msg = "Il vincitore è "

                for winner in winners:
                    msg += f"{self.players[winner].nickname}, "
                    
                
                print(msg[:-2])

                #money_split = sorted(jackpots)
                
                #k = 0
                #jackpot = money_split[k][0]
                #*paying = []
                money_split = []
                for n in range(split_pot + 1):
                    money_split.append(win_report.pop(0))

                money_split.sort(key=lambda x: x[2])

                for k in range(split_pot + 1): #per quanti dividere
                    jackpot = money_split[k][2]
                    if jackpot <= 0:
                        continue

                    for n in range(split_pot - k + 1): # Se non hanno lo stesso jackpot
                        self.players[money_split[k + n][1]].score += jackpot // (split_pot - k + 1)

                    self.jackpots = [k_jackpot - jackpot for k_jackpot in self.jackpots]

                    money_split[k:] = [[m[0], m[1],
                                    m[2] - jackpot]
                                    for m in money_split[k:]]

                    win_report = [[m[0], m[1],
                                    m[2] - jackpot]
                                    for m in win_report]

                all_paid = [jackpot > 0 for jackpot in self.jackpots]
                z = all_paid.count(False)

                #defeated = 1 - z if z > 1 else None
                #*win_report = win_report[split_pot:]

                for c in range(z):
                    idx = all_paid.index(False)
                    all_paid.pop(idx)
                    self.jackpots.pop(idx)
                    if c > split_pot + inizial_out:
                        win_report.pop(idx)


                #for j in jackpots: # modificare jackpots con money_split
                #    if jackpots[k + divide_for] == jackpots[k + divide_for + 1]:
                #        divide_for += 1
                #        continue
                #    else:
                #        # Prendo la vincita
                #        jackpot = money_split[k][0]
                #        # Aggiorno i punteggi
                #        for n in range(divide_for):
                #            self.players[money_split[k + n][1]].score += j // (divide_for + 1)
    #
                #        self.jackpots = [k_jackpot - jackpot for k_jackpot in self.jackpots]
    #
                #        k += divide_for + 1
                #        divide_for = 0
                #    

            #*self.deck.add_graveyard(Poker.table.area)
            #*for player in self.players:
            #*    self.deck.add_graveyard(player.hand)
    #*
            #*self.players[winner_turn].score += self.jackpots[winner_turn] 
    
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
        if len(self.players) == 1:
            winner = 0
        else:
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
                
                for player in self.players:
                    self.deck.add_graveyard(player.hand)
                
                if len(self.table.area) > 0:
                    self.deck.add_graveyard(self.table.area)
                self.who_broke()

                self.current_round = 0
                self.current_dealer = (self.current_dealer + 1) % self.n_player
                self.deck.shuffle(True)
            else:
                self.show_winner()
                gameover = True


if __name__ == "__main__":
    game = Poker(4)
    game.deck.shuffle()

    game.players[0].hand = game.players[0].hand + my_card.FrenchCard(5,0) + my_card.FrenchCard(5,3)
    game.players[1].hand = game.players[1].hand + my_card.FrenchCard(5,1) + my_card.FrenchCard(5,2)
    game.players[2].hand = game.players[2].hand + my_card.FrenchCard(0,0) + my_card.FrenchCard(4,3)
    game.players[3].hand = game.players[3].hand + my_card.FrenchCard(4,0) + my_card.FrenchCard(7,3)

    game.table.area = game.table.area + my_card.FrenchCard(12,0) + my_card.FrenchCard(0,2) + my_card.FrenchCard(1,0) + my_card.FrenchCard(2,1) + my_card.FrenchCard(3,0)

    print(f"Sul tavolo c'è:\n{game.table.area}")

    for player in game.players:
        print(f"{player.nickname} ha: {player.hand}")

    game.handle_turn()
    #game.play()
    

    #x = random.sample(list(range(game.n_player)), 2)
    #print(x)
    #for i, player in enumerate(game.players):
    #    if i in x:
    #        player.is_human = False
    #    
    #    print(player.is_human)

    #for i in range(4):
    #    game.dealing_card()
    #    game.current_round += 1


    #game.players[0].score = 1000
    #game.players[1].score = 5000
    #game.players[2].score = 300
    #game.players[3].score = 2000

    #game.puntata()
#
    ##game.valuta_punti()

    #out_game = random.sample(list(range(game.n_player)), 2)

    #print(f"\n{out_game}")
    #for idx in out_game:
    #    game.players[idx].score = random.randint(-1000, 0)

    #print()
    #print(f"Il dealer è il {game.players[game.current_dealer].nickname}")
    #game.who_broke()
    #print(f"Il dealer è il {game.players[game.current_dealer].nickname}")
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

    
    