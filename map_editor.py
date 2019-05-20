import pygame
import numpy as np


pygame.init()
file = open('level.txt', 'w')
size = width, height = 1280,960
window = pygame.display.set_mode(size)
pygame.display.set_caption( "Race-AI map editor" )

clock = pygame.time.Clock()
fps = 60
to_draw = []



current_color = 0
draw_start = False

red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

font = pygame.font.Font(None, 36)
def show_text(msg ,color, x, y):
    text = font.render(msg, True, color)
    textpos = (x, y)
    window.blit(text, textpos)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = mouse_pos
            draw_start = True

        if event.type == pygame.MOUSEBUTTONUP:
            final_pos = mouse_pos
            draw_start = False

            #rect = pygame.Rect(pos,(final_pos[0]- pos[0], final_pos[1]-pos[1]))
            #rect.normalize()
            to_draw += [(pos, final_pos)]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_RETURN:
                for platform in to_draw:

                    print("["+str(platform).split("(")[1].split(")")[0] +",black ],")
                    file.write("["+str(platform).split("(")[1].split(")")[0] +",black ]\n")
            if event.key == pygame.K_BACKSPACE:
                to_draw.pop()
    window.fill(white)

    # show line when mouse button down
    if draw_start:
        pygame.draw.line(window, black, pos, mouse_pos, 4)


    # TODO: fix this
    # draws all saved lines permanently
    for i in range(0, len(to_draw)):
            pygame.draw.line(window, black, to_draw[i][0], to_draw[i][1], 4)



    show_text("x:", black, 1070, 0)
    show_text(str(mouse_x), black, 1100, 0)
    show_text("y:", black, 1170, 0)
    show_text(str(mouse_y), black, 1200, 0)

    pygame.display.update()
    clock.tick(fps)

file.close()
pygame.quit()