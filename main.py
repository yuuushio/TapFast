import pygame
import numpy as np
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

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
    # There are `num_tiles - 1` borders *between* the tiles. 
    #  Then +1 border on right and +1 border on the left
    #  == width - ((nx - 1)*bs + 2*bs)
    #  == " - bs(nx+1)
    # This ensures that the true w/h are accurate--avoiding calculating for
    #  edge-cases when calculating coordinates/position of tiles with their borders.
    w = SCREEN_WIDTH - (nx + 1) * BORDER_SIZE
    h = SCREEN_HEIGHT - (ny + 1) * BORDER_SIZE
    return (w, h)

def tile_array(num_tiles_x=4, num_tiles_y=4):
    # initial matrix which calculates and stores the x,y coordinates of each tile
    tile_coord_grid = np.empty((num_tiles_x, num_tiles_y), dtype=object)
    w, h = calc_true_res(num_tiles_x, num_tiles_y)

    tile_width = w//num_tiles_x
    tile_height = h//num_tiles_y

    

    # Calculate the total width occupied by the tiles and the borders combined.
    total_tile_width = tile_width * num_tiles_x + BORDER_SIZE * (num_tiles_x + 1)

    # Calculate the width error--difference between the screen width
    # and the total width occupied by the tiles and borders.
    # This error represents the number of pixels that are left out due to rounding down.
    width_error = SCREEN_WIDTH - total_tile_width

    total_tile_height = tile_height * num_tiles_y + BORDER_SIZE * (num_tiles_y + 1)
    height_error = SCREEN_HEIGHT - total_tile_height


    num_rows = num_tiles_x*num_tiles_y

    # columns: x, y, x_end, y_end, time_clicked
    matrix_shape = (num_rows, 4)

    # Cool idea: use matrix--instead of objects--to keep track of individual tile
    #  properties; mainly, its x,y coordinates, and the area it occupies.
    raw_matrix = np.empty(matrix_shape)

    # Keeping track of row
    counter = 0

    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            # `i/j * (width/height + border_size)` is used to calculate the tile position
            #   with its right border.
            # And then we shift (the x/y position) by another BORDER_SIZE to 
            #  add the left-border to current tile.
            x = i * (tile_width + BORDER_SIZE) + BORDER_SIZE
            y = j * (tile_height + BORDER_SIZE) + BORDER_SIZE

            # Distribute the width error across the tiles.
            # If the current tile's index (i) is less than the width error, 
            # add an extra pixel to its x position.
            # This effectively spreads the error pixels across the first few tiles.
            if i < width_error:
                x += i
            else:
                # Once all error pixels are distributed, add the total width error
                # to the x position of the remaining tiles.
                # This ensures that all tiles are positioned correctly.
                x += width_error


            # Distribute the height error across the tiles.
            # If the current tile's index (j) is less than the height error, 
            # add an extra pixel to its y position.
            if j < height_error:
                y += j
            else:
                # Once all error pixels are distributed, add the total height error
                # to the y position of the remaining tiles.
                y += height_error

            tile_coord_grid[i, j] = (x, y)
            
            tmp_x, tmp_y = tile_coord_grid[i, j]
            raw_matrix[counter][0] = tmp_x
            raw_matrix[counter][1] = tmp_y
            raw_matrix[counter][2] = tmp_x+tile_width
            raw_matrix[counter][3] = tmp_y+tile_height
            counter += 1



    # print(tile_coord_grid)
    # print(raw_matrix.dtype)
    return tile_coord_grid, raw_matrix
            


def draw_tile(x, y, color, border_color, num_tiles_x=4, num_tiles_y=4, border_thickness=1):
    # Draw the outer rectangle (border)


    w, h = calc_true_res(num_tiles_x, num_tiles_y)

    tile_width = w//num_tiles_x
    tile_height = h//num_tiles_y
    

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
    num_tiles = 10
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

                if len(clicked_tile) != 0: 
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
            draw_tile(x_pos, y_pos, color, BLACK, num_tiles,num_tiles)

            sub_counter += 1
        

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
