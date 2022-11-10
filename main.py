import math
import time
import Etat
import pygame
import Noeud
from Search import Search
from collections import deque

from pygame import mixer

# for music background
mixer.init()

mixer.music.load('./assets/music/8bit.mp3')

mixer.music.set_volume(0.6)

mixer.music.play(loops=-1)


# fonts
pygame.font.init()



# Player
IMAGES = {
    "U": "./assets/Player/dwight.png",
    "D": "./assets/Player/dwight.png",
    "L": "./assets/Player/dwight.png",
    "R": "./assets/Player/dwight.png",
}

# Environement

CASES = {
    "R":   "./assets/Ground/ground_06.png",
    "O":   "./assets/Blocks/block_04.png",
    " ":   "./assets/Ground/ground_01.png",
    "S":   "./assets/Ground/ground_03.png",
    "B":   "./assets/Crates/crate_05.png",
    "*":   "./assets/Crates/crate_40.png",
    "D":    "./assets/Environment/cross.png"
}


board = [
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", " ", " ", " ", "O", "O"],
    ["O", ".", " ", "B", " ", " ", "O", "O"],
    ["O", "O", "O", " ", "B", " ", "O", "O"],
    ["O", "S", "O", "O", " ", " ", "O", "O"],
    ["O", " ", "O", " ", "S", " ", "O", "O"],
    ["O", "B", " ", "*", "B", "B", "S", "O"],
    ["O", " ", " ", " ", "S", " ", " ", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
]

board1 = [
    ['O', 'O', 'O', 'O', 'O', 'O'],
          ['O', 'S', ' ', 'B', ' ', 'O'],
          ['O', ' ', 'O', 'R', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O']]

board2 = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
          ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
          ['O', ' ', ' ', 'O', 'O', 'O', ' ', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'O', '.', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
          ['O', ' ', ' ', 'B', ' ', ' ', 'O', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board3 = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
          ['O', ' ', ' ', ' ', 'O', ' ', ' ', 'O'],
          ['O', ' ', ' ', 'B', 'R', ' ', ' ', 'O'],
          ['O', ' ', ' ', ' ', 'O', 'B', ' ', 'O'],
          ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
          ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board4 = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
          ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
          ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
          ['O', 'O', ' ', '*', ' ', ' ', 'O'],
          ['O', 'O', 'B', 'O', 'B', ' ', 'O'],
          ['O', ' ', 'S', 'R', 'S', ' ', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'O', 'O'],
          ['O', 'O', 'O', ' ', ' ', 'O', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O', 'O']]

board5 = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
          ['O', 'O', 'O', 'S', 'O', ' ', ' ', 'O', 'O'],
          ['O', ' ', ' ', ' ', ' ', 'B', ' ', 'O', 'O'],
          ['O', ' ', 'B', ' ', 'R', ' ', ' ', 'S', 'O'],
          ['O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O'],
          ['O', 'O', 'O', 'B', 'O', ' ', 'O', 'O', 'O'],
          ['O', 'O', 'O', ' ', ' ', 'S', 'O', 'O', 'O'],
          ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board6 = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'S', ' ', 'O', ' ', 'R', 'O'],
    ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
    ['O', 'S', ' ', ' ', 'B', ' ', 'O'],
    ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
    ['O', 'S', ' ', 'O', ' ', ' ', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
]

board7 = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'S', 'S', 'S', ' ', 'O', 'O', 'O'],
    ['O', ' ', 'S', ' ', 'B', ' ', ' ', 'O'],
    ['O', ' ', ' ', 'B', 'B', 'B', ' ', 'O'],
    ['O', 'O', 'O', 'O', ' ', ' ', 'R', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
]

board8 = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', ' ', ' ', ' ', ' ', 'O', 'O', 'O'],
    ['O', ' ', ' ', ' ', 'B', ' ', ' ', 'O'],
    ['O', 'S', 'S', 'S', '*', 'B', 'R', 'O'],
    ['O', ' ', ' ', ' ', 'B', ' ', ' ', 'O'],
    ['O', ' ', ' ', ' ', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
]

board9 = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'S', ' ', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', ' ', ' ', 'O', 'O', 'O', 'O'],
    ['O', 'S', ' ', 'S', ' ', 'O', 'O', 'O', 'O'],
    ['O', ' ', 'B', ' ', 'B', 'B', ' ', ' ', 'O'],
    ['O', 'O', 'O', 'S', ' ', ' ', 'B', 'R', 'O'],
    ['O', 'O', 'O', ' ', ' ', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
]


# this function is used to print the board using pygame
def render_dynamic(surface, board_d, board_s, board_dead, orientation):
    legale_moves = {"B", "*"}
    
    # read dynamic matrix
    for row_index, row in enumerate(board_d):
        for col_index, column in enumerate(row):
            
            #determin size in pygame aka 64*64
            position_x = col_index*64
            position_y = row_index*64

            # implement map graphical assets with their assoiateive character
            asset = pygame.image.load(
                CASES[board_s[row_index][col_index]]).convert_alpha()
            surface.blit(asset, (position_x, position_y))

            if board_dead[row_index][col_index] == "D":
                asset = pygame.image.load(CASES["D"]).convert_alpha()
                surface.blit(asset, (position_x, position_y))

            if column == "R":
                asset = pygame.image.load(orientation).convert_alpha()
                surface.blit(asset, (position_x, position_y))
            elif column == "B" and board_s[row_index][col_index] == "S":
                asset = pygame.image.load(
                    CASES["*"]).convert_alpha()
                surface.blit(asset, (position_x, position_y))
            elif column in legale_moves:
                asset = pygame.image.load(
                    CASES[column]).convert_alpha()
                surface.blit(asset, (position_x, position_y))





#----------------------------------#

Launch = True
Menu = False
MenuAlgo = False
MenuHeur = True
Player = False
AI = True

FIRSTIME = True

# size of window
WIDTH = (len(board[0])+1)*64
HEIGHT = (len(board)+1)*64
surface = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame.RESIZABLE
surface.fill((0, 0, 0))


#color background

backColor = pygame.color.Color('#000000')

# window caption
pygame.display.set_caption("The Office Sokoban")

Algorithme = ""
heuristic = ""
orientation = IMAGES["D"]
k = 0
    
#----------------------------------#    

text_font = pygame.font.Font('./assets/fonts/Pixeltype.ttf', 50)

p = 1;


while Launch:
    
    surface.fill(backColor)
    pygame.display.flip()
    
    # player_stand = pygame.image.load('./assets/win.jpg').convert_alpha()
    # player_stand = pygame.transform.rotozoom(player_stand,0,2)
    # player_stand_rect = player_stand.get_rect(center = (400,200))
    
    
    while MenuHeur:
        asset = pygame.image.load(
            "./assets/Menu/g22.png").convert_alpha()
        asset = pygame.transform.scale(asset, (WIDTH, HEIGHT))
        surface.blit(asset, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Launch = False
                MenuHeur = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    heuristic = 1
                    MenuHeur = False
                    surface.fill((0, 0, 0))
                    pygame.display.flip()
                elif event.key == pygame.K_F2:
                    heuristic = 2
                    MenuHeur = False
                    surface.fill((0, 0, 0))
                    pygame.display.flip()
                elif event.key == pygame.K_F3:
                    heuristic = 3
                    MenuHeur = False
                    surface.fill((0, 0, 0))
                    pygame.display.flip()

    while AI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                AI = False
                Launch = False

        if FIRSTIME:
            boards = [board1, board2, board3, board4, board5]
            boards_new = [board6, board7, board8, board9, board]

            all_boards = boards
            all_boards.extend(boards_new)

            boards_used = all_boards

            FIRSTIME = False
            Game = Etat.SokoPuzzle(boards_used[k])
            init_node = Noeud.Node(Game)

            deb = time.time()
            if Algorithme == "BFS":
                node, step = Search.BFS(init_node)
            else:
                node, step = Search.AlgoTypeA(init_node, heuristic)
            fin = time.time()

            
            print(f"--Board {p}--")
            print(f"Steps: {step}")
            print(f"Moves : {node.executed_moves}")

            text = f"Steps : {step}    <<Board {p}>>    Time : {math.ceil(fin-deb)}s"
           
            text_render = text_font.render(text, False, (255, 255, 255))

            surface.blit(text_render, (10,600))
            pygame.display.flip()

            

            IA_moves = str(node.executed_moves)
            with open("Deroulement2.txt", "a") as fichier:
                fichier.write(f"--Board {p}-- \n Moves : {IA_moves} \n Step : {step} \n")

            IA_moves = [x for x in IA_moves]
            IA_moves = deque(IA_moves)

        if len(IA_moves) > 0:
            move = IA_moves.popleft()
            Game.do_move(move)
            orientation = IMAGES[move]
        else:
            FIRSTIME = True
            k += 1
            surface.fill((0, 0, 0))
            pygame.display.flip()
            p = p + 1
            Game = Etat.SokoPuzzle(boards_used[k])

        # ------------------------ RENDY PYGAME DE LA MAP DYNAMIQUE
        render_dynamic(surface, Game.board_d, Game.board_s,
                       Game.board_dead, orientation)
        # surface.blit(text_render, (0,0))
        pygame.display.flip()
        time.sleep(0.2)