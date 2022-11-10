import numpy as np
from copy import deepcopy

# cette classe représente un etat du jeu , il change lorsque le joueur fait un mouvement(se deplace)


class SokoPuzzle:
    
    def __init__(self, board):
        
        # define matrix dimension (map)
        self.height = len(board)
        self.width = len(board[0])
        
        
        # generate static matrix that will represent solid objects
        
        self.board_s = self.create_matrix()
        self.board_d = self.create_matrix()
        
        # static element
        
        self.static = {"O"," ","S"}

        # the movements
        
        self.moves = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1)
        }        
        
        # the forbidden movements
        
        self.forbidden_moves = {"B", "O"}
        self.robot_pos = (3, 2)
        
        
        # split map into static and dynamic
        
        for i, line in enumerate(board):
            for j, element in enumerate(line):
                if element in self.static:
                    self.board_s[i][j] = element
                elif element == "R":
                    self.board_d[i][j] = element
                    self.robot_pos = (i, j)
                elif element == "S":
                    self.board_s[i][j] = element
                elif element == ".":
                    self.robot_pos = (i, j)
                    self.board_s[i][j] = "S"
                    self.board_d[i][j] = "R"
                elif element == "*":
                    self.board_d[i][j] = "B"
                    self.board_s[i][j] = "S"
                else:
                    self.board_s[i][j] = " "
                    self.board_d[i][j] = "B"
        
        # this will find dead locks aka positions where if a cube is there it means game over .
        self.board_dead = self.create_deadlock()
        
        
    # function that calculate player new position in the map
        
    def direction(self, tuples):
        
        #get actual position
        r_x, r_y = self.robot_pos
        
        #add the movement (tuple) to get new position
        r_x += tuples[0]
        r_y += tuples[1]
        
        # if there is a wall in new position then cant execute move
        if self.board_s[r_x][r_y] == "O":
            return False
        # if there isnt a cube then do move normally
        elif self.board_d[r_x][r_y] != "B":
            self.robot_pos = (r_x, r_y)
            self.board_d[r_x][r_y] = "R"
            self.board_d[r_x-tuples[0]][r_y-tuples[1]] = " "
            return True
        #if there is cube but after it a wall
        elif self.board_d[r_x+tuples[0]][r_y+tuples[1]] != "B" and self.board_s[r_x+tuples[0]][r_y+tuples[1]] != "O":
            self.robot_pos = (r_x, r_y)
            self.board_d[r_x-tuples[0]][r_y-tuples[1]] = " "
            self.board_d[r_x][r_y] = "R"
            self.board_d[r_x+tuples[0]][r_y+tuples[1]] = "B"

            return True

        return False
        
        
    def is_deadlock(self):
        dynamic_board = np.array(self.board_d)
        bx, by = np.where(dynamic_board == "B")

        for x, y in zip(bx, by):
            if self.board_dead[x][y] == "D":
                return True

        return False    
        
        
    # dunction that create matrix full of deadlocks
    def create_deadlock(self):
        board_dead = self.create_matrix()
        for i in range(1, len(self.board_s)-1):
            for j in range(1, len(self.board_s[0])-1):
                if self.is_corner_deadlock(i, j):
                    board_dead[i][j] = "D"

        board_dead = self.detect_line_dead_lock(board_dead)
        return board_dead    
        
        
    # dtetect middle dead locks
    def detect_line_dead_lock(self, board_dead):

        dont_verif = {"S", "O"}

        left_line = True
        right_line = True
        top_line = True
        bottom_line = True

        corners_dead_locks = np.array(board_dead)
        dx, dy = np.where(corners_dead_locks == "D")
        new_dx = dx[1:]
        new_dy = dy[1:]

        for indice_x, indice_y in zip(dx, dy):
            for indice_i, indice_j in zip(new_dx, new_dy):
                if indice_i == indice_x and indice_j != indice_y:

                    counter = indice_y
                    counter_deb = indice_j

                    if indice_j > indice_y:
                        counter = indice_j
                        counter_deb = indice_y

                    for col in range(counter):
                        if self.board_s[indice_x][col] not in dont_verif:
                            if self.board_s[indice_x+1][col] != "O":
                                bottom_line = False
                            if self.board_s[indice_x-1][col] != "O":
                                top_line = False

                    i_can_add = True
                    if bottom_line or top_line:
                        for j in range(counter_deb, counter):
                            if self.board_s[indice_x][j] in dont_verif:
                                i_can_add = False

                        for j in range(counter_deb, counter):
                            if i_can_add and self.board_s[indice_x][j] not in dont_verif:
                                board_dead[indice_x][j] = "D"

                if indice_j == indice_y and indice_i != indice_x:
                    counter = indice_x
                    counter_deb = indice_i
                    if indice_i > indice_x:
                        counter = indice_i
                        counter_deb = indice_x

                    for row in range(counter):
                        if self.board_s[row][indice_y] not in dont_verif:
                            if self.board_s[row][indice_y+1] != "O":
                                right_line = False
                            if self.board_s[row][indice_y-1] != "O":
                                left_line = False

                    i_can_add = True

                    if left_line or right_line:
                        for i in range(counter_deb, counter):
                            if self.board_s[i][indice_y] in dont_verif:
                                i_can_add = False

                        for i in range(counter_deb, counter):
                            if i_can_add and self.board_s[i][indice_y] not in dont_verif:
                                board_dead[i][indice_y] = "D"

            left_line = True
            right_line = True
            top_line = True
            bottom_line = True

        return board_dead
    
    
    # dtetect corner dead locks
    def is_corner_deadlock(self, x, y):

        dont_verif = {"S", "O"}
        horizontal_move = False
        vertical_move = False

        if self.board_s[x][y] not in dont_verif:
            if self.board_s[x+1][y] == "O" or self.board_s[x-1][y] == "O":
                horizontal_move = True
            if self.board_s[x][y+1] == "O" or self.board_s[x][y-1] == "O":
                vertical_move = True

        return horizontal_move and vertical_move

        
    # confirms the objects node
    def is_goal(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board_s[i][j] == "S" and self.board_d[i][j] != "B":
                    return False

        return True


    # Function That does the movements
    def do_move(self, m):
        return self.direction(self.moves[m])


    # Function That does show deadlocks aka positions where cube shouldnt be there
    def show_deadlock_map(self):
        print("**********************")
        for line_d, line_s in zip(self.board_dead, self.board_s):
            for col_d, col_s in zip(line_d, line_s):
                if col_d == ' ':
                    print(col_s, end=" ")
                else:
                    print(col_d, end=" ")
            print("\n")
    
    
    
    # Function That show the matrixes (map/states)
    def show_matrix(self):
        print("**********************")
        for line_d, line_s in zip(self.board_d, self.board_s):
            for col_d, col_s in zip(line_d, line_s):
                if col_d == ' ':
                    print(col_s, end=" ")
                else:
                    print(col_d, end=" ")
            print("\n")    
        
      
        
        
    # function that generate an empty matrix (filled with spaces)
    def create_matrix(self):
        mat = []
        for _ in range(self.height):
            line = []
            for _ in range(self.width):
                line.append(' ')
            mat.append(line)
        return mat