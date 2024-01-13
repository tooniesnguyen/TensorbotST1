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

WIDTH = 1000
ROWS = 110   



def time_complexity(func):
    def warp(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Time inference func {func.__name__}: {(time.time() - start):.3f} second')
        return result
    return warp

def simulation(width= WIDTH, rows = ROWS):
    global arr_path_finding

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
                    print("Point corrdinate: ", spot.row, spot.col)
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
                    # print("Sucessful", arr_path_finding)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)

    pygame.quit()



def collect_barrier(show_mode=1, width=WIDTH, rows =  ROWS, reload_barr = False):
    if show_mode:
        win = pygame.display.set_mode((WIDTH, WIDTH))
    else:
        win = pygame.display.set_mode((WIDTH, WIDTH),flags=pygame.HIDDEN)
    grid = make_grid(ROWS, width)
    barrier_arr = []
    if reload_barr:
        data_from_txt = read_txt_file()
        barrier_arr = data_from_txt
        for temp_data in data_from_txt:
            spot = grid[temp_data[0]][temp_data[1]]
            spot.make_barrier()
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
                spot.make_barrier()
                temp_arr = [spot.row, spot.col]
                if temp_arr not in barrier_arr:
                    barrier_arr.append(temp_arr)
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                arr_to_remove=[spot.row, spot.col]
                barrier_arr = [item for item in barrier_arr if item != arr_to_remove] 
                spot.reset()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    write_txt_file(barrier_arr)
                    run = False
                            
                    # print(barrier_arr)
                if event.key == pygame.K_c:
                    grid = make_grid(ROWS, width)

def Astar_search(current_coor, target_coor, barrier_arr, rows = ROWS, show_mode = 0, width = WIDTH):
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
    for temp_data in barrier_arr:
        spot = grid[temp_data[0]][temp_data[1]]
        spot.make_barrier()
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)

    arr_path_finding = algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
    arr_path_finding.append(tuple(target_coor))
    # print("Sucessful", arr_path_finding)
    pygame.quit()
    return arr_path_finding


if __name__ == "__main__":
    barrier_from_txt = read_txt_file()

    collect_barrier(reload_barr=True)
    # simulation()
    # print(Astar_search([0,17], [5,28],barrier_from_txt))
    # print(WORK_DIR)