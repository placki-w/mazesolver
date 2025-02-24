import unittest

from graphics import Maze, Cell

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

    def test_reset_visited_cells(self):
        m1 = Maze(0,0,10,10, 50, 50)
        m1._cells[0][0].visited = True
        m1._cells[4][2].visited = True

        m1._reset_cells_visited()

        for i in range(m1._num_cols):
            for j in range(m1._num_rows):
                self.assertFalse(m1._cells[i][j].visited)

if __name__ == "__main__":
    unittest.main()