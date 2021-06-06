import ast
import os
import sys
import pygame
import menu
import game
import common


def main():
    player_name = ''
    pygame.mixer.init()
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

    new_best: int = 0

    while True:
        player_name = menu.menu({'name': player_name, 'new_best': new_best})
        if player_name != common.Command.EXIT:
            player_score = game.game()
        else:
            break

        print(str(player_name) + " : " + str(player_score))
        if player_score > scores.get(player_name, 0):
            new_best = player_score
            scores[player_name] = player_score
            with open('scores.txt', 'w') as f:
                f.write(scores.__str__())
        else:
            new_best = 0

    pygame.joystick.quit()
    pygame.mixer.quit()
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()
