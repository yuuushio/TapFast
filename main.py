import pygame
import numpy as np
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TILE_SIZE = 50

BORDER_SIZE = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (41, 37, 34)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Don't Tap")

def calc_true_res(nx, ny):
    # calculate left over w/h after taking away borders
    w = SCREEN_WIDTH - (nx*BORDER_SIZE)
    h = SCREEN_HEIGHT - (ny*BORDER_SIZE)

    return (w,h)

def tile_array(num_tiles_x=6, num_tiles_y=6):
    tile_coord_grid = np.empty((num_tiles_x, num_tiles_y), dtype=object)
    w, h = calc_true_res(num_tiles_x, num_tiles_y)

    tile_width = w//num_tiles_x
    tile_height = h//num_tiles_y

    print("tile size:", tile_width, tile_height)

    tmp_x, tmp_y = BORDER_SIZE, BORDER_SIZE

    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            tile_coord_grid[i, j] = (tmp_x+(tile_width*i), tmp_y+(tile_height*j))

    print(tile_coord_grid)
    return tile_coord_grid
            


def draw_tile(x, y, color, border_color, border_thickness=1, num_tiles=8):
    # Draw the outer rectangle (border)
    true_width = SCREEN_WIDTH 
    true_height = SCREEN_HEIGHT #- (num_tiles*2*border_thickness)
    tile_width = true_width//num_tiles
    tile_height = true_height//num_tiles
    
    # Draw the inner rectangle (main tile)
    pygame.draw.rect(screen, color, (x+border_thickness//2, y+border_thickness//2, tile_width-border_thickness, tile_height-border_thickness))

def main():

    running = True
    y_position = SCREEN_HEIGHT - TILE_SIZE
    x_position = random.randint(0, SCREEN_WIDTH - TILE_SIZE)
    num_tiles = 6
    tile_grid = tile_array(num_tiles, num_tiles)

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (x,y) in tile_grid:
                    print("Don't Tap!")
                    # y_position = SCREEN_HEIGHT - TILE_SIZE
                    # x_position = random.randint(0, SCREEN_WIDTH - TILE_SIZE)
                    # running = False

        screen.fill(BROWN)
        for i in range(num_tiles):
            for j in range(num_tiles):
                x_pos, y_pos = tile_grid[i, j]
                draw_tile(x_pos, y_pos, RED, BLACK)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
