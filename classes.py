
class Player:
    def __init__ (self, name, is_ai_player, current_sum_of_chips, current_bet, in_this_round, hand=None):
        self.name = name
        self.is_ai_player = is_ai_player
        self.current_sum_of_chips = current_sum_of_chips
        self.current_bet = current_bet
        self.sum_of_all_hands_bet = current_bet
        self.is_a_split_hand = False
        self.in_this_round = in_this_round
        self.hand = hand if hand is not None else []

