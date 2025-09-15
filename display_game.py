from threading import Thread
import os
from level import Level
import pygame
import copy
from levelsTested import testedLevels
# from boxxle2 import boxxle2
from build_game import *
from dfs import *
from bfs import *
from manhattanStar  import *
from results_db import save_result
import time
# from main import startScreen

APP_FOLDER = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'assets'

# Facteur d'échelle et taille des tuiles
SCALE_FACTOR = 2
TILE_SIZE = 32 * SCALE_FACTOR

pygame.init()

# Chargement des images avec mise à l'échelle
icon = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "icon.png")), (64, 64))
# aStarBtn = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "aStarBtn.png")), (58 * SCALE_FACTOR, 23 * SCALE_FACTOR))
bfsBtn = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "bfsBtn.png")),  (58 * SCALE_FACTOR, 23 * SCALE_FACTOR))
dfsBtn = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "dfsBtn.png")),  (58 * SCALE_FACTOR, 23 * SCALE_FACTOR))
undoBtn = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "undoBtn.png")),  (58 * SCALE_FACTOR, 23 * SCALE_FACTOR))
resetBtn = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "resetBtn.png")),  (58 * SCALE_FACTOR, 23 * SCALE_FACTOR))
quitBtn = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "quitBtn.png")),  (58 * SCALE_FACTOR, 23 * SCALE_FACTOR))
homeBtn = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "homeBtn.png")),  (58 * SCALE_FACTOR, 23 * SCALE_FACTOR))


PLAYER_MOVE_DELAY = 150  # par défaut, en millisecondes

crate = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "crate.png")), (TILE_SIZE, TILE_SIZE))
treasure = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "treasure.png")), (TILE_SIZE, TILE_SIZE))

wb = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
wl = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
wr = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
wt = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
wlt = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
wlb = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
wrt = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
wrb = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
wtb = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
wlr = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
w3l = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
w3r = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
w3t = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
w3b = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
w4 = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "wall.png")), (TILE_SIZE, TILE_SIZE))
charS = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "charS.png")), (TILE_SIZE, TILE_SIZE))

tl = (
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "tl1.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "tl2.png")), (TILE_SIZE, TILE_SIZE))
)
td = (
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "td1.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "td2.png")), (TILE_SIZE, TILE_SIZE))
)
tls = (
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "tls1.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "tls2.png")), (TILE_SIZE, TILE_SIZE))
)
tds = (
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "tds1.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "tds2.png")), (TILE_SIZE, TILE_SIZE))
)
coin = (
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "c1.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "c2.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "c3.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "c4.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "c5.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "c6.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "c7.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "c8.png")), (TILE_SIZE, TILE_SIZE))
)
char = (
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "char1.png")), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "char2.png")), (TILE_SIZE, TILE_SIZE))
)

clock = pygame.time.Clock()

levels = []
levelIndex = -1
animPtr = 0
speed_label = "Normale"  # Valeur par défaut


def render(currLevel, screen):
    '''
    Cette fonction aide à rendre chaque élément à l'écran. Elle calcule la valeur en pixels de chaque élément et le blit à sa position appropriée.
    '''
    x = (800 - TILE_SIZE * currLevel.rows) // 2
    for i in range(0, currLevel.rows):
        y = (932 - TILE_SIZE * currLevel.cols) // 2
        for j in range(0, currLevel.cols):
            if currLevel.matrix[i][j] == 1:
                wallType = wallFreeFaces(currLevel.matrix, (i, j))
                if len(wallType) == 1:
                    if (i + j) % 2 == 0:
                        screen.blit(td[(i * j) % 2], (y, x))
                    else:
                        screen.blit(tl[(i * j) % 2], (y, x))
                    if (0, 1) in wallType:
                        screen.blit(wl, (y, x))
                    elif (0, -1) in wallType:
                        screen.blit(wr, (y, x))
                    elif (1, 0) in wallType:
                        screen.blit(wt, (y, x))
                    elif (-1, 0) in wallType:
                        screen.blit(wb, (y, x))
                elif len(wallType) == 2:
                    if (i + j) % 2 == 0:
                        screen.blit(td[(i * j) % 2], (y, x))
                    else:
                        screen.blit(tl[(i * j) % 2], (y, x))
                    if (0, 1) in wallType:
                        if (1, 0) in wallType:
                            screen.blit(wlt, (y, x))
                        elif (-1, 0) in wallType:
                            screen.blit(wlb, (y, x))
                        else:
                            screen.blit(wtb, (y, x))
                    elif (0, -1) in wallType:
                        if (1, 0) in wallType:
                            screen.blit(wrt, (y, x))
                        elif (-1, 0) in wallType:
                            screen.blit(wrb, (y, x))
                    else:
                        screen.blit(wlr, (y, x))
                elif len(wallType) == 3:
                    if (i + j) % 2 == 0:
                        screen.blit(td[(i * j) % 2], (y, x))
                    else:
                        screen.blit(tl[(i * j) % 2], (y, x))
                    if (0, 1) not in wallType:
                        screen.blit(w3r, (y, x))
                    elif (0, -1) not in wallType:
                        screen.blit(w3l, (y, x))
                    elif (1, 0) not in wallType:
                        screen.blit(w3b, (y, x))
                    elif (-1, 0) not in wallType:
                        screen.blit(w3t, (y, x))
                elif len(wallType) == 4:
                    if (i + j) % 2 == 0:
                        screen.blit(td[(i * j) % 2], (y, x))
                    else:
                        screen.blit(tl[(i * j) % 2], (y, x))
                    screen.blit(w4, (y, x))
            elif currLevel.matrix[i][j] == 5:
                if (i + j) % 2 == 0:
                    if currLevel.matrix[i - 1][j] == 1:
                        screen.blit(tds[(i * j) % 2], (y, x))
                    else:
                        screen.blit(td[(i * j) % 2], (y, x))
                else:
                    if currLevel.matrix[i - 1][j] == 1:
                        screen.blit(tls[(i * j) % 2], (y, x))
                    else:
                        screen.blit(tl[(i * j) % 2], (y, x))
                screen.blit(treasure, (y, x))
            elif currLevel.matrix[i][j] == 2:
                if (i + j) % 2 == 0:
                    if currLevel.matrix[i - 1][j] == 1:
                        screen.blit(tds[(i * j) % 2], (y, x))
                    else:
                        screen.blit(td[(i * j) % 2], (y, x))
                else:
                    if currLevel.matrix[i - 1][j] == 1:
                        screen.blit(tls[(i * j) % 2], (y, x))
                    else:
                        screen.blit(tl[(i * j) % 2], (y, x))
                if currLevel.playerY == i - 1 and currLevel.playerX == j:
                    screen.blit(charS, (y, x))
                screen.blit(coin[animPtr % 8], (y, x))
            elif currLevel.matrix[i][j] == 3:
                if (i + j) % 2 == 0:
                    if currLevel.matrix[i - 1][j] == 1:
                        screen.blit(tds[(i * j) % 2], (y, x))
                    else:
                        screen.blit(td[(i * j) % 2], (y, x))
                else:
                    if currLevel.matrix[i - 1][j] == 1:
                        screen.blit(tls[(i * j) % 2], (y, x))
                    else:
                        screen.blit(tl[(i * j) % 2], (y, x))
                screen.blit(crate, (y, x))
            elif currLevel.matrix[i][j] == 0:
                if (i + j) % 2 == 0:
                    if currLevel.matrix[i - 1][j] == 1:
                        screen.blit(tds[(i * j) % 2], (y, x))
                    else:
                        screen.blit(td[(i * j) % 2], (y, x))
                else:
                    if currLevel.matrix[i - 1][j] == 1:
                        screen.blit(tls[(i * j) % 2 - 1], (y, x))
                    else:
                        screen.blit(tl[(i * j) % 2], (y, x))
                if currLevel.playerY == i - 1 and currLevel.playerX == j:
                    screen.blit(charS, (y, x))
            if currLevel.playerX == j and currLevel.playerY == i:
                screen.blit(char[animPtr % 2], (y, x))
            y += TILE_SIZE
        x += TILE_SIZE
    screen.blit(bfsBtn, (105 * SCALE_FACTOR, 360 * SCALE_FACTOR))
    # screen.blit(aStarBtn, (135 * SCALE_FACTOR, 360 * SCALE_FACTOR))
    screen.blit(dfsBtn, (185 * SCALE_FACTOR, 360 * SCALE_FACTOR))

    # New buttons
    screen.blit(undoBtn, (265 * SCALE_FACTOR, 360 * SCALE_FACTOR))
    screen.blit(resetBtn, (345 * SCALE_FACTOR, 360 * SCALE_FACTOR))
    screen.blit(quitBtn, (425 * SCALE_FACTOR, 360 * SCALE_FACTOR))
    screen.blit(homeBtn, (505 * SCALE_FACTOR, 360 * SCALE_FACTOR))
    

debug =False
def automator(moves, state, screen):
    '''
    Cette fonction exécute automatiquement les mouvements stockés dans la liste <moves>.
    '''
    global animPtr
    for step in moves:
        pygame.time.wait(PLAYER_MOVE_DELAY)
        if isLegal(state, step):
            move(state, step)
        else:
            print(f"[⚠️ Avertissement] Mouvement illégal ignoré : {step}")   
           
        screen.fill((53, 73, 94))
        animPtr += 1
        render(state, screen)
        pygame.display.update()

def gameScreen(currLevel, levelIndex, levels):
    '''
    Fonction principale du jeu qui initie la boucle de jeu.
    '''
    buffer = 0
    global animPtr
    pygame.mixer.init()

    # Chargement des sons
    push = pygame.mixer.Sound(os.path.join(APP_FOLDER, "push.wav"))
    footstep = pygame.mixer.Sound(os.path.join(APP_FOLDER, "footstep.wav"))
    metal = pygame.mixer.Sound(os.path.join(APP_FOLDER, "metal.wav"))

    pygame.display.set_caption("Sokoban")
    pygame.display.set_icon(icon)
    # screen2 = pygame.display.set_mode((1132, 600))
    screen2 = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    
    end = False
    move_history = []  # Historique des mouvements
    original_level = copy.deepcopy(currLevel)  # Pour la réinitialisation

    
    while not end:
        clock.tick(24)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    vals = (0, -1)
                    if isLegal(currLevel, vals):
                        move_history.append(copy.deepcopy(currLevel))
                        if currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 0:
                            pygame.mixer.Sound.play(footstep)
                            pygame.mixer.music.stop()
                        elif currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 2:
                            pygame.mixer.Sound.play(push)
                            pygame.mixer.music.stop()
                        elif currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 3:
                            pygame.mixer.Sound.play(metal)
                            pygame.mixer.music.stop()
                        move(currLevel, vals)
                        pygame.time.wait(PLAYER_MOVE_DELAY) 
                elif event.key == pygame.K_DOWN:
                    vals = (0, 1)
                    if isLegal(currLevel, vals):
                        move_history.append(copy.deepcopy(currLevel))
                        if currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 0:
                            pygame.mixer.Sound.play(footstep)
                            pygame.mixer.music.stop()
                        elif currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 2:
                            pygame.mixer.Sound.play(push)
                            pygame.mixer.music.stop()
                        elif currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 3:
                            pygame.mixer.Sound.play(metal)
                            pygame.mixer.music.stop()
                        move(currLevel, vals)
                        pygame.time.wait(PLAYER_MOVE_DELAY) 
                elif event.key == pygame.K_LEFT:
                    vals = (-1, 0)
                    if isLegal(currLevel, vals):
                        move_history.append(copy.deepcopy(currLevel))
                        if currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 0:
                            pygame.mixer.Sound.play(footstep)
                            pygame.mixer.music.stop()
                        elif currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 2:
                            pygame.mixer.Sound.play(push)
                            pygame.mixer.music.stop()
                        elif currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 3:
                            pygame.mixer.Sound.play(metal)
                            pygame.mixer.music.stop()
                        move(currLevel, vals)
                        pygame.time.wait(PLAYER_MOVE_DELAY) 
                elif event.key == pygame.K_RIGHT:
                    vals = (1, 0)
                    if isLegal(currLevel, vals):
                        move_history.append(copy.deepcopy(currLevel))
                        if currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 0:
                            pygame.mixer.Sound.play(footstep)
                            pygame.mixer.music.stop()
                        elif currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 2:
                            pygame.mixer.Sound.play(push)
                            pygame.mixer.music.stop()
                        elif currLevel.matrix[currLevel.playerY + vals[1]][currLevel.playerX + vals[0]] == 3:
                            pygame.mixer.Sound.play(metal)
                            pygame.mixer.music.stop()
                        move(currLevel, vals)
                        pygame.time.wait(PLAYER_MOVE_DELAY) 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 25 * SCALE_FACTOR <= mouse[0] <= (25 + 58) * SCALE_FACTOR and 360 * SCALE_FACTOR <= mouse[1] <= (360 + 23) * SCALE_FACTOR:
                    currLevel = copy.deepcopy(levels[levelIndex])
                    start = time.time()
                    solution = breadthFirstSearch(currLevel).timeLine
                    end = time.time()
                    duration = end - start
                    if solution:
                        save_result("BFS", speed_label, len(solution), duration)

                    if solution:
                        t1 = Thread(target=automator, args=(solution, currLevel, screen2))
                        t1.start()
                        t1.join()
                if 105 * SCALE_FACTOR <= mouse[0] <= (105 + 58) * SCALE_FACTOR and 360 * SCALE_FACTOR <= mouse[1] <= (360 + 23) * SCALE_FACTOR:
                    currLevel = copy.deepcopy(levels[levelIndex])
                    start = time.time()
                    solution = aStarManhattan(currLevel).timeLine
                    end = time.time()
                    duration = end - start
                    if solution:
                        save_result("A*", speed_label, len(solution), duration)

                    if solution:
                        t1 = Thread(target=automator, args=(solution, currLevel, screen2))
                        t1.start()
                        t1.join()
                if 185 * SCALE_FACTOR <= mouse[0] <= (185 + 58) * SCALE_FACTOR and 360 * SCALE_FACTOR <= mouse[1] <= (360 + 23) * SCALE_FACTOR:
                    currLevel = copy.deepcopy(levels[levelIndex])
                    start = time.time()
                    solution = depthFirstSearch(currLevel).timeLine
                    end = time.time()
                    duration = end - start
                    if solution:
                        save_result("DFS", speed_label, len(solution), duration)

                    if solution:
                        t1 = Thread(target=automator, args=(solution, currLevel, screen2))
                        t1.start()
                        t1.join()
                        
                # Undo Button
                if 265 * SCALE_FACTOR <= mouse[0] <= (265 + 58) * SCALE_FACTOR and 360 * SCALE_FACTOR <= mouse[1] <= (360 + 23) * SCALE_FACTOR:
                    if move_history:
                        currLevel = move_history.pop()
                
                # Reset Button
                if 345 * SCALE_FACTOR <= mouse[0] <= (345 + 58) * SCALE_FACTOR and 360 * SCALE_FACTOR <= mouse[1] <= (360 + 23) * SCALE_FACTOR:
                    currLevel = copy.deepcopy(original_level)
                    move_history.clear()
                
                # Quit Button
                if 425 * SCALE_FACTOR <= mouse[0] <= (425 + 58) * SCALE_FACTOR and 360 * SCALE_FACTOR <= mouse[1] <= (360 + 23) * SCALE_FACTOR:
                    end = True
                
                # Home Button
                if 505 * SCALE_FACTOR <= mouse[0] <= (505 + 58) * SCALE_FACTOR and 360 * SCALE_FACTOR <= mouse[1] <= (360 + 23) * SCALE_FACTOR:
                    pygame.display.quit()  # ferme juste la fenêtre de jeu
                    from main import startScreen
                    end = True  # Quitte gameScreen()
                    return

            if check(currLevel):
                print("✅ Niveau terminé.")
                levelIndex += 1
                if levelIndex >= len(levels):
                    print("🎉 Tous les niveaux ont été terminés.")
                    
                    pygame.time.wait(2000)
                    end = True
                else:
                    currLevel = copy.deepcopy(levels[levelIndex])
                    original_level = copy.deepcopy(currLevel)
                    move_history.clear()
                    pygame.time.wait(1000)  # Pause entre les niveaux


        
        screen2.fill((53, 73, 94))
        buffer += 1
        if not buffer % 4:
            animPtr += 1
        render(currLevel, screen2)
        pygame.display.update()
        
      
