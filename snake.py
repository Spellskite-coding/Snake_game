import pygame
import random

# Initialisation de Pygame
pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (213, 50, 80)
VERT = (0, 255, 0)
BLEU = (50, 153, 213)

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 600, 400
TAILLE_BLOC = 20

# Initialisation de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption('Snake Game')

# Horloge pour contrôler la vitesse
horloge = pygame.time.Clock()

# Police pour le score
police = pygame.font.SysFont("comicsansms", 25)

def dessiner_serpent(taille_bloc, pixels):
    for pixel in pixels:
        pygame.draw.rect(fenetre, VERT, [pixel[0], pixel[1], taille_bloc, taille_bloc])

def dessiner_pomme(taille_bloc, position_pomme):
    pygame.draw.rect(fenetre, ROUGE, [position_pomme[0], position_pomme[1], taille_bloc, taille_bloc])

def afficher_score(score):
    texte = police.render(f"Score: {score}", True, BLANC)
    fenetre.blit(texte, [10, 10])

def bouger_serpent(direction, pixels):
    nouvelle_tete = pixels[0].copy()
    if direction == "HAUT":
        nouvelle_tete[1] -= TAILLE_BLOC
    elif direction == "BAS":
        nouvelle_tete[1] += TAILLE_BLOC
    elif direction == "GAUCHE":
        nouvelle_tete[0] -= TAILLE_BLOC
    elif direction == "DROITE":
        nouvelle_tete[0] += TAILLE_BLOC
    pixels.insert(0, nouvelle_tete)
    return pixels

def jeu():
    fin_jeu = False
    fin_partie = False

    # Position initiale du serpent
    x = LARGEUR // 2
    y = HAUTEUR // 2

    # Changement de position
    x_change = 0
    y_change = 0

    # Liste des segments du serpent
    pixels_serpent = []
    longueur_serpent = 1

    # Position de la pomme
    position_pomme = [random.randrange(1, (LARGEUR // TAILLE_BLOC)) * TAILLE_BLOC,
                      random.randrange(1, (HAUTEUR // TAILLE_BLOC)) * TAILLE_BLOC]

    # Score
    score = 0

    # Direction initiale
    direction = "DROITE"

    while not fin_jeu:
        while fin_partie:
            fenetre.fill(NOIR)
            # Message "Game Over" en deux lignes et centré
            texte_game_over = police.render("Game Over !", True, ROUGE)
            texte_instructions = police.render("Appuie sur Entrée pour rejouer ou Échap pour quitter", True, BLANC)
            fenetre.blit(texte_game_over, [LARGEUR // 2 - texte_game_over.get_width() // 2, HAUTEUR // 2 - 30])
            fenetre.blit(texte_instructions, [LARGEUR // 2 - texte_instructions.get_width() // 2, HAUTEUR // 2 + 10])
            afficher_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        jeu()
                    if event.key == pygame.K_ESCAPE:
                        fin_jeu = True
                        fin_partie = False
                if event.type == pygame.QUIT:
                    fin_jeu = True
                    fin_partie = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin_jeu = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "BAS":
                    direction = "HAUT"
                    x_change = 0
                    y_change = -TAILLE_BLOC
                elif event.key == pygame.K_DOWN and direction != "HAUT":
                    direction = "BAS"
                    x_change = 0
                    y_change = TAILLE_BLOC
                elif event.key == pygame.K_LEFT and direction != "DROITE":
                    direction = "GAUCHE"
                    x_change = -TAILLE_BLOC
                    y_change = 0
                elif event.key == pygame.K_RIGHT and direction != "GAUCHE":
                    direction = "DROITE"
                    x_change = TAILLE_BLOC
                    y_change = 0

        # Déplacement du serpent
        if pixels_serpent:
            pixels_serpent = bouger_serpent(direction, pixels_serpent)
            if len(pixels_serpent) > longueur_serpent:
                pixels_serpent.pop()

        # Affichage
        fenetre.fill(NOIR)
        dessiner_serpent(TAILLE_BLOC, pixels_serpent)
        dessiner_pomme(TAILLE_BLOC, position_pomme)
        afficher_score(score)

        # Mise à jour de la tête du serpent
        if not pixels_serpent:
            pixels_serpent.append([x, y])
        else:
            pixels_serpent[0] = [x, y]

        # Mise à jour de la position
        x += x_change
        y += y_change

        # Collision avec les murs
        if x >= LARGEUR or x < 0 or y >= HAUTEUR or y < 0:
            fin_partie = True

        # Collision avec soi-même
        for bloc in pixels_serpent[1:]:
            if bloc == [x, y]:
                fin_partie = True

        # Collision avec la pomme
        if x == position_pomme[0] and y == position_pomme[1]:
            position_pomme = [random.randrange(1, (LARGEUR // TAILLE_BLOC)) * TAILLE_BLOC,
                              random.randrange(1, (HAUTEUR // TAILLE_BLOC)) * TAILLE_BLOC]
            longueur_serpent += 1
            score += 1

        pygame.display.update()
        horloge.tick(8)  # Vitesse ajustée

    pygame.quit()
    quit()

# Lancer le jeu
jeu()
