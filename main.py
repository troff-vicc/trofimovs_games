import pygame
from states.menu_state import MenuState
from states.game_state import GameState


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    
    states = MenuState(screen, lambda new_state: change_state(new_state))
    
    def change_state(new_state):
        nonlocal states
        if new_state == "menu":
            states = MenuState(screen, lambda new_state: change_state(new_state))
        elif new_state == "game":
            states = GameState(screen, lambda new_state: change_state(new_state))
    
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
