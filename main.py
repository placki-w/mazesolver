from graphics import Window, Point, Line, Cell, Maze

def main():
    

    """
    #Points for lines, to draw in window
    point1 = Point(0,100)
    point2 = Point(300,10)

    line = Line(point1, point2)

    win.draw_line(line, 'black')

    c1 = Cell(win)
    c1.has_left_wall = False
    c1.draw(50, 50, 100, 100)

    c2 = Cell(win)
    c2.has_right_wall = False
    c2.draw(125, 125, 200, 200)

    c = Cell(win)
    c.has_bottom_wall = False
    c.draw(225, 225, 250, 250)

    c = Cell(win)
    c.has_top_wall = False
    c.draw(300, 300, 500, 500)

    c1.draw_move(c2) #mid points of two cells, connecting line
    """

    screen_x = 1000
    screen_y = 1000

    win = Window(screen_x, screen_y)

    num_rows = 8
    num_cols = 8
    margin = 50
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

    maze._reset_cells_visited()
    maze.solve()

    win.wait_for_close()


if __name__ == '__main__':
    main()