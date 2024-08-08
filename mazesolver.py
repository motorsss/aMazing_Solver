from tkinter import Tk, BOTH, Canvas
from colors import *
import random
import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=5
        )

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("aMazing Solver")
        self.canvas = Canvas(self.__root, bg="PaleTurquoise1", width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
        self.__root.destroy()

    def draw_line(self, line, fill_color=colorme()):
        line.draw(self.canvas, fill_color)

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, colorme())
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "PaleTurquoise1")

        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, colorme())
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "PaleTurquoise1")

        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, colorme())
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "PaleTurquoise1")

        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, colorme())
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "PaleTurquoise1")

    def draw_move(self, to_cell, undo=False):

        line_color = colorme() if not undo else "gray"

        self._win.canvas.create_line(
                (self._x1 + self._x2)//2, (self._y1 + self._y2)//2,
                (to_cell._x1 + to_cell._x2)//2,(to_cell._y1 + to_cell._y2)//2,
                fill=line_color, width = 24
        )

    def mark_visited(self):
        offset = int(min(abs(self._x2 - self._x1),abs(self._y2 - self._y1))*.33)
        if self.visited is True:
            self._win.canvas.create_rectangle(
                self._x1+offset , self._y1+offset, self._x2-offset, self._y2-offset,
                fill="goldenrod1", outline="black",
            ),
        else:
            self._win.canvas.create_rectangle(
                self._x1+offset , self._y1+offset, self._x2-offset, self._y2-offset,
                fill="PaleTurquoise1", outline="PaleTurquoise1",
            ),
        self._win.redraw()




class Maze:
    def __init__(
            self,
            mazex,
            mazey,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None, seed=None
        ):
        self._mazex = mazex
        self._mazey = mazey
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is not None: random.seed(seed)

        self._create_cells()


    def _create_cells(self):
        self._cells = []
        for cols in range(self._num_cols):
            rowlist = []
            for row in range(self._num_rows):
                rowlist.append(Cell(self._win))
            self._cells.append(rowlist)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j, offset=7):
        if self._win is None:
            return
        x1 = -offset+self._mazex + i * self._cell_size_x
        y1 = -offset+self._mazey + j * self._cell_size_y
        x2 = offset+x1 + self._cell_size_x
        y2 = offset+y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)

        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.001)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)

    def _wallbreaker(self, i=0, j=0):

        self._cells[i][j].visited = True

        while True:
            visitable = []
            if i > 0 and self._cells[i-1][j].visited is False:
                visitable.append([i-1, j])

            if i < self._num_cols-1 and self._cells[i+1][j].visited is False:
                visitable.append([i+1, j])

            if j > 0 and self._cells[i][j-1].visited is False:
                visitable.append([i, j-1])

            if j < self._num_rows-1 and self._cells[i][j+1].visited is False:
                visitable.append([i, j+1])

            if len(visitable) == 0:
                return
            visiting = random.choice(visitable)

            if visiting[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._draw_cell(i, j)
                self._cells[i + 1][j].has_left_wall = False
                self._draw_cell(i+1, j)


            if visiting[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._draw_cell(i, j)
                self._cells[i - 1][j].has_right_wall = False
                self._draw_cell(i-1, j)

            if visiting[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._draw_cell(i, j)
                self._cells[i][j + 1].has_top_wall = False
                self._draw_cell(i, j+1)

            if visiting[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._draw_cell(i, j)
                self._cells[i][j - 1].has_bottom_wall = False
                self._draw_cell(i, j-1)

            self._wallbreaker(visiting[0],visiting[1])

    def _reset_cells_visited(self):
        for cols in self._cells:
            for cell in cols:
                cell.visited = False




