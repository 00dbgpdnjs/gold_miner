## class
# You have to code them below as many objects as you need without class. Then You have to manage a lot of vars
# gem1.get_rect().size
# gem1_width = gem1_size[0]
# gem1_height = gem1_size[1]
# gem1_x_pos = ...
# gem1_y_pos = ...

import pygame, os, math

class Claw(pygame.sprite.Sprite): 
    def __init__(self, image, position): 
        super().__init__()
        self.original_image = image # ?? location O
        self.image = image # rotated self.original_image
        self.rect = image.get_rect(center=position)
        
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0) # Create 'offset' var/ (to x, to y)
        self.position = position # for update()
        self.direction = LEFT
        self.angle_speed = 2.5 # Increases each 2.5 degree per frame; width of angular change; movement speed
        self.angle = 10 # initial Angle (Right End)

    def update(self, to_x): # defaulted methon of Sprite class/ Update self.rect
        if self.direction == LEFT: 
            self.angle += self.angle_speed # + ?? -> not angle, but speed
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed

        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT) # Use the method instead of 'self.direction = RIGHT'
        elif self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x # claw launch
        self.rotate()

        #print(self.angle, self.direction)
        # rect_center = self.position + self.offset
        # self.rect = self.image.get_rect(center=rect_center)
    def rotate(self):
        #pass
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1) # rotate + zoom / (,, No image size change)

        offset_rotated = self.offset.rotate(self.angle) # the func defaulted of Vector2 caculate automatically offset by ()
        #print(offset_rotated) # I checked the var before reflecting in rect (below)

        self.rect = self.image.get_rect(center=self.position+offset_rotated)
        #print(self.rect) # (x,y,width,height) ?? why are x,y fixed -> position of 'claw=Claw(,position)' (without code above)

        #pygame.draw.rect(screen, RED, self.rect, 1)     

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen): # to draw anything
        screen.blit(self.image, self.rect) # We can't use parameters of other area, so we use its var.
        #pygame.draw.circle(screen, RED, self.position, 3) # (,,, radius)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # (,,from here,to here,thickness)

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT

# Create a new class(Gemstone) from Sprite which is a parents class
# to define which image and its pos 
# object is each gemstone
class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position, price, speed): # Define requisitely initialization method/ (which image, pos of each gemstone,,claw speed base on caught gem)
        super().__init__() # (for a parents class)
        self.image = image # Define requisitely 2 vars(image, rect) 
        self.rect = image.get_rect(center=position)
        self.price = price # ??
        self.speed = speed
 # Ready to use this class

    def set_position(self, position, angle): # When the claw and gem collide, Change the position of the gem so that the red dot, claw and gem are in a straight line. And caught gem follows the claw./ (,Center coordinates of the claw,)
        r = self.rect.size[0] // 2 # radius # refer to 'draw_radians.png'
        rad_angle = math.radians(angle) # Theta θ / refer to 'radians.py'
        to_x = r * math.cos(rad_angle) # Bottom of Triangle x = r * cosθ
        to_y = r * math.sin(rad_angle) # Height of Triangle y = r * sinθ
        self.rect.center = (position[0] + to_x, position[1] + to_y) # gem repositino


def setup_gemstone():
    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamond_price, diamond_speed = 600, 7

    # small gold
    small_gold = Gemstone(gemstone_images[0], (200, 380), small_gold_price, small_gold_speed) # (image, position,price,speed) 
    gemstone_group.add(small_gold) 
    gemstone_group.add(Gemstone(gemstone_images[0], (400, 400), small_gold_price, small_gold_speed))
    gemstone_group.add(Gemstone(gemstone_images[0], (600, 450), small_gold_price, small_gold_speed))
    gemstone_group.add(Gemstone(gemstone_images[0], (800, 400), small_gold_price, small_gold_speed))
    gemstone_group.add(Gemstone(gemstone_images[0], (1150, 380), small_gold_price, small_gold_speed))

    # big gold
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500), big_gold_price, big_gold_speed))
    gemstone_group.add(Gemstone(gemstone_images[1], (800, 500), big_gold_price, big_gold_speed))

    # stone
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380), stone_price, stone_speed))
    gemstone_group.add(Gemstone(gemstone_images[2], (700, 330), stone_price, stone_speed))
    gemstone_group.add(Gemstone(gemstone_images[2], (1000, 480), stone_price, stone_speed))

    # diamond
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420), diamond_price, diamond_speed))
    gemstone_group.add(Gemstone(gemstone_images[3], (150, 500), diamond_price, diamond_speed))

def update_score(score): # ??
    global curr_score
    curr_score += score

def display_score():
    txt_curr_score = game_font.render(f"Curr Score : {curr_score:,}", True, BLACK) #(which,antialias,)/ ':,' : Comma every three digits
    screen.blit(txt_curr_score, (50, 20))

    txt_goal_score = game_font.render(f"Goal Score : {goal_score:,}", True, BLACK)
    screen.blit(txt_goal_score, (50, 80))

def display_time(time):
    txt_timer = game_font.render(f"Time : {time}", True, BLACK)
    screen.blit(txt_timer, (1100, 50))

def display_game_over():
    game_font = pygame.font.SysFont("arialrounded", 60)
    txt_game_over = game_font.render(game_result, True, BLACK)
    rect_game_over = txt_game_over.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(txt_game_over, rect_game_over)

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("arialrounded", 30) # When using just Fond and sharing this file, an error occurs/ (basic+round,)/ refer to Check_font.py

goal_score = 1500
curr_score = 0

# ralated to gameover
game_result = None
total_time = 60
start_ticks = pygame.time.get_ticks()

# vars related to game
default_offset_x_claw = 40
to_x = 0 # store a value to move the claw image based on x-coordinate
caught_gemstone = None

move_speed = 12 # launch speed; increase x-coordinate
return_speed = 20 # when returning with nothing 

LEFT = -1 # to the left
STOP = 0
RIGHT = 1

RED = (255, 0, 0)
BLACK = (0, 0, 0)

current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "big_gold.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "stone.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "diamond.png")).convert_alpha()]
    # convert_alpha(): Changes the imported image to an alpha image to give the image transparency

# If you create a group, you don't need to code 'blit' as many gems as you have.
gemstone_group = pygame.sprite.Group() # Create a group / A next function that adds gem objects created by Gemstone class one by one to this var
setup_gemstone()

Claw_image = pygame.image.load(os.path.join(current_path, "claw.png")).convert_alpha() 
claw = Claw(Claw_image, (screen_width // 2, 110)) # (image, position)

running = True
while running: 
    clock.tick(30) # FPS = 30; Fixed game speed on any computers

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Click X btn
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            claw.set_direction(STOP)
            to_x = move_speed

    # boundry value
    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw:
        to_x = 0
        claw.set_init_state()

        if caught_gemstone:
            update_score(caught_gemstone.price)
            gemstone_group.remove(caught_gemstone)
            caught_gemstone = None # ?? -> It's not same to the code above

    if not caught_gemstone: # when 'caught_gemstone' is, I don't have to check collision
        for gemstone in gemstone_group: # bring a Sprite one by one in the group
            #if claw.rect.colliderect(gemstone.rect):
            if pygame.sprite.collide_mask(claw, gemstone): # excluding transparent regions (however, set alpha to code loading the image)
                caught_gemstone = gemstone
                to_x = -gemstone.speed # This code just change value of 'to_x' And caculation code is 'self.offset.x += to_x' 
                #break # ?? -> I don't have to need

    if caught_gemstone:
        caught_gemstone.set_position(claw.rect.center, claw.angle)

    screen.blit(background, (0, 0))
    gemstone_group.draw(screen) # Draw all Sprite in the group on the screen
    claw.update(to_x) # Update the info of the rect
    claw.draw(screen) # There is draw func in Group(), but there is no draw func in each Sprite. So Create draw func in Claw class
    # 'screen.blit(claw.image, claw.position)' is also possible, but process is in the class

    display_score()

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ex) 1234 -> 1.234
    display_time(total_time - int(elapsed_time)) # ex) 1.234 -> 1

    if total_time - int(elapsed_time) <= 0:
        running = False
        if curr_score >= goal_score:
            game_result = "Mission Complete"
        else:
            game_result = "Game Over"
        display_game_over()


    pygame.display.update() # Reflect[update] images

pygame.time.delay(2000)
pygame.quit()