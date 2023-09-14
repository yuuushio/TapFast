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
hl_tile = {}

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
    # columns: x,y,x_end,y_end,time_clicked
    matrix_shape = (num_rows, 4)

    # Cool idea: use matrix--instead of objects--to keep track of individual tile
    #  properties; mainly, its x,y coordinates, and the area it occupies.
    raw_matrix = np.empty(matrix_shape)
    # Keeping track of row
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

# Utility function to get the index/position of the clicked tile
def get_tile_index(rm, ct):
    index = 0
    for tile in rm:
        # check if x,y match
        if ct[0] == tile[0] and ct[1] == tile[1]:
            return index
        else:
            index += 1

def random_tiles(arr_len, clicked_set, intensity):
    selection = set(range(arr_len)) - clicked_set
    return random.sample(list(selection), intensity)


def left_over_random(arr_len, initial_random_indexes, clicked_set, intensity):
    # take away the clicked indexes from the population
    selection = list(set(range(arr_len)) - clicked_set)

    # how many number of tiles do we need to calculate:
    rm_intensity = intensity - len(set(initial_random_indexes) - clicked_set)
    return list(set(initial_random_indexes) - clicked_set) + random.sample(selection, rm_intensity)


def main():

    running = True
    num_tiles = 6
    tile_grid,rm = tile_array(num_tiles, num_tiles)
    intensity = 6
    clicked_stack = set()
    rand_indexes = random_tiles(rm.shape[0], clicked_stack, intensity)

    while running:
        clicked_tile = None
        screen.fill(WHITE)
        current_time = pygame.time.get_ticks()
        # print(rm.shape)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x,y)

                # Condition that returns which tile was clicked by the mouse
                clicked_tile = rm[(rm[:, 0] <= x) & (x <= rm[:, 2]) & (rm[:, 1] <= y) & (y <= rm[:, 3])]
                index = get_tile_index(rm, clicked_tile[0])

                clicked_stack.add(index)

                # Map the clicked time index with the time it was clicked at
                hl_tile[index] = current_time

                print("Don't Tap!")

        screen.fill(BROWN)
        sub_counter = 0 # tile index counter

        if len(clicked_stack) != 0:
            rand_indexes = left_over_random(rm.shape[0], rand_indexes, clicked_stack, intensity)
            clicked_stack.clear()

        for tile in rm:
            color = WHITE
            x_pos, y_pos = tile[0], tile[1]
            # if sub_counter in hl_tile and current_time - hl_tile[sub_counter] < 100:
            #     color = BLACK
            if sub_counter in rand_indexes:
                color = BLACK
            draw_tile(x_pos, y_pos, color, BLACK, num_tiles)

            sub_counter += 1
        

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
