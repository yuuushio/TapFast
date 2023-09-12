import pygame
import numpy as np
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TILE_SIZE = 50

BORDER_SIZE = 5

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
    # take away border_size to account for oth indexes (for both i and j)
    w = SCREEN_WIDTH - (nx*BORDER_SIZE) - BORDER_SIZE
    h = SCREEN_HEIGHT - (ny*BORDER_SIZE) - BORDER_SIZE

    return (w,h)



def tile_array(num_tiles_x=6, num_tiles_y=6):
    # initial matrix which calculates and stores the x,y coordinates of each tile
    tile_coord_grid = np.empty((num_tiles_x, num_tiles_y), dtype=object)
    w, h = calc_true_res(num_tiles_x, num_tiles_y)

    tile_width = w//num_tiles_x
    tile_height = h//num_tiles_y

    print("tile size:", tile_width, tile_height)


    num_rows = num_tiles_x*num_tiles_y
    matrix_shape = (num_rows, 4)

    # Cool idea: use matrix--instead of objects--to keep track of individual tile
    #  properties; mainly, its x,y coordinates, and the area it occupies.
    raw_matrix = np.empty(matrix_shape)
    counter = 0

    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            if i == 0 and j == 0:
                tile_coord_grid[i, j] = (i+BORDER_SIZE, j+BORDER_SIZE)
            elif i == 0:
                tile_coord_grid[i, j] = (i+BORDER_SIZE, (BORDER_SIZE+tile_height)*j+BORDER_SIZE)
            elif j == 0:
                tile_coord_grid[i, j] = ((BORDER_SIZE+tile_width)*i+BORDER_SIZE, j+BORDER_SIZE)
            else:
                # Another border_size--after it's done calculating the coordinates--to shift things
                tile_coord_grid[i, j] = ((BORDER_SIZE+tile_width)*i+BORDER_SIZE, (BORDER_SIZE+tile_height)*j+BORDER_SIZE)
            
            tmp_x, tmp_y = tile_coord_grid[i, j]
            raw_matrix[counter][0] = tmp_x
            raw_matrix[counter][1] = tmp_y
            raw_matrix[counter][2] = tmp_x+tile_width
            raw_matrix[counter][3] = tmp_y+tile_height
            counter += 1



    # print(tile_coord_grid)
    # print(raw_matrix.dtype)
    return tile_coord_grid, raw_matrix
            


def draw_tile(x, y, color, border_color, num_tiles_x=6, num_tiles_y=6, border_thickness=1):
    # Draw the outer rectangle (border)


    w, h = calc_true_res(num_tiles_x, num_tiles_y)

    tile_width = w//num_tiles_x
    tile_height = h//num_tiles_y
    
    # Draw the inner rectangle (main tile)
    # pygame.draw.rect(screen, color, (x+border_thickness//2, y+border_thickness//2, tile_width-border_thickness, tile_height-border_thickness))


    pygame.draw.rect(screen, color, (x, y, tile_width, tile_height))


def main():

    running = True
    y_position = SCREEN_HEIGHT - TILE_SIZE
    x_position = random.randint(0, SCREEN_WIDTH - TILE_SIZE)
    num_tiles = 6
    tile_grid,rm = tile_array(num_tiles, num_tiles)

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x,y)

                # Condition that returns which tile was clicked by the mouse
                print(rm[(rm[:, 0] < x) & (x <= rm[:, 2]) & (rm[:, 1] < y) & (y <= rm[:, 3])])


                print("Don't Tap!")
                    # y_position = SCREEN_HEIGHT - TILE_SIZE
                    # x_position = random.randint(0, SCREEN_WIDTH - TILE_SIZE)
                    # running = False

        screen.fill(BROWN)
        for i in range(num_tiles):
            for j in range(num_tiles):
                x_pos, y_pos = tile_grid[i, j]
                draw_tile(x_pos, y_pos, RED, BLACK, num_tiles)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
