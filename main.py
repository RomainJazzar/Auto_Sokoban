from threading import Thread
import os
import pygame
import copy

from level import Level
from levelsTested import testedLevels
from build_game import *
from dfs import *
from bfs import *
from manhattanStar import *
from display_game import *
from results_db import init_db
init_db()


# Facteur de mise à l’échelle
SCALE_FACTOR = 1
# Dossier des assets
APP_FOLDER = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'assets'
icon = pygame.transform.scale(pygame.image.load(os.path.join(APP_FOLDER, "icon.png")), (64, 64))

levels = copy.deepcopy(testedLevels)
levelIndex = 0

def startScreen(levelIndex, levels):
    import display_game
    end = False
    pygame.init()
    
    display_game.PLAYER_MOVE_DELAY = 500  # Par défaut
    display_game.speed_label = "Normale"
    
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 650
    screen1 = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("SokoBot")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    # Charger l'image de fond
    try:
        background = pygame.image.load("assets/background.png").convert()
        background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception as e:
        print("Erreur chargement image background :", e)
        background = None
    
    # Polices
    font = pygame.font.SysFont('Arial', 60 * SCALE_FACTOR)
    font2 = pygame.font.SysFont('Arial', 20 * SCALE_FACTOR)

    # Texte des boutons
    choice3_text = font2.render('Vitesse: Lente', True, (255, 39, 255), (53, 73, 94))
    choice4_text = font2.render('Vitesse: Normale', True, (255, 39, 255), (53, 73, 94))
    choice5_text = font2.render('Vitesse: Rapide', True, (255, 39, 255), (53, 73, 94))
    playText = font2.render('Lancer le jeu', True, (40, 255, 40), (53, 73, 94))

    # Positionnement
    center_x = WINDOW_WIDTH // 2
    start_y = 150 * SCALE_FACTOR
    spacing = 40 * SCALE_FACTOR

    # Création des rectangles
    choice3_rect = choice3_text.get_rect(center=(center_x, start_y))
    choice4_rect = choice4_text.get_rect(center=(center_x, start_y + spacing))
    choice5_rect = choice5_text.get_rect(center=(center_x, start_y + 2 * spacing))
    play_rect = playText.get_rect(center=(center_x, start_y + 3 * spacing + 20))

    while not end:
        clock.tick(6)
        # Afficher l'image de fond si chargée, sinon fond uni
        if background:
            screen1.blit(background, (0, 0))
        else:
            screen1.fill((53, 73, 94))

        # Titre
        title = font.render('Sokoban', True, (0, 255, 125), (53, 73, 94))
        title_rect = title.get_rect(center=(center_x, 40 * SCALE_FACTOR))
        screen1.blit(title, title_rect)

        # Boutons
        screen1.blit(choice3_text, choice3_rect)
        screen1.blit(choice4_text, choice4_rect)
        screen1.blit(choice5_text, choice5_rect)
        screen1.blit(playText, play_rect)

        # Icône (optionnelle)
        try:
            screen1.blit(pygame.transform.scale(icon, (80 * SCALE_FACTOR, 80 * SCALE_FACTOR)), (center_x - 40, 550))
        except:
            pass

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if choice3_rect.collidepoint(mx, my):
                    display_game.PLAYER_MOVE_DELAY = 900
                    display_game.speed_label = "Lente"
                elif choice4_rect.collidepoint(mx, my):
                    display_game.PLAYER_MOVE_DELAY = 500
                    display_game.speed_label = "Normale"
                elif choice5_rect.collidepoint(mx, my):
                    display_game.PLAYER_MOVE_DELAY = 150
                    display_game.speed_label = "Rapide"  

                elif play_rect.collidepoint(mx, my):
                    local_index = 0
                    while local_index < len(levels):
                        currLevel = copy.deepcopy(levels[local_index])
                        gameScreen(currLevel, local_index, levels)
                        local_index += 1
                    # Retour automatique au menu après tous les niveaux
                    startScreen(0, levels)

        pygame.display.update()


if __name__ == "__main__":
    startScreen(levelIndex, levels)
