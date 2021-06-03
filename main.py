import ast
import os
import sys
import pygame
import menu
import game
import common


def main():
    player_score = 0
    player_name = ''
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        j = pygame.joystick.Joystick(0)
        j.init()

    if not os.path.exists('scores.txt'):
        with open('scores.txt', 'w'):
            ...
        scores = {}
    else:
        with open('scores.txt', 'r') as f:
            scores = ast.literal_eval(f.readline())

    while True:
        player_name = menu.menu(player_name)
        if player_name != common.Command.EXIT:
            player_score = game.game()
        else:
            break

    if player_score > 0:
        scores['Eugene'] = player_score
        with open('scores.txt', 'w') as f:
            f.write(scores.__str__())

    pygame.joystick.quit()
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()
