from classes import *
import time
import sys

def main():
    num_rows = random.randint(20, 60)
    num_cols = random.randint(20, 60)
    margin = 10
    screen_x = 2000
    screen_y = 2000
    seed = None
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)
    sys.setrecursionlimit(10000)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed)
    maze.solve()
    win.wait_for_close()

main()
