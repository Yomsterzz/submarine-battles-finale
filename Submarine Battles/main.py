import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 992
HEIGHT = 496
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Submarine Battles")

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GRAY = 255, 0, 0
YELLOW = 255, 255, 0
border = pygame.Rect(WIDTH // 2, 0, 10, HEIGHT)

health_font = pygame.font.SysFont("comicsans", 45)
winner_font = pygame.font.SysFont("futura", 75)

fps = 60
vel = 9
missile_vel = 14
max_missiles = 7
player_width = 83
player_height = 60
yellow_hit = pygame.USEREVENT + 1
gray_hit = pygame.USEREVENT + 2

gray_sub_img = pygame.image.load("./images/gray-sub.png")
gray_sub = pygame.transform.scale(gray_sub_img, (player_width, player_height))

yellow_sub_img = pygame.image.load("./images/yellow-sub.png")
yellow_sub = pygame.transform.scale(yellow_sub_img, (player_width, player_height))

bg = pygame.image.load("./images/pixelwater.png")
bg_scaled = pygame.transform.scale(bg, (WIDTH, HEIGHT))

def draw_screen(gray, yellow, gray_missiles, yellow_missiles, gray_health, yellow_health):
    screen.blit(bg_scaled, (0, 0))
    pygame.draw.rect(screen, WHITE, border)

    gray_health_text = health_font.render("Health: " + str(gray_health), 1, WHITE)
    yellow_health_text = health_font.render("Health: " + str(yellow_health), 1, WHITE)
    screen.blit(gray_health_text, (WIDTH - gray_health_text.get_width() - 10, 20))
    screen.blit(yellow_health_text, (10, 20))

    screen.blit(yellow_sub, (yellow.x, yellow.y))
    screen.blit(gray_sub, (gray.x, gray.y))

    for missile in gray_missiles:
        pygame.draw.rect(screen, GRAY, missile)

    for missile in yellow_missiles:
        pygame.draw.rect(screen, YELLOW, missile)

    pygame.display.update()

def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0: 
        yellow.x -= vel
    if keys_pressed[pygame.K_d] and yellow.x + vel + yellow.width < border.x: 
        yellow.x += vel
    if keys_pressed[pygame.K_w] and yellow.y - vel > 0: 
        yellow.y -= vel
    if keys_pressed[pygame.K_s] and yellow.y + vel + yellow.height < HEIGHT - 15:
        yellow.y += vel

def handle_gray_movement(keys_pressed, gray):
    if keys_pressed[pygame.K_LEFT] and gray.x - vel > border.x + border.width:  
        gray.x -= vel
    if keys_pressed[pygame.K_RIGHT] and gray.x + vel + gray.width < WIDTH: 
        gray.x += vel
    if keys_pressed[pygame.K_UP] and gray.y - vel > 0:  
        gray.y -= vel
    if keys_pressed[pygame.K_DOWN] and gray.y + vel + gray.height < HEIGHT - 15:  
        gray.y += vel

def handle_missiles(yellow_missiles, yellow, gray_missiles, gray):
    for missile in yellow_missiles:
        missile.x += missile_vel
        if gray.colliderect(missile):
            yellow_missiles.remove(missile)
            pygame.event.post(pygame.event.Event(gray_hit))
        elif missile.x > WIDTH:
            yellow_missiles.remove(missile)

    for missile in gray_missiles:
        missile.x -= missile_vel
        if yellow.colliderect(missile):
            gray_missiles.remove(missile)
            pygame.event.post(pygame.event.Event(yellow_hit))
        elif missile.x < 0:
            gray_missiles.remove(missile)
def draw_winner(text):
    draw_text = winner_font.render(text, 1, WHITE)
    screen.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    gray = pygame.Rect(700,300, player_width, player_height)
    yellow = pygame.Rect(100,300, player_width, player_height)
    gray_missiles = []
    yellow_missiles = []
    gray_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_missiles) < max_missiles:
                    missile = pygame.Rect(yellow.x + 20, yellow.y + yellow.height//2 -2, 10,5) 
                    yellow_missiles.append(missile)

                if event.key == pygame.K_RSHIFT and len(gray_missiles) < max_missiles:
                    missile = pygame.Rect(gray.x + 20, gray.y + gray.height//2 -2, 10,5) 
                    gray_missiles.append(missile)
            
            if event.type == yellow_hit:
                yellow_health -= 1
            
            if event.type == gray_hit:
                gray_health -= 1
            
        winner_text = ""
        if gray_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            winner_text = "Gray wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        handle_gray_movement(key_pressed, gray)
        handle_yellow_movement(key_pressed, yellow)
        handle_missiles(yellow_missiles, yellow, gray_missiles, gray)
        draw_screen(gray, yellow, gray_missiles, yellow_missiles, gray_health, yellow_health)

main()
if __name__ == "__main__":
    main()