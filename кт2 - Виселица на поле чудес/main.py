import game


game.start()

while game.is_running():
    game.draw_game()
    game.play_turn()
    if game.player_won():
        game.stop_game()
    elif game.player_lost():
        game.stop_game()

game.show_result()
