import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 900, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 30)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images.
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
level=1
lvl1 = {"GAS":'in the gas state matter has no definite volume or shape', "AIR":'a mixture of games like oxygen,carbon dioxide...', "AIR":'a mixture of games like oxygen,carbon dioxide...',
        "DNA":'Deoxyribonucleic acid','MASS':'measure of how much matter an object contains' }

lvl2={'SOLID':'in the solid state has a definite shape and volume','ORGAN':'a body part that does a special job within a body system ',
      'BRAIN':'a complex organ that controls our body','LUNGS':'pair of air-filled organs located on either side of the chest'}
lvl3={'VOLUME':'the amount of space an obiact takes up','LIQUID':'liquid state has a definite volume but has no shape of its own',
      'CONDENSES':'when a gas condenses it changes into liquid','EVAPORATES':'when the liquid evaporates it turns into gas'}
word = random.choice(list(lvl1.keys()))
guessed = []

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)

def drawButtons():
        # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
def draw():
    win.fill(WHITE)
    # draw title
    # text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    # win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = TITLE_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))
    drawButtons()
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()
    
def render_multi_line(text, x, y, fsize):
        lines = text.splitlines()
        for i, l in enumerate(lines):
            win.blit(WORD_FONT.render(l, 0, BLACK), (x, y + fsize*i))

def display_message(message):
    pygame.time.delay(100)
    win.fill(WHITE)
    render_multi_line(message,WIDTH/2 - WORD_FONT.render(message, 1, BLACK).get_width()/2,HEIGHT/2 - WORD_FONT.render(message, 1, BLACK).get_height()/2,10)
    # text = WORD_FONT.render(message, 1, BLACK)
    # win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global hangman_status
    global level
    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        
        if won:
            if (level==1):
                display_message(lvl1[word])
            elif(level==2):
                display_message(lvl2[word])
            else:
                display_message(lvl3[word])
            level+=1
            return True

        if hangman_status == 6:
            display_message("You LOST!")
            display_message("The word was: "+word)
            return False
    
while True:
    if main():
        print("here")
        hangman_status=0
        guessed=[]
        for letter in letters:
            letter[3]=True
        
        if level==2:
            word = random.choice(list(lvl2.keys()))
        elif level ==3:
            word = random.choice(list(lvl3.keys()))
        if level==4:
            display_message("You WOON!")
            pygame.quit()    
    else:
        pygame.quit()