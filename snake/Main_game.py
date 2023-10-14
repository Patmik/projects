# 1 - Importowanie pakietów.
import pygame
from Snake import *
from Food import *
import sys
import random
import pygwidgets

# 2 - Definiowanie stałych.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 5
N_PIXELS_TO_MOVE = 1


# 3 - Inicjalizacja środowiska pygame.
pygame.init()
window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
clock = pygame.time.Clock()

# 4 - Wczytanie zasobów: obrazy, dźwięki itd.


# 5 - Inicjalizacja zmiennych.

oSnake = Sanke(window, WINDOW_WIDTH, WINDOW_HEIGHT)
oFood = Food(window, WINDOW_WIDTH, WINDOW_HEIGHT)
score = oSnake.score
flag = True
oScore = pygwidgets.DisplayText(window, (20, 50), 'Dowolny tekst', fontSize=36, textColor=WHITE)

# 6 - Pętla działająca w nieskończoność.
while True:

    # 7 - Sprawdzanie pod kątem zdarzeń i ich obsługa
    for event in pygame.event.get():
        # Jeżeli został kliknięty przycisk zamknięcia okna, należy wyjść z pygame i zakończyć działanie programu.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Sprawdzenie, czy użytkownik nacisnął klawisz.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and oSnake.direction != (10,0):
                oSnake.change_direction('LEFT')
            elif event.key == pygame.K_RIGHT and oSnake.direction != (-10,0):
                oSnake.change_direction('RIGHT')
            elif event.key == pygame.K_UP and oSnake.direction != (0,10):
                oSnake.change_direction('UP')
            elif event.key == pygame.K_DOWN and oSnake.direction != (0,-10):
                oSnake.change_direction('DOWN')

    # 8 - Wykonywanie wszelkich akcji dla „danej klatki”.
    oSnake.move()
    oSnake.eat(oFood.position,flag)
    if flag == True:
        flag = oSnake.flag
    else:
        oFood.randomize_position()
        flag = True
    
    oScore.setValue('Wynik:' + str(oSnake.score))
        
    


    # 9 - Usunięcie zawartości okna.
    window.fill(BLACK)

    # 10 - Wyświetlenie wszystkich elementów okna.
   
    oSnake.draw()  # Wyświetlenie weza
    oFood.draw()
    oScore.draw()
    # 11 - Uaktualnienie okna.
    pygame.display.update()

    # 12 - Niewielkie spowolnienie całości.
    clock.tick(FRAMES_PER_SECOND)  # Framework pygame wstrzyma na chwilę działanie.        