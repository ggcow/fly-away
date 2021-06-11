import ast
import menu
import game
from common import *


def main():
    player_name = ''
    pygame.mixer.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        j = pygame.joystick.Joystick(0)
        j.init()

    if not os.path.exists('scores.txt'):
        with open('scores.txt', 'w') as f:
            f.write('{}')
        scores = {}
    else:
        with open('scores.txt', 'r') as f:
            scores = ast.literal_eval(f.readline())

    player_score: int = 0
    new_best = False
    m = menu.Menu()

    while True:
        player_name = m.main({'name': player_name, 'score': player_score, 'new_best': new_best})
        if player_name != Command.EXIT:
            try:
                best_score = list(scores.values())[0]
            except IndexError:
                best_score = 0
            player_score = game.game(best_score)
        else:
            break

        print(str(player_name) + " : " + str(player_score))
        if player_score > scores.get(player_name, 0):
            new_best = True
            scores[player_name] = player_score
            scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
            with open('scores.txt', 'w') as f:
                f.write(scores.__str__())
        else:
            new_best = 0

    pygame.joystick.quit()
    pygame.mixer.quit()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()
