import art
import func
import var

while True:
    print(art.logo)
    func.check_input_is_y_o_n(input('Do you want to play a game of Blackjack? Type \'y\' or \'n\': ').lower())
    var.running = True
    func.main()








