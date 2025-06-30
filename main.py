import pygame
from states.logo_state import LogoState
from states.menu_state import MenuState
from states.game_state import GameState
from states.pause_state import PauseState
from states.finish_state import FinishState


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Пятнашки")
    clock = pygame.time.Clock()
    
    states = LogoState(screen, lambda new_state: change_state(new_state))
    old_ = None

    def change_state(new_state):
        nonlocal states, old_
        if new_state == "menu":
            old_ = None
            states = MenuState(screen, lambda new_state: change_state(new_state))
        elif new_state == "pause":
            old_ = states
            states = PauseState(screen, lambda new_state: change_state(new_state))
        elif new_state == "finish":
            old_ = states
            states = FinishState(screen, lambda new_state: change_state(new_state))
        elif new_state == "game":
            if old_ is None:
                states = GameState(screen, lambda new_state: change_state(new_state))
            else:
                states = old_
                old_ = None


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            states.handle_events(event)
        
        states.draw()
        clock.tick(60)


if __name__ == "__main__":
    main()
