import pygame
from gameObjects import GameEngine
from utils import RESOLUTION, UPSCALED

def main():
    #Initialize the module
    pygame.init()
    
    pygame.font.init()
    arial = pygame.font.SysFont("Arial", 50)

    for i in range(pygame.joystick.get_count()):
        print(i)
        j = pygame.joystick.Joystick(i)
        if not j.get_init():
            j.init()
        
    #Get the screen
    screen = pygame.display.set_mode(list(map(int, UPSCALED)))
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))

    
    gameEngine = GameEngine()
    
    RUNNING = True
    
    while RUNNING:
        gameEngine.draw(drawSurface)
        
        pygame.transform.scale(drawSurface,
                               list(map(int, UPSCALED)),
                               screen)
     
        pygame.display.flip()
        gameClock = pygame.time.Clock()
        
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                RUNNING = False
            else:
                gameEngine.handleEvent(event)
        
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000
        gameEngine.update(seconds)
        #message = arial.render((str(gameEngine.waveCounter)), True, (255, 255, 255))
        #screen.blit(message, (RESOLUTION[0]//2, RESOLUTION[1]+20))

    pygame.quit()


if __name__ == '__main__':
    main()