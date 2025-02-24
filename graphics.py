from tkinter import Tk, BOTH, Canvas
import time, random


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg="white")
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running_status = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running_status = True
        while self.__running_status:
            self.redraw()
        print('Window closed...')
    
    def close(self):
        self.__running_status = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    #(0,0 is the top left of the screen)

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
        )

        
class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
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
            self._win.draw_line(line, 'black')
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, 'white')
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, 'black')
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, 'white')
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, 'black')
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, 'white')
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, 'black')
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, 'white')

    def draw_move(self, to_cell, undo=False):
        self_x = (self._x1 + self._x2) / 2
        self_y = (self._y1 + self._y2) / 2
        target_x = (to_cell._x1 + to_cell._x2) / 2 
        target_y = (to_cell._y1 + to_cell._y2) / 2

        line = Line(Point(self_x, self_y), Point(target_x, target_y))
        if undo:
            self._win.draw_line(line, 'gray')
        else:
            self._win.draw_line(line, 'red')


class Maze:
    def __init__(
    self,
    x1,
    y1,
    num_rows,
    num_cols,
    cell_size_x,
    cell_size_y,
    win=None,
    seed=None
):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
    
    def _create_cells(self):
        
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                item = Cell(self._win)
                column.append(item)
            self._cells.append(column)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = self._x1 + (i + 1) * self._cell_size_x
        y2 = self._y1 + (j + 1) * self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._num_cols -1 ,self._num_rows - 1 )

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            # Check right
            if (i + 1) < self._num_cols and not self._cells[i+1][j].visited:
                to_visit.append(('right', i+1, j))
            # Check bottom
            if (j + 1) < self._num_rows and not self._cells[i][j+1].visited:
                to_visit.append(('bottom', i, j+1))
            # Check left
            if (i-1) >= 0 and not self._cells[i-1][j].visited:
                to_visit.append(('left', i-1, j))
            # Check top
            if (j-1) >= 0 and not self._cells[i][j-1].visited:
                to_visit.append(('top', i, j-1))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            else:
                rando_pick = random.randrange(0,len(to_visit))
                if to_visit[rando_pick][0] == 'right':
                    self._cells[i][j].has_right_wall = False
                    self._cells[to_visit[rando_pick][1]][to_visit[rando_pick][2]].has_left_wall = False
                if to_visit[rando_pick][0] == 'bottom':
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[to_visit[rando_pick][1]][to_visit[rando_pick][2]].has_top_wall = False
                if to_visit[rando_pick][0] == 'top':
                    self._cells[i][j].has_top_wall = False
                    self._cells[to_visit[rando_pick][1]][to_visit[rando_pick][2]].has_bottom_wall = False
                if to_visit[rando_pick][0] == 'left':
                    self._cells[i][j].has_left_wall = False
                    self._cells[to_visit[rando_pick][1]][to_visit[rando_pick][2]].has_right_wall = False
                self._break_walls_r(to_visit[rando_pick][1], to_visit[rando_pick][2])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r( i=0, j=0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if (i, j) == (self._num_cols - 1, self._num_rows - 1):
            return True
        # Check right
        if (i + 1) < self._num_cols and self._cells[i][j].has_right_wall == False and not self._cells[i+1][j].visited:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            right = self._solve_r(i=i+1, j=j)
            if right:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
        # Check bottom
        if (j + 1) < self._num_rows and self._cells[i][j].has_bottom_wall == False and not self._cells[i][j+1].visited:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            bottom = self._solve_r(i=i, j=j+1)
            if bottom:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        # Check left
        if (i-1) >= 0 and self._cells[i][j].has_left_wall == False and not self._cells[i-1][j].visited:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            left = self._solve_r(i=i-1, j=j)
            if left:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        # Check top
        if (j-1) >= 0 and self._cells[i][j].has_top_wall == False and not self._cells[i][j-1].visited:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            top = self._solve_r(i=i, j=j-1)
            if top:
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)

        return False