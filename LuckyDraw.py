import pygame
import numpy as np

pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512, devicename=None)
pygame.init()

# load music file and play
# pygame.mixer.music.set_volume(0.1)
# pygame.mixer.music.load('music.mp3')
# pygame.mixer.music.play(-1)

# load sound effect files, must be .wav
# bullet_sound = pygame.mixer.Sound('bullet.wav')
# bullet_sound.set_volume(0.1)
# hit_sound = pygame.mixer.Sound('hit.wav')
# hit_sound.set_volume(0.1)
# restore_sound = pygame.mixer.Sound('restore.wav')
# restore_sound.set_volume(0.1)

# load background image from current working directory
# bg = pygame.image.load('bg.jpg')

# define the surface
surf_width = 1280
surf_height = 720
window = pygame.display.set_mode(size=(surf_width, surf_height))  # width x height of surface
pygame.display.set_caption("Lucky Draw")


class Button:
    buttons = []

    def __init__(self, x, y, text, font_size=20, font='arial', color=(180, 50, 0), transparent=True):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.font = font
        self.color = color
        font = pygame.font.SysFont(self.font, self.font_size)
        text = font.render(self.text, True, self.color)
        self.width = int(text.get_width() + 4)
        self.height = int(text.get_height() + 4)
        self.bounding_box = (self.x, self.y, self.width, self.height)
        self.buttons.append(self)
        self.transparent = transparent
        self.bg_color = (255, 255, 255)
        self.border_color = color
        self.border_width = 2
        self.clickCount = 0

    def update_bounding_box(self):
        self.bounding_box = (self.x, self.y, self.width, self.height)

    def draw(self, window):
        if not self.transparent:
            pygame.draw.rect(window, self.bg_color, self.bounding_box)
        if self.clickCount > 0:
            pygame.draw.rect(window, (255, 255, 0), self.bounding_box)
        pygame.draw.rect(window, self.border_color, self.bounding_box, self.border_width)
        font = pygame.font.SysFont(self.font, self.font_size)
        text = font.render(self.text, True, self.color)
        window.blit(text, [self.x+2, self.y+2])

    def check_collision(self):
        if self.x <= mouse_position[0] <= self.x + self.width and self.y <= mouse_position[1] <= self.y + self.height:
            self.transparent = False
            return True
        else:
            self.transparent = True


class Text:
    texts = []

    def __init__(self, x, y, text, font_size=10, font='arial', color=(0, 0, 0), transparent=True):
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.font = font
        self.color = color
        font = pygame.font.SysFont(self.font, self.font_size)
        text = font.render(self.text, True, self.color)
        self.width = int(text.get_width() + 4)
        self.height = int(text.get_height() + 4)
        self.bounding_box = (self.x, self.y, self.width, self.height)
        self.texts.append(self)
        self.transparent = transparent
        self.border_color = color

    def update_bounding_box(self):
        self.bounding_box = (self.x, self.y, self.width, self.height)

    def draw(self, window):
        font = pygame.font.SysFont(self.font, self.font_size)
        text = font.render(self.text, True, self.color)
        window.blit(text, [self.x+2, self.y+2])


def redraw_game_window():
    # window.blit(bg, [0, 0])  # set background to image from [0, 0] position
    pygame.draw.rect(window, (100, 100, 100), (0, 0, surf_width, surf_height))

    for button in Button.buttons:  # draw buttons
        button.draw(window)

    for text in Text.texts:  # draw scrolling names
        text.draw(window)
    pygame.draw.rect(window, (0, 255, 0), (int(surf_width * 0.4 - 400 / 2), 360, 400, 61), 5)

    font = pygame.font.SysFont('arial', 10)  # create object with font style and font size
    text = font.render(str(mouse_position), True, (0, 0, 0))
    window.blit(text, [surf_width - text.get_width() - 5, 5])

    pygame.draw.circle(window, (255, 0, 0), mouse_position, 2)  # draw mouse position

    font = pygame.font.SysFont('arial', 30)  # draw title
    title = ["SHELL WELLS ANNUAL DINNER",
             "LUCKY DRAW",
             "xxx"]
    text = []
    for line in title:
        text.append(font.render(line, True, (0, 0, 0)))
    for line in range(len(text)):
        window.blit(text[line], [int(surf_width / 2 - text[line].get_width() / 2), line * int(text[line].get_height())])

    textlist = []  # check names in scrolling names
    for text in Text.texts:
        textlist.append(text.text)
    font = pygame.font.SysFont('arial', 7)  # draw participant lists
    text = []
    for line in list1:
        if line in textlist:
            text.append(font.render(line, True, (255, 0, 0)))
        else:
            text.append(font.render(line, True, (0, 0, 0)))
    for line in range(len(text)):
        window.blit(text[line], [2, 2 + line * int(text[line].get_height())])
    text = []
    for line in list2:
        if line in textlist:
            text.append(font.render(line, True, (255, 0, 0)))
        else:
            text.append(font.render(line, True, (0, 0, 0)))
    for line in range(len(text)):
        window.blit(text[line], [100, 2 + line * int(text[line].get_height())])

    font = pygame.font.SysFont('arial', 12)  # draw winner list
    text = font.render("Lucky winners:", True, (0, 0, 0))
    window.blit(text, [surf_width * 0.9, 100 - int(text.get_height())])
    font = pygame.font.SysFont('arial', 8)
    text = []
    for n, line in enumerate(winner_list):
        text.append(font.render(str(n+1) + ". " + line, True, (0, 0, 0)))
    for line in range(len(text)):
        window.blit(text[line], [surf_width * 0.9, 100 + line * int(text[line].get_height())])

    pygame.display.update()


# start and reset buttons
font = pygame.font.SysFont('arial', 20)
text = font.render('START', True, (0, 0, 0))
start_button = Button(int(surf_width * 0.4 - text.get_width() / 2), int(surf_height * 0.8), 'START', color=(0, 0, 200))
font = pygame.font.SysFont('arial', 10)
text = font.render('RESET', True, (0, 0, 0))
reset_button = Button(surf_width - text.get_width() - 5, surf_height - text.get_height() - 5, 'RESET', font_size=10, color=(0, 0, 200))

# initialize player list
player_list = []
# update this player_list later
# player_list = ["WONG KIM MUN",
#                "WONG TIMUN",
#                "WONG BLUE MOON"]
for n in range(130):  # placeholder
    player_list.append("Joachim " + str(n+1))
list1 = player_list[:int((len(player_list)+1)/2)]
list2 = player_list[int((len(player_list)+1)/2):]

# initialize random winner list
for n in range(6):
    font = pygame.font.SysFont('arial', 0)
    x = player_list[np.random.randint(0, len(player_list) - 1)]
    text = font.render(x, True, (0, 0, 0))
    Text(int(surf_width * 0.4 - text.get_width() / 2), int(surf_height * 0.25) + n*60, x, font_size=0)

# initialize winner list
winner_list = []
# for n in range(50):  # placeholder for testing
#     winner_list.append(str(n))

# initialize close and runtime
clock = pygame.time.Clock()
speed = 1
run = True

while run:
    clock.tick(60)  # set frame per second to max

    # define state of keyboard buttons
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        pass
    elif keys[pygame.K_RIGHT]:
        pass
    elif keys[pygame.K_DOWN]:
        pass

    # define state of mouse buttons and position
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()

    # define when to terminate loop, i.e. when click on CLOSE button (QUIT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False

    # define what mouse-clicks do
    if start_button.check_collision() and start_button.clickCount == 0:
        if mouse_buttons[0]:
            start_button.clickCount = 1

    if reset_button.check_collision() and reset_button.clickCount == 0 and len(winner_list) > 0:
        if mouse_buttons[0]:
            reset_button.clickCount = 1
            player_list.append(winner_list[-1])
            player_list.sort()
            winner_list.pop(-1)
            list1 = player_list[:int((len(player_list) + 1) / 2)]
            list2 = player_list[int((len(player_list) + 1) / 2):]

    # define delay
    if 0 < start_button.clickCount <= 300:
        start_button.clickCount += 1
        if len(Text.texts) < 6:
            if 0 < start_button.clickCount <= 50:
                speed = 4
            elif 0 < start_button.clickCount <= 150:
                speed = 2
            elif 0 < start_button.clickCount <= 300:
                speed = 1
                if start_button.clickCount > 220:
                    for text in Text.texts:
                        if text.font_size == 50:
                            speed = 0
                            winner_list.append(text.text)
                            player_list.remove(text.text)
                            list1 = player_list[:int((len(player_list) + 1) / 2)]
                            list2 = player_list[int((len(player_list) + 1) / 2):]
    else:
        start_button.clickCount = 0
        speed = 1
    if 0 < reset_button.clickCount <= 20:
        reset_button.clickCount += 1
    else:
        reset_button.clickCount = 0

    if len(Text.texts) < 6:
        font = pygame.font.SysFont('arial', 10)
        x = player_list[np.random.randint(0, len(player_list) - 1)]
        text = font.render(x, True, (0, 0, 0))
        Text(int(surf_width * 0.4 - text.get_width() / 2), int(surf_height * 0.25), x)

    for text in Text.texts:
        text.y += 3*speed
        text.font_size = int(50 * np.sin(np.pi * (text.y - surf_height * 0.25) / (6 * 60)))
        font = pygame.font.SysFont(text.font, text.font_size)
        x = font.render(text.text, True, text.color)
        text.width = int(x.get_width() + 4)
        text.height = int(x.get_height() + 4)
        text.update_bounding_box()
        text.x = int(surf_width * 0.4 - x.get_width() / 2) - 2

    for text in Text.texts:
        if text.y >= int(surf_height * 0.25) + 6*60:
            Text.texts.pop(Text.texts.index(text))

    redraw_game_window()

pygame.display.quit()
pygame.quit()
