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
RED = (255, 0, 0)

# Classe pour représenter chaque barre
class Barre:
    def __init__(self, x, color, y_positions, min_y, max_y, direction):
        self.x = x  # Position horizontale de la barre
        self.color = color  # Couleur des joueurs sur la barre
        self.initial_y_positions = y_positions  # Liste des positions verticales pour chaque joueur
        self.y_offset = 0  # Décalage vertical de la barre
        self.player_width = 20  # Largeur des joueurs (rectangle)
        self.player_height = 30  # Hauteur des joueurs (rectangle)
        self.min_y = min_y  # Limite de déplacement vers le haut
        self.max_y = max_y  # Limite de déplacement vers le bas
        self.direction = direction  # Direction du tir : (1, 0) pour droite, (-1, 0) pour gauche

    def dessiner(self, surface):
        for y in self.initial_y_positions:
            # Calculer la position en ajoutant le décalage
            rect = pygame.Rect(self.x - self.player_width // 2, y + self.y_offset - self.player_height // 2, self.player_width, self.player_height)
            pygame.draw.rect(surface, self.color, rect)  # Dessiner le rectangle représentant un joueur

    def deplacer(self, direction):
        if direction == "up":
            new_offset = self.y_offset - 0.3  # Déplacement vers le haut
            if new_offset >= self.min_y:
                self.y_offset = new_offset
        elif direction == "down":
            new_offset = self.y_offset + 0.3  # Déplacement vers le bas
            if new_offset <= self.max_y:
                self.y_offset = new_offset

# Classe pour représenter la balle
class Balle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = 2  # Vitesse initiale sur l'axe x
        self.speed_y = 1  # Vitesse initiale sur l'axe y
        self.attached_to_barre = None  # Barre à laquelle la balle est attachée (None par défaut)

    def dessiner(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def deplacer(self):
        # Déplacer la balle uniquement si elle n'est pas attachée
        if self.attached_to_barre is None:
            self.x += self.speed_x
            self.y += self.speed_y

            # Rebondir sur le haut et le bas du terrain
            if self.y - self.radius <= 0 or self.y + self.radius >= height:
                self.speed_y *= -1

            # Vérifier la collision avec les joueurs des barres
            for barre in barres:
                for y in barre.initial_y_positions:
                    joueur_y = y + barre.y_offset
                    if (barre.x - barre.player_width // 2 - self.radius <= self.x <= barre.x + barre.player_width // 2 + self.radius) and \
                       (joueur_y - barre.player_height // 2 - self.radius <= self.y <= joueur_y + barre.player_height // 2 + self.radius):
                        # Arrêter la balle lorsqu'elle touche un joueur
                        self.speed_x = 0
                        self.speed_y = 0
                        self.attached_to_barre = barre
                        return  # Sortir de la méthode après avoir arrêté la balle

    def tirer(self):
        if self.attached_to_barre is not None:
            direction = self.attached_to_barre.direction
            self.speed_x = direction[0] * 5  # Direction x multipliée par une vitesse
            self.speed_y = direction[1] * 5  # Direction y multipliée par une vitesse
            self.attached_to_barre = None  # Détacher la balle

# Créer des barres pour chaque équipe avec des configurations différentes
barres = [
    Barre(50, BLUE, [height // 2], -50, 50, (1, 0)),  # Gardien de l'équipe bleue
    Barre(150, BLUE, [height // 3, 2 * height // 3], -110, 110, (1, 0)),  # Défenseurs de l'équipe bleue
    Barre(250, BLACK, [height // 4, height // 2, 3 * height // 4], -70, 70, (-1, 0)),  # Milieu de l'équipe noire
    Barre(350, BLUE, [50, 120, 190, 260, 330], -30, 50, (1, 0)),  # Attaquants de l'équipe bleue
    Barre(450, BLACK, [50, 120, 190, 260, 330], -30, 50, (-1, 0)),  # Attaquants de l'équipe noire
    Barre(550, BLUE, [height // 4, height // 2, 3 * height // 4], -75, 75, (1, 0)),  # Milieu de l'équipe bleue
    Barre(650, BLACK, [height // 3, 2 * height // 3], -110, 110, (-1, 0)),  # Défenseurs de l'équipe noire
    Barre(750, BLACK, [height // 2], -50, 50, (-1, 0)),  # Gardien de l'équipe noire
]

# Initialisation de la balle
balle = Balle(400, 200, 10, RED)

# Fonction pour dessiner le terrain
def dessiner_terrain():
    window.fill(GREEN)  # Remplir l'arrière-plan avec du vert
    pygame.draw.rect(window, WHITE, (0, height // 3, 5, height // 3))  # But gauche
    pygame.draw.rect(window, WHITE, (width - 5, height // 3, 5, height // 3))  # But droit
    pygame.draw.line(window, WHITE, (width // 2, 0), (width // 2, height), 5)  # Ligne centrale
    pygame.draw.circle(window, WHITE, (width // 2, height // 2), 50, 5)  # Cercle central

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Contrôler les barres
    if keys[pygame.K_a]:
        barres[0].deplacer("up")
    if keys[pygame.K_q]:
        barres[0].deplacer("down")
    if keys[pygame.K_s]:
        barres[1].deplacer("up")
    if keys[pygame.K_z]:
        barres[1].deplacer("down")
    if keys[pygame.K_e]:
        barres[2].deplacer("up")
    if keys[pygame.K_d]:
        barres[2].deplacer("down")
    if keys[pygame.K_r]:
        barres[3].deplacer("up")
    if keys[pygame.K_f]:
        barres[3].deplacer("down")
    if keys[pygame.K_t]:
        barres[4].deplacer("up")
    if keys[pygame.K_g]:
        barres[4].deplacer("down")
    if keys[pygame.K_y]:
        barres[5].deplacer("up")
    if keys[pygame.K_h]:
        barres[5].deplacer("down")
    if keys[pygame.K_u]:
        barres[6].deplacer("up")
    if keys[pygame.K_j]:
        barres[6].deplacer("down")
    if keys[pygame.K_i]:
        barres[7].deplacer("up")
    if keys[pygame.K_k]:
        barres[7].deplacer("down")

    # Tirer la balle avec ESPACE
    if keys[pygame.K_SPACE]:
        balle.tirer()

    # Mettre à jour les positions
    balle.deplacer()

    # Dessiner le terrain et les barres
    dessiner_terrain()
    for barre in barres:
        barre.dessiner(window)
    balle.dessiner(window)

    pygame.display.flip()  # Mettre à jour l'affichage

pygame.quit()
sys.exit()
