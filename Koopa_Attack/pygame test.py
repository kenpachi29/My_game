import pygame
import random
import sys

pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
PLAYER_SIZE = 30
KOOPA_SIZE = (int(SCREEN_WIDTH / 12), int(SCREEN_WIDTH / 12))
OBSTACLE_INTERVAL = 44
PLAYER_VELOCITY = 5
BG_COLOR = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
KOOPA1_IMG_PATH = "Koopa 1.png"
KOOPA2_IMG_PATH = "Koopa 2.png"
KOOPA3_IMG_PATH = "Koopa 3.png"
KOOPA4_IMG_PATH = "Koopa 4.png"
BACKGROUND_IMG_PATH = "Mario Background.jpg"
FLY1_IMG_PATH = "FLY1.png"
FLY2_IMG_PATH = "FLY2.png"
FLY3_IMG_PATH = "FLY3.png"
FIRE_FLOWER_IMG_PATH = "fire flower.png"
ICE_FLOWER_IMG_PATH = "ice flower.png"
MUSIC_PATH = "utomp3.com - New Super Mario Bros Wii Forest Theme Soundtrack.mp3"
MENU_START_IMG_PATH = "menue start mario.jpg"
MENU_GAME_OVER_IMG_PATH = "menue game over.jpg"

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Auto-Runner Game")

# Chargement des images
koopa1_img = pygame.image.load(KOOPA1_IMG_PATH).convert_alpha()
koopa1_img = pygame.transform.scale(koopa1_img, KOOPA_SIZE)
koopa2_img = pygame.image.load(KOOPA2_IMG_PATH).convert_alpha()
koopa2_img = pygame.transform.scale(koopa2_img, KOOPA_SIZE)
koopa3_img = pygame.image.load(KOOPA3_IMG_PATH).convert_alpha()
koopa3_img = pygame.transform.scale(koopa3_img, KOOPA_SIZE)
koopa4_img = pygame.image.load(KOOPA4_IMG_PATH).convert_alpha()
koopa4_img = pygame.transform.scale(koopa4_img, KOOPA_SIZE)
background_img = pygame.image.load(BACKGROUND_IMG_PATH).convert()
background_img = pygame.transform.scale(background_img, (background_img.get_width(), SCREEN_HEIGHT))  # Redimensionner pour s'adapter à l'écran
fly1_img = pygame.image.load(FLY1_IMG_PATH).convert_alpha()
fly2_img = pygame.image.load(FLY2_IMG_PATH).convert_alpha()
fly3_img = pygame.image.load(FLY3_IMG_PATH).convert_alpha()
fire_flower_img = pygame.image.load(FIRE_FLOWER_IMG_PATH).convert_alpha()
ice_flower_img = pygame.image.load(ICE_FLOWER_IMG_PATH).convert_alpha()
menu_start_img = pygame.image.load(MENU_START_IMG_PATH).convert()
menu_start_img = pygame.transform.scale(menu_start_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
menu_game_over_img = pygame.image.load(MENU_GAME_OVER_IMG_PATH).convert()
menu_game_over_img = pygame.transform.scale(menu_game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.play(-1)  # -1 pour répéter la musique en boucle

# Création de la classe Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame_index = 0
        self.frames = [fly1_img, fly2_img, fly3_img]
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (50, 100)
        self.rect.inflate_ip(-27, -30.5)
        self.frame_timer = 0
        self.frame_delay = 10  # Ajustez cette valeur pour contrôler la vitesse de l'animation
        self.velocity_x = 0
        self.velocity_y = 0
        self.has_fire_power = False
        self.has_ice_power = False

    def update(self, keys, all_sprites, projectiles, power_ups):
        # Réinitialiser la vélocité
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Gérer les mouvements
        if keys[pygame.K_UP]:
            self.velocity_y = -PLAYER_VELOCITY
        elif keys[pygame.K_DOWN]:
            self.velocity_y = PLAYER_VELOCITY
        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_VELOCITY
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_VELOCITY

        # Mettre à jour la position du joueur en fonction de la vélocité
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Limiter le mouvement du joueur à l'écran
        self.rect.y = max(0, min(self.rect.y , SCREEN_HEIGHT - self.rect.height))
        self.rect.x = max(0, min(self.rect.x , SCREEN_WIDTH - self.rect.width))

        # Gérer le changement de frame
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # Gérer les collisions avec les power-ups
        power_up_collisions = pygame.sprite.spritecollide(self, power_ups, True)  # Détecter les collisions avec les power-ups
        for power_up in power_up_collisions:
            if power_up.type == "fire_flower":
                self.has_fire_power = True
            elif power_up.type == "ice_flower":
                self.has_ice_power = True

        # Gérer les collisions avec les projectiles
        projectile_collisions = pygame.sprite.spritecollide(self, projectiles, True)  # Détecter les collisions avec les projectiles
        for projectile in projectile_collisions:
            # Ici, vous pouvez ajouter du code pour gérer les effets des projectiles sur le joueur
            pass

# Création de la classe PowerUp
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, img_path, pos_x, pos_y, type):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.type = type

# Création de la classe Koopa
class Koopa(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.frame_index = 0
        self.frames = [koopa1_img, koopa2_img, koopa3_img, koopa4_img]
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = speed
        self.frame_timer = 0
        self.frame_delay = 10  # Ajustez cette valeur pour contrôler la vitesse de l'animation

    def update(self):
        # Mettre à jour la position
        self.rect.x -= self.speed

        # Gérer le changement de frame
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

# Création des groupes de sprites
all_sprites = pygame.sprite.Group()
koopas = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Horloge pour contrôler la vitesse du jeu
clock = pygame.time.Clock()

# Fonction pour générer aléatoirement des power-ups
def spawn_power_ups():
    if random.randint(1, 1000) == 1:  # Par exemple, un power-up apparaît toutes les 1000 itérations
        power_up_type = random.choice(["fire_flower", "ice_flower"])  # Sélectionner aléatoirement le type de power-up
        if power_up_type == "fire_flower":
            new_power_up = PowerUp(FIRE_FLOWER_IMG_PATH, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), "fire_flower")
        elif power_up_type == "ice_flower":
            new_power_up = PowerUp(ICE_FLOWER_IMG_PATH, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), "ice_flower")
        all_sprites.add(new_power_up)
        power_ups.add(new_power_up)

def run_game():
    # Réinitialisation des sprites et groupes de sprites
    all_sprites.empty()
    koopas.empty()

    # Création du joueur
    player = Player()
    all_sprites.add(player)

    # Réinitialisation des variables de jeu
    obstacle_counter = 0
    score = 0
    koopa_speed = 3

    # Position initiale du fond d'écran
    bg_x = 0

    # Boucle principale du jeu
    running = True
    game_over_flag = False  # Variable pour indiquer si le jeu est terminé
    while running:
        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Redémarrer le jeu lorsque la touche Entrée est pressée
                    return False

        # Vérifier si le joueur a perdu
        if not game_over_flag:
            # Gérer les mouvements du joueur
            keys = pygame.key.get_pressed()
            player.update(keys, all_sprites, projectiles, power_ups)

            # Augmenter le score à chaque boucle de jeu
            score += 1

            # Générer les obstacles (Koopas)
            obstacle_counter += 1
            if obstacle_counter >= OBSTACLE_INTERVAL:
                obstacle_counter = 0
                new_koopa = Koopa(koopa_speed)
                all_sprites.add(new_koopa)
                koopas.add(new_koopa)

            # Augmenter progressivement la vitesse des Koopas en fonction du score
            if score % 500 == 0:  # Augmenter la vitesse tous les 500 points
                koopa_speed += 1

            # Mettre à jour la position des Koopas
            koopas.update()

            # Générer aléatoirement des power-ups
            spawn_power_ups()

            # Dessiner tous les sprites
            screen.blit(background_img, (bg_x, 0))
            screen.blit(background_img, (bg_x + background_img.get_width(), 0))
            all_sprites.draw(screen)

            # Afficher le score à l'écran
            font = pygame.font.Font(None, 36)
            text = font.render("Score: " + str(score), True, (0, 0, 0))
            screen.blit(text, (10, 10))

            # Mettre à jour l'affichage
            pygame.display.flip()

            # Mettre à jour la position du fond d'écran pour le défilement
            bg_x -= 2  # Ajustez la vitesse de défilement ici

            # Si le premier fond d'écran sort de l'écran, replace-le à l'arrière
            if bg_x <= -background_img.get_width():
                bg_x = 0

            # Limiter la vitesse de la boucle
            clock.tick(60)
        else:
            game_over(score)  # Appel de la fonction game_over avec le score actuel
            return True

def main():
    show_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over_flag = run_game()
                    if game_over_flag:
                        show_menu()
                elif event.key == pygame.K_RETURN:  # Redémarrer le jeu lorsque la touche Entrée est pressée
                    game_over_flag = run_game()
                    if game_over_flag:
                        show_menu()

def show_menu():
    # Affichage du menu de démarrage
    screen.blit(menu_start_img, (0, 0))
    
    # Affichage du nom du jeu
    font = pygame.font.Font(None, 72)
    game_name_text = font.render("Koopa's Attack", True, (255, 255, 255))
    screen.blit(game_name_text, (200, 50))
    
    # Affichage du message pour démarrer le jeu
    font = pygame.font.Font(None, 36)
    title_text = font.render("PRESS SPACE TO START", True, (255, 255, 255))
    screen.blit(title_text, (300, 100))
    
    pygame.display.flip()

main()