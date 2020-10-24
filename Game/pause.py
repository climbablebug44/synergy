import pygame

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.Quit:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.k_c:
                    paused = False
                elif event.key == pygame.k_q:
                    pygame.quit()
                    quit()
        pygame.display.fill(0,0,0)
        pygame.draw_text("Paused ",25,435,330)             
        pygame.draw_text("Press c To continue and q to quit",25,435,400)
        pygame.display.update()            
                

     # put this pause function inside your game control if-else statement
     # like: elif event.key == pygame.k_p:
         #pause() (calling the  pause function)
         