import art
import var
import classes
import random
from pynput.keyboard import Listener, Key
import threading


def on_key_press(key):
    if key == Key.esc:
        var.running = False


def main():
    with (Listener(on_press=on_key_press) as listener):
        var.round_num = 0
        try:
            while var.running:
                var.new_decks_of_cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'] * 4 * input_decks()
                var.playing_decks = var.new_decks_of_cards.copy()

                var.initial_amount_of_chips = input_initial_amount_of_chips()
                var.amount_of_human_players = input_amount_of_human_players()
                var.amount_of_ai_players = input_amount_of_ai_players()
                initialize_players()

                while True:
                    var.round_num += 1
                    initialize_blackjack_round()
                    scoreboard = ''
                    num_players_left = 0

                    for p in var.players:
                        if p.is_a_split_hand:
                            var.players.remove(p)
                        elif p.current_sum_of_chips < 10:
                            print(f'{p.name} doesn\'t have enough chips to keep playing. {p.name} is kicked out!')
                            var.players.remove(p)
                        else:
                            scoreboard += f'-{p.name}: {p.current_sum_of_chips}-  '
                            if not p.is_ai_player:
                                num_players_left += 1
                    if num_players_left == 0:
                        print('There are no more players left with chips to keep playing. The Casino closes for tonight.')
                        break

                    print('-press ESC to exit the game-')
                    print(art.logo)
                    print(scoreboard + '\n')

        except KeyboardInterrupt:
            print("\nESC was pressed. The game was interrupted by a user.")
        finally:
            print("The Casino is closed.")
            listener.stop()



def check_input_is_y_o_n(p):
    """Checks that the input is a 'y' or 'n'."""
    if p != 'y':
        if p == 'n':
            print('Another time then, have a nice day!')
            exit()
        else:
            p = input('Wrong input. If you want to play a game of Blackjack type \'y\', otherwise type \'n\': ').lower()
            check_input_is_y_o_n(p)
    else:
        print('Great, let\'s get started:')

def input_decks():
    """Checks and makes sure that the input is an int between 1 and 12."""
    while True:
        try:
            a = int(input('How many decks do you wish to play with? Type a value from 1 to 8: '))
            if isinstance(a, int):
                if 0 < a < 9:
                    return a
                else:
                    print('Invalid amount.')
        except ValueError:
            print('Invalid input type.')

def input_initial_amount_of_chips():
    """Checks and makes sure that the input is an int between 100 and 100.000."""
    while True:
        try:
            a = int(input('How many chips are players going to start the game with? Type a value from 100 to 100.000: '))
            if isinstance(a, int):
                if 100 <= a <= 100000:
                    return a
                else:
                    print('Invalid amount.')
        except ValueError:
            print('Invalid input type.')



def input_amount_of_human_players():
    """Checks and makes sure that the input is an int between 1 and 8."""
    while True:
        try:
            a = int(input("How many players will be playing? Choose an amount from 1 to 8: "))
            if isinstance(a, int):
                if 0 < a < 9:
                    return a
                else:
                    print('Invalid amount.')
        except ValueError:
            print('Invalid input type.')

def input_amount_of_ai_players():
    """Checks and makes sure that the input is an int between 0 and 8-amount_of_players."""
    while True:
        try:
            if var.amount_of_human_players == 8:
                return
            a = int(input(f"How many AI players do you want to add? Choose an amount from 0 to {8-var.amount_of_human_players}: "))
            if isinstance(a, int):
                if 0 <= a < 9 - var.amount_of_human_players:
                    return a
                else:
                    print('Invalid amount.')
        except ValueError:
            print('Invalid input type.')


def minimum_bet():
    """Allows to change the minimum bet of the round and the amount that the AI's will bet."""
    print(f'The minimum bet is {var.min_bet}.')
    while True:
        a = input(f'If you wish to change the minimum bet, enter a new value from 10 to {var.initial_amount_of_chips}, otherwise hit \'ENTER\': ')
        if a == '':
            return
        try:
            a = int(a)
            if 10<= a <= var.initial_amount_of_chips:
                var.min_bet = a
                for p in var.players:
                    if p.current_sum_of_chips < var.min_bet:
                        p.current_bet = 0
                        p.in_this_round = False
                        print(f'{p.name} doesn\'t have enough chips to meet the minimum bet and must stand down for this round.')
                return
            else:
                print(f'Invalid amount. ')
        except ValueError:
            print('Invalid input type.')


def initialize_players():
    """Asks for the necessary input for each player and initialize them as objects."""

    for pl in range(1, var.amount_of_human_players+1):
        name = input(f'What is the name of Player {pl}? ')
        for p in var.players:
            while p.name == name:
                name = input('Taken name, input another name for this player: ')
        player = classes.Player(name, False, var.initial_amount_of_chips, var.min_bet, True)
        var.players.append(player)

    for c in range(1, var.amount_of_ai_players+1):
        player = classes.Player(f'AI Player {c}', True, var.initial_amount_of_chips, var.min_bet, True)
        var.players.append(player)



def input_bet():
    """Checks that the input is an int between 1 and the players current sum of chips"""
    for p in var.players:
        if p.is_ai_player:
            p.current_bet = var.min_bet
        else:
            while True:
                i = input(f'{p.name} your current sum is ${p.current_sum_of_chips}. How much do you wish to bet? ')
                try:
                    a = int(i)
                    if var.min_bet <= a < p.current_sum_of_chips:
                        p.current_bet = a
                        p.sum_of_all_hands_bet = a
                        break
                    elif a == p.current_sum_of_chips:
                        print(f'{p.name} is going All In! May the Goddess of fortune smile upon you.')
                        p.current_bet = a
                        p.sum_of_all_hands_bet = a
                        break
                    elif a == 0:
                        p.in_this_round = False
                        p.current_bet = a
                        p.sum_of_all_hands_bet = a
                        print(f'{p.name} is standing down in this round.')
                        break
                    else:
                        print(f'Invalid amount. The amount need to be between {var.min_bet} and {p.current_sum_of_chips}. You can stand down by betting 0.')
                except ValueError:
                    print('Invalid input type.')
    print(f'\n')


def deal_card():
    """Deals a card."""
    if len(var.playing_decks) < 2:
        print('Changing cards...')
        var.playing_decks = var.new_decks_of_cards.copy()
        deal_card()
    else:
        drawn_card = random.choice(var.playing_decks)
        var.playing_decks.remove(drawn_card)
        return drawn_card


def score(hand):
    s = 0
    num_of_a = 0
    for c in hand:
        if str(c).isdigit():
            s += int(c)
        elif c =='A':
            num_of_a+=1
        elif c in ['J', 'Q', 'K']:
            s += 10
    if num_of_a > 0:
        if (s+num_of_a) < 12:
            s += num_of_a+10
        elif (s+num_of_a) > 11:
            s += num_of_a
    return s


def initialize_blackjack_round():
    var.dealers_hand = []
    for p in var.players:
        p.in_this_round = True
        p.hand = []
    print(f'\nLet\'s start round {var.round_num}: ')
    minimum_bet()
    print('Welcome. Please place your bets for this round. ')
    input_bet()

    for i in range(1,3):
        for p in var.players:
            if p.in_this_round:
                p.hand.append(deal_card())

    var.dealers_hand.append(deal_card())
    print(f'The Dealer\'s first card: {var.dealers_hand[0]}; current score: {score(var.dealers_hand)}')
    var.dealers_hand.append(deal_card())


    for p in var.players:
        if p.in_this_round:
            print(f'{p.name}\'s cards: {p.hand}; current score: {score(p.hand)}')

    print('\nTo Hit -Type \'h\', \'hit\' or press \'ENTER\'-, Stand -Type \'s\' or \'stand\'-, Double Down Stand -Type \'dd\' or \'double down\'- or Split Stand -Type \'ss\' or \'split stand\'-: ')

    play_round()
    results()
    print(f'\n')


def play_round():
    """To double down or split stand the total value of all bets in all hands needs to be accounted for to make sure it doesn't exceed the total amount of held chips"""
    for p in var.players:
        if p.in_this_round and not p.is_ai_player:
                while score(p.hand) < 21:
                    a = input(f'{p.name}\'s hand: {p.hand}; current score: {score(p.hand)}: ')
                    try:
                        if isinstance(a, str):
                            if a == 'h' or a == 'hit' or a =='':
                                p.hand.append(deal_card())
                            elif a == 's' or a == 'stand':
                                p.in_this_round = False
                                break
                            elif len(p.hand) == 2 and (a == 'dd' or a =='double down'):
                                if p.current_bet + p.sum_of_all_hands_bet <= p.current_sum_of_chips:
                                    print('Doubling Down...')
                                    add_bet_to_sum_of_all_bets(p)
                                    p.current_bet *= 2
                                    print(f'{p.name} doubled their bet to {p.current_bet}.')
                                else:
                                    print(f'{p.name} you don\'t have enough chips to double down.')

                            elif len(p.hand) == 2 and (a == 'ss' or a == 'split stand'):
                                if p.hand[0] == p.hand[1] and p.current_bet + p.sum_of_all_hands_bet <= p.current_sum_of_chips:
                                    add_bet_to_sum_of_all_bets(p)

                                    print('Splitting Stand...')
                                    p.hand = [p.hand[0]]
                                    split_hand = classes.Player(f'{p.name}\'s split hand', False, p.current_sum_of_chips, p.current_bet, True)
                                    split_hand.is_a_split_hand = True
                                    split_hand.sum_of_all_hands_bet = p.sum_of_all_hands_bet
                                    split_hand.hand = p.hand.copy()
                                    split_hand.hand.append(deal_card())
                                    var.players.insert(var.players.index(p) + 1, split_hand)
                                    p.hand.append(deal_card())
                                    print(f'{p.name} two new split hands are: {p.hand} and {split_hand.hand}. To begin with play your first new hand, then you will play the following one.')

                                else:
                                    a = input('You are ineligible for Splitting Stand. Press \'ENTER\' to Hit, type \'s\' to Stand, \'dd\' to Double Down: ')
                            else:
                                print('Invalid action. Press \'ENTER\' to Hit, type \'s\' to Stand, \'dd\' to Double Down or \'ss\' to Split Stand: ')
                    except ValueError:
                        print('Invalid input type.')

                else:
                    if score(p.hand) == 21:
                        print(f'{p.name} your hand is {p.hand} with a score of 21!')
                    elif score(p.hand) > 21:
                        p.in_this_round = False
                        print(f'{p.name} you Bust! Your hand is: {p.hand} with a score of {score(p.hand)}.')

        elif p.in_this_round and p.is_ai_player:
            while score(p.hand) < 17:
                p.hand.append(deal_card())
                if score(p.hand) > 21:
                    print(f'{p.name} Bust! Their hand is: {p.hand} with a score of {score(p.hand)}.')
                    p.in_this_round = False
                else:
                    print(f'{p.name}\'s hand: {p.hand}; current score: {score(p.hand)}. ')

    while score(var.dealers_hand) < 17:
        var.dealers_hand.append(deal_card())
        if score(var.dealers_hand) > 21:
            print(f'The Dealer Bust! The Dealers hand is: {var.dealers_hand} with a score of {score(var.dealers_hand)}.')
        else:
            print(f'The Dealers hand: {var.dealers_hand}; current score: {score(var.dealers_hand)}. ')
    print('\n')

def add_bet_to_sum_of_all_bets(p):
    pp = p
    i = 0
    if not p.is_a_split_hand:
        p.sum_of_all_hands_bet += p.current_bet
    while pp.is_a_split_hand:
        pp = var.players[var.players.index(p) - i]
        var.players[var.players.index(p) - i].sum_of_all_hands_bet += p.current_bet
        i += 1

def find_parent(p):
    pp = p
    i = 0
    while pp.is_a_split_hand:
        pp = var.players[var.players.index(p) - i]
        i += 1
    print(f'Checking find_parent: the parent of {p.name} is {pp.name}?')
    return var.players[var.players.index(pp)]

def results():
    """Compares a players score p_score against the dealers score d_score and adjusts the players chip sum"""
    print(f'The Dealers hand is {var.dealers_hand} with a score of {score(var.dealers_hand)}. ')
    print(f'Results of round {var.round_num}: ')
    for p in var.players:
        if p.current_bet > 0:
            if not p.is_a_split_hand:
                if score(p.hand) > 21:
                    p.current_sum_of_chips -= p.current_bet
                    print(f"{p.name} bust and lose {p.current_bet} 😭.  New chip sum: {p.current_sum_of_chips}.")
                elif score(var.dealers_hand) > 21:
                    p.current_sum_of_chips += p.current_bet
                    print(f"The Dealer bust. {p.name} win {p.current_bet} 😁.  New chip sum: {p.current_sum_of_chips}.")
                elif score(p.hand) == score(var.dealers_hand):
                    if score(p.hand) == 21:
                        if len(p.hand) == len(var.dealers_hand):
                            print(f"{p.name} got a Push (draw) 🙃. Chip sum: {p.current_sum_of_chips}.")
                        elif len(p.hand) == 2:
                            p.current_sum_of_chips += int(1.5 * p.current_bet)
                            print(f"{p.name} win ${int(1.5 * p.current_bet)} with a Blackjack 😎.  New chip sum: {p.current_sum_of_chips}.")
                        elif len(var.dealers_hand) == 2:
                            p.current_sum_of_chips -= p.current_bet
                            print(f"{p.name} lose ${p.current_bet}, the Dealer has Blackjack 😱. New chip sum: {p.current_sum_of_chips}.")
                    else:
                        print(f"{p.name} got a Push (draw) 🙃. Chip sum: {p.current_sum_of_chips}.")
                elif len(p.hand) == 2 and score(p.hand) ==21:
                    p.current_sum_of_chips += int(1.5 * p.current_bet)
                    print(f"{p.name} win ${int(1.5 * p.current_bet)} with a Blackjack 😎.  New chip sum: {p.current_sum_of_chips}.")
                elif len(var.dealers_hand) == 2 and score(var.dealers_hand) == 21:
                    p.current_sum_of_chips -= p.current_bet
                    print(f"{p.name} lose ${p.current_bet}, the Dealer has Blackjack 😱. New chip sum: {p.current_sum_of_chips}.")
                elif score(p.hand) > score(var.dealers_hand):
                    p.current_sum_of_chips += p.current_bet
                    print(f"{p.name} win {p.current_bet} 😃.  New chip sum: {p.current_sum_of_chips}.")
                else:
                    p.current_sum_of_chips -= p.current_bet
                    print(f"{p.name} lose {p.current_bet} 😤.  New chip sum: {p.current_sum_of_chips}.")

            elif p.is_a_split_hand:
                pp = find_parent(p)
                if score(p.hand) > 21:
                    pp.current_sum_of_chips -= p.current_bet
                    print(f"{p.name} bust and lose {p.current_bet} 😭.  New chip sum: {pp.current_sum_of_chips}.")
                elif score(var.dealers_hand) > 21:
                    pp.current_sum_of_chips += p.current_bet
                    print(f"The Dealer bust. {p.name} win {p.current_bet} 😁.  New chip sum: {pp.current_sum_of_chips}.")
                elif score(p.hand) == score(var.dealers_hand):
                    if score(p.hand) == 21:
                        if len(p.hand) == len(var.dealers_hand):
                            print(f"{p.name} got a Push (draw) 🙃. Chip sum: {pp.current_sum_of_chips}.")
                        elif len(p.hand) == 2:
                            pp.current_sum_of_chips += int(1.5 * p.current_bet)
                            print(f"{p.name} win ${int(1.5 * p.current_bet)} with a Blackjack 😎.  New chip sum: {pp.current_sum_of_chips}.")
                        elif len(var.dealers_hand) == 2:
                            pp.current_sum_of_chips -= p.current_bet
                            print(f"{p.name} lose ${p.current_bet}, the Dealer has Blackjack 😱. New chip sum: {pp.current_sum_of_chips}.")
                    else:
                        print(f"{p.name} got a Push (draw) 🙃. Chip sum: {pp.current_sum_of_chips}.")
                elif len(p.hand) == 2 and score(p.hand) ==21:
                    pp.current_sum_of_chips += int(1.5 * p.current_bet)
                    print(f"{p.name} win ${int(1.5 * p.current_bet)} with a Blackjack 😎.  New chip sum: {pp.current_sum_of_chips}.")
                elif len(var.dealers_hand) == 2 and score(var.dealers_hand) == 21:
                    pp.current_sum_of_chips -= p.current_bet
                    print(f"{p.name} lose ${p.current_bet}, the Dealer has Blackjack 😱. New chip sum: {pp.current_sum_of_chips}.")
                elif score(p.hand) > score(var.dealers_hand):
                    pp.current_sum_of_chips += p.current_bet
                    print(f"{p.name} win {p.current_bet} 😃.  New chip sum: {pp.current_sum_of_chips}.")
                else:
                    pp.current_sum_of_chips -= p.current_bet
                    print(f"{p.name} lose {p.current_bet} 😤.  New chip sum: {pp.current_sum_of_chips}.")

        elif p.current_bet == 0:
            print(f'{p.name} didn\'t bet in this round.')
