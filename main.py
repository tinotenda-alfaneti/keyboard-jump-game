import pygame
import sys
import random


# initializing pygame
pygame.init()

# setting game display size
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_mode((screen_width, screen_height))

#setting background
image = pygame.image.load("keyboard.jpg")
background = pygame.transform.scale(image, (screen_width, screen_height))

# display caption
pygame.display.set_caption("Atarist Jump Game")

# font
font = pygame.font.Font("comic.ttf", 42)

#background music
pygame.mixer.music.load("music/background.wav")
#pygame.mixer.music.play(-1)

# words list from a file removing the special character
words = []
special = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", ".", ",", "[", "]", "'", ";"]
file = open("dictionary.txt", "r").read().split()
for word in file:

    if 4 < len(word.strip()) < 15:
        words.append(word.strip().lower())
        for letter in word:
            if letter in special:
                if word in words:
                    words.remove(word)

#defining variables
word_speed = 0.5
score = 0
display_word = "test"
your_word = ""
x_cor = random.randint(300, 700)
y_cor = 200
text = ""
font_name = pygame.font.match_font('"comic.ttf"')

# tracking the scores
previous_score = 0
record = open("scores.txt", "r")
for old_score in record:
    previous_score = int(old_score)
new_background = pygame.image.load("newback.jpg")
new_background = pygame.transform.scale(new_background, (screen_width, screen_height))


# function will randomly take words from the words list and initializes x and y coordinates of the word
def new_word():
    global display_word, your_word, x_cor, y_cor, text, word_speed
    x_cor = random.randint(300, 700)
    y_cor = 200
    word_speed += 0.10
    your_word = ""
    display_word = random.choice(words)


new_word()


# function will help to draw text on display in a given font and size
def draw_text(display, text, size, x, y):
    display = display
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 5, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


# function display the front game screen and the game over screen
def game_front_screen():
    global previous_score
    screen.blit(new_background, (0, 0))
    if not game_over:
        draw_text(screen, "GAME OVER!", 90, screen_width/2, screen_height/4)
        score_record = open("scores.txt", "w")
        if score > previous_score:
            score_record.write(str(score))
            draw_text(screen, f"High score: {score}", 70, screen_width / 2, screen_height / 2)
        else:
            score_record.write(str(previous_score))
            draw_text(screen, f"Score: {score}", 70, screen_width / 2, screen_height / 2)

    else:
        draw_text(screen, "Press any key to begin!", 54, screen_width/2, screen_height/2)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False


game_over = True
game_start = True

while True:
    if game_over:
        if game_start:
            game_front_screen()
        game_start = False
    game_over = False

    #setting up the game screen and player, the score
    background = pygame.image.load("background.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))
    character = pygame.image.load("char.jpg")
    character = pygame.transform.scale(character, (50, 50))
    wood = pygame.image.load('wood-.png')
    wood = pygame.transform.scale(wood, (150, 50))
    screen.blit(background, (0, 0))
    screen.blit(wood, (x_cor - 60, y_cor + 15))
    screen.blit(character, (x_cor - 130, y_cor))
    draw_text(screen, str(display_word), 40, x_cor + 10, y_cor)
    draw_text(screen, 'High Score:' + str(previous_score), 40, screen_width / 2, 30)
    draw_text(screen, 'Score:' + str(score), 40, screen_width / 2, 5)
    #for moving the display word, player and wood
    y_cor += word_speed
    #checking if the y_cor is not yet out of the screen. If it is out the game will be over
    if y_cor > screen_height - 5:
        game_front_screen()

    else:
        pygame.display.update()
    # checking key presses and when the player hits the quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        #getting the user's word
        elif event.type == pygame.KEYDOWN:
            your_word += pygame.key.name(event.key)
    #checks to see if the user is typing the right word
    if display_word.startswith(your_word):
        if display_word == your_word:
            score += len(display_word)
            new_word()
    else:
        game_front_screen()
