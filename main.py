import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
width, height = 800, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jeu de Babyfoot")

# Couleurs
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Classe pour représenter chaque barre
class Barre:
    def __init__(self, x, color, y_positions):
        self.x = x  # Position horizontale de la barre
        self.color = color  # Couleur des joueurs sur la barre
        self.initial_y_positions = y_positions  # Liste des positions verticales pour chaque joueur
        self.y_offset = 0  # Décalage vertical de la barre
        self.player_width = 20  # Largeur des joueurs (rectangle)
        self.player_height = 30  # Hauteur des joueurs (rectangle)

    def dessiner(self, surface):
        for y in self.initial_y_positions:
            # Calculer la position en ajoutant le décalage
            rect = pygame.Rect(self.x - self.player_width // 2, y + self.y_offset - self.player_height // 2, self.player_width, self.player_height)
            pygame.draw.rect(surface, self.color, rect)  # Dessiner le rectangle représentant un joueur

    def deplacer(self, direction):
        # Limites pour le mouvement
        min_y = - (height // 2) + self.player_height // 0.2  # Limite supérieure
        max_y = height // 2 - self.player_height // 0.2  # Limite inférieure

        if direction == "up":
            new_offset = self.y_offset - 0.1  # Déplacement vers le haut
            if new_offset >= min_y:  # Vérifiez si elle est dans les limites
                self.y_offset = new_offset

        elif direction == "down":
            new_offset = self.y_offset + 0.1  # Déplacement vers le bas
            if new_offset <= max_y:  # Vérifiez si elle est dans les limites
                self.y_offset = new_offset

# Créer des barres pour chaque équipe avec des configurations différentes
barres = [
    Barre(50, BLUE, [height // 2]),  # Gardien de l'équipe bleue
    Barre(150, BLUE, [height // 3, 2 * height // 3]),  # Défenseurs de l'équipe bleue
    Barre(250, BLACK, [height // 4, height // 2, 3 * height // 4]),  # Milieu de l'équipe noire
    Barre(350, BLUE, [50, 120, 190, 260, 330]),  # Attaquants de l'équipe bleue
    Barre(450, BLACK, [50, 120, 190, 260, 330]),  # Attaquants de l'équipe noire
    Barre(550, BLUE, [height // 4, height // 2, 3 * height // 4]),  # Milieu de l'équipe bleue
    Barre(650, BLACK, [height // 3, 2 * height // 3]),  # Milieu de l'équipe noire
    Barre(750, BLACK, [height // 2]),  # Gardien de l'équipe noire
]

# Fonction pour dessiner le terrain
def dessiner_terrain():
    window.fill(GREEN)  # Remplir l'arrière-plan avec du vert
    # Lignes de but
    pygame.draw.rect(window, WHITE, (0, height // 3, 5, height // 3))  # But gauche
    pygame.draw.rect(window, WHITE, (width - 5, height // 3, 5, height // 3))  # But droit
    # Ligne centrale
    pygame.draw.line(window, WHITE, (width // 2, 0), (width // 2, height), 5)
    # Cercle central
    pygame.draw.circle(window, WHITE, (width // 2, height // 2), 50, 5)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtenir les touches enfoncées
    keys = pygame.key.get_pressed()

    # Contrôler les barres
    # Gardien équipe bleue
    if keys[pygame.K_a]:  # Touche A pour monter
        barres[0].deplacer("up")
    if keys[pygame.K_q]:  # Touche Q pour descendre
        barres[0].deplacer("down")

    # Défenseurs équipe bleue
    if keys[pygame.K_s]:  # Touche S pour monter
        barres[1].deplacer("up")
    if keys[pygame.K_z]:  # Touche Z pour descendre
        barres[1].deplacer("down")

    # Milieu équipe bleue
    if keys[pygame.K_e]:  # Touche E pour monter
        barres[2].deplacer("up")
    if keys[pygame.K_d]:  # Touche D pour descendre
        barres[2].deplacer("down")

    # Attaquants équipe bleue
    if keys[pygame.K_r]:  # Touche R pour monter
        barres[3].deplacer("up")
    if keys[pygame.K_f]:  # Touche F pour descendre
        barres[3].deplacer("down")

    # Milieu équipe noire
    if keys[pygame.K_t]:  # Touche T pour monter
        barres[4].deplacer("up")
    if keys[pygame.K_g]:  # Touche G pour descendre
        barres[4].deplacer("down")

    # Défenseurs équipe noire
    if keys[pygame.K_y]:  # Touche Y pour monter
        barres[5].deplacer("up")
    if keys[pygame.K_h]:  # Touche H pour descendre
        barres[5].deplacer("down")

    # Gardien équipe noire
    if keys[pygame.K_u]:  # Flèche haut pour monter
        barres[6].deplacer("up")
    if keys[pygame.K_j]:  # Flèche bas pour descendre
        barres[6].deplacer("down")

    if keys[pygame.K_i]:  # Flèche haut pour monter
        barres[7].deplacer("up")
    if keys[pygame.K_k]:  # Flèche bas pour descendre
        barres[7].deplacer("down")

    if keys[pygame.K_o]:  # Flèche haut pour monter
        barres[8].deplacer("up")
    if keys[pygame.K_l]:  # Flèche bas pour descendre
        barres[8].deplacer("down")

    # Dessiner le terrain et les barres avec les joueurs
    dessiner_terrain()
    for barre in barres:
        barre.dessiner(window)

    pygame.display.flip()  # Mettre à jour l'affichage

# Quitter Pygame proprement
pygame.quit()
sys.exit()
