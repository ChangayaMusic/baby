import pygame
import sys
import math

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

# Variables de score
score_bleu = 0
score_noir = 0

# Classe pour représenter chaque barre
class Barre:
    def __init__(self, x, color, y_positions, min_y, max_y, direction):
        self.x = x
        self.color = color
        self.initial_y_positions = y_positions
        self.y_offset = 0
        self.player_width = 20
        self.player_height = 30
        self.min_y = min_y
        self.max_y = max_y
        self.direction = direction

    def dessiner(self, surface):
        for y in self.initial_y_positions:
            # Dessiner les joueurs sous forme de rectangles
            rect = pygame.Rect(
                self.x - self.player_width // 2,
                y + self.y_offset - self.player_height // 2,
                self.player_width,
                self.player_height
            )
            pygame.draw.rect(surface, self.color, rect)
            
            # Dessiner un cercle blanc au centre de chaque joueur (réduit à rayon 3)
            pygame.draw.circle(
                surface, 
                WHITE,  # Couleur du cercle (blanc)
                (int(self.x), int(y + self.y_offset)),  # Position centrale du joueur
                3 # Nouveau rayon plus petit
            )

    def deplacer(self, direction):
        vitesse = 0.5  # Vitesse de déplacement ajustée
        if direction == "up":
            new_offset = self.y_offset - vitesse  # Déplacement vers le haut
            if new_offset >= self.min_y:
                self.y_offset = new_offset
        elif direction == "down":
            new_offset = self.y_offset + vitesse  # Déplacement vers le bas
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
                    # Position du cercle blanc du joueur
                    player_center = (int(barre.x), int(joueur_y))

                    # Vérification si la balle touche le cercle (proximité de la balle avec le centre du joueur)
                    distance = ((self.x - player_center[0]) ** 2 + (self.y - player_center[1]) ** 2) ** 0.5
                    if distance <= self.radius + 3:  # Zone de collision réduite (3 au lieu de 8)
                        # Calcul de l'angle de déviation en fonction de la position de la balle
                        angle = math.atan2(self.y - player_center[1], self.x - player_center[0])

                        # Appliquer une déviation à la balle en fonction de l'angle
                        speed = math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)
                        self.speed_x = math.cos(angle) * speed
                        self.speed_y = math.sin(angle) * speed
                        
                        # Modifier la direction pour simuler un rebond
                        self.speed_x = -self.speed_x  # Inverser la direction sur l'axe X

                        self.attached_to_barre = barre
                        return  # Sortir de la méthode après avoir dévié la balle

    def tirer(self):
        if self.attached_to_barre is not None:
            direction = self.attached_to_barre.direction
            self.speed_x = direction[0] * 0.5  # Direction x multipliée par une vitesse
            self.speed_y = direction[1] * 0.5  # Direction y multipliée par une vitesse
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
balle = Balle(width // 2, height // 2, 8, RED)

# Fonction pour dessiner le terrain
def dessiner_terrain():
    window.fill(GREEN)
    pygame.draw.rect(window, WHITE, (0, height // 3, 5, height // 3))  # But gauche
    pygame.draw.rect(window, WHITE, (width - 5, height // 3, 5, height // 3))  # But droit
    pygame.draw.line(window, WHITE, (width // 2, 0), (width // 2, height), 5)  # Ligne centrale
    pygame.draw.circle(window, WHITE, (width // 2, height // 2), 50, 5)  # Cercle central

# Fonction pour vérifier les buts et mettre à jour les scores
def check_goal():
    global score_bleu, score_noir, balle
    if balle.x - balle.radius <= 0:  # But pour l'équipe noire
        score_noir += 1
        reset_balle(team='bleu')
    elif balle.x + balle.radius >= width:  # But pour l'équipe bleue
        score_bleu += 1
        reset_balle(team='noir')

def reset_balle(team):
    if team == 'noir':
        balle.x, balle.y = 350, height // 2  # Barre de milieu de l'équipe bleue
    else:
        balle.x, balle.y = 450, height // 2  # Barre de milieu de l'équipe noire
    balle.speed_x, balle.speed_y = 0, 0  # Réinitialiser la vitesse
    balle.attached_to_barre = None  # La balle n'est attachée à aucune barre

# Fonction pour afficher les scores
def afficher_scores():
    font = pygame.font.SysFont(None, 50)
    score_text = font.render(f"Bleu: {score_bleu} - Noir: {score_noir}", True, WHITE)
    window.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))

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

    # Vérifier les buts
    check_goal()

    # Dessiner le terrain, les barres, la balle et les scores
    dessiner_terrain()
    for barre in barres:
        barre.dessiner(window)
    balle.dessiner(window)
    afficher_scores()

    pygame.display.flip()  # Mettre à jour l'affichage

pygame.quit()
sys.exit()
