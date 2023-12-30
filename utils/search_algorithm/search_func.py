from .search import *
import pygame
import socket
import os
from pathlib import Path
import json
import time

HOST = socket.gethostbyname(socket.gethostname())
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
WORK_DIR = os.path.dirname(ROOT)

WIDTH = 800
ROWS = 111   



def time_complexity(func):
    def warp(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Time inference func {func.__name__}: {(time.time() - start):.3f} second')
        return result
    return warp

def simulation( width= WIDTH, rows = ROWS):

    win = pygame.display.set_mode((WIDTH, WIDTH))
    grid = make_grid(rows, width)

    start = None
    end = None
    barrier_arr = []
    run = True
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()
                    data_from_txt = read_txt_file()
                    for temp_data in data_from_txt:
                        spot = grid[temp_data[0]][temp_data[1]]
                        spot.make_barrier()
                        
                elif spot != end and spot != start:
                    spot.make_barrier()
                    temp_arr = [spot.row, spot.col] 
                    if temp_arr not in barrier_arr:
                        barrier_arr.append([spot.row, spot.col])

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # print(barrier_arr)
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    arr_path_finding = algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
                    print("Sucessful", arr_path_finding)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)

    pygame.quit()



def collect_barrier(show_mode=1, width=WIDTH, rows =  ROWS):
    if show_mode:
        win = pygame.display.set_mode((WIDTH, WIDTH))
    else:
        win = pygame.display.set_mode((WIDTH, WIDTH),flags=pygame.HIDDEN)
    grid = make_grid(ROWS, width)
    barrier_arr = []
    run = True
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.make_barrier()
                temp_arr = [spot.row, spot.col]
                if temp_arr not in barrier_arr:
                    barrier_arr.append(temp_arr)
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    write_txt_file(barrier_arr)
                    run = False
                            
                    # print(barrier_arr)
                if event.key == pygame.K_c:
                    grid = make_grid(ROWS, width)

def Astar_search(current_coor, target_coor, rows = ROWS, show_mode = 0, width = WIDTH):
    if show_mode:
        win = pygame.display.set_mode((WIDTH, WIDTH))
    else:
        win = pygame.display.set_mode((WIDTH, WIDTH),flags=pygame.HIDDEN)
    pygame.display.iconify()
    grid = make_grid(rows, width)
    start = grid[current_coor[0]][current_coor[1]]
    start.make_start()
    end = grid[target_coor[0]][target_coor[1]]
    end.make_end()
    barrier_from_txt = read_txt_file()
    for temp_data in barrier_from_txt:
        spot = grid[temp_data[0]][temp_data[1]]
        spot.make_barrier()
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

    arr_path_finding = algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
    print("Sucessful", arr_path_finding)
    pygame.quit()


if __name__ == "__main__":
    # collect_barrier()
    # simulation()
    Astar_search([0,0], [3,6])
    # print(WORK_DIR)