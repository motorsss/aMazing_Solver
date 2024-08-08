from mazesolver import *

def main():
    num_rows = 30
    num_cols = 30
    margin = 10
    screen_x = 2100
    screen_y = 2100
    seed = None
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed)
    maze._break_entrance_and_exit()
    maze._wallbreaker()

    for rows in maze._cells:
        for cols in rows:
            cols.mark_visited()

    maze._reset_cells_visited()

    for rows in maze._cells:
        for cols in rows:
            cols.mark_visited()

    win.wait_for_close()

main()