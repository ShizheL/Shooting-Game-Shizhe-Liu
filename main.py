import pygame, sys
from pygame.locals import *
import random

pygame.init()

screen = pygame.display.set_mode((640,480))
screen_pos = [32,24]     
fpsClock = pygame.time.Clock()

player_pack = []
for x in range(62,66):
    for y in range(46, 50):
        temp = [x,y]
        player_pack.append(temp)
player_direction = 0
player_head = [[player_pack[4][0], player_pack[4][1] - 20], [player_pack[8][0], player_pack[8][1] - 20]]
dx = 0
dy = 0
speed = 0
max_speed = 5
direction_manager = {0 : [0, -1], 1 : [1, -1], 2 : [1, 0], 3 : [1, 1], 4 : [0, 1], 5 : [-1, 1], 6 : [-1, 0], 7 : [-1, -1]}

score = 0
score_timer_count = 1
score_text_setup = pygame.font.SysFont("Arial", 30)
all_bullets = []
lives = 15
lives_text_setup = pygame.font.SysFont("Arial", 30)
game_over_text_setup = pygame.font.SysFont("Arial", 80)

robot_interval = 0
game_count = 0
stage = 1
game_over = False

class Bullets():
    def __init__(self, arrow_direction, startx, starty):
        self.location = [[startx, starty]]
        self.point_direction = arrow_direction
        self.colour = (255, 255, 0)
        self.hit_player = False
        self.hit_robot = False
        if self.point_direction == 0 or self.point_direction == 4:
            for i in range(2):
                self.location.append([startx, self.location[-1][-1] + ((self.point_direction / 2) - 1)])
        elif self.point_direction == 6 or self.point_direction == 2:
            for i in range(2):
                self.location.append([self.location[-1][0] + (((-1) * (self.point_direction * 0.5)) + 2), starty])
        elif self.point_direction == 1:
            for i in range(2):
                self.location.append([self.location[-1][0] + 1, self.location[-1][-1] - 1])
        elif self.point_direction == 3:
            for i in range(2):
                self.location.append([self.location[-1][0] + 1, self.location[-1][-1] + 1])
        elif self.point_direction == 5:
            for i in range(2):
                self.location.append([self.location[-1][0] - 1, self.location[-1][-1] + 1])
        elif self.point_direction == 7:
            for i in range(2):
                self.location.append([self.location[-1][0] - 1, self.location[-1][-1] - 1])
    
    def check_robot(self):
        global robot_enemies
        if self.hit_robot == False:
            for i in range(len(robot_enemies)):
                if robot_enemies[i].alive_now == True:
                    for x in robot_enemies[i].location:
                        for y in self.location:
                            if x[0] == y[0] and x[1] == y[1]:
                                robot_enemies[i].alive_now = False
                                self.hit_robot == True
    
    def check_player(self):
        global player_pack
        global player_head
        global lives
        if self.hit_player == False:
            for i in range(len(player_head)):
                for x in self.location:
                    if player_head[i][0] == x[0] and player_head[i][1] == x[1] and self.hit_player == False:
                        self.hit_player = True
            
            for a in range(len(player_pack)):
                for b in self.location:
                    if player_pack[a][0] == b[0] and player_pack[a][1] == b[1] and self.hit_player == False:
                        self.hit_player = True

    def bullet_moove(self):
        global speed
        global direction_manager
        for i in range(len(self.location)):
            self.location[i][0] += direction_manager[self.point_direction][0] * 5
            self.location[i][1] += direction_manager[self.point_direction][1] * 5
            pygame.draw.rect(screen, self.colour, Rect((self.location[i][0] - screen_pos[0]) * 10, (self.location[i][1] - screen_pos[1]) * 10, 10, 10))

class Robots():
    def __init__(self):
        self.startp = [random.randint(5, 122), random.randint(5, 91)]
        self.location = [[self.startp[0], self.startp[1]]]
        for w in range (-2, 3):
            self.location.append([self.startp[0], self.startp[1] + w])
            self.location.append([self.startp[0] + w, self.startp[1]])
        self.colour = (255,0,0)
        self.move_steps = 0
        self.dx = random.choice([1, -1])
        self.dy = random.choice([1, -1])
        self.alive_now = True
    
    def robot_shoot(self):
        global player_pack
        global all_bullets
        can_shoot = True
        for i in player_pack:
            if i[0] == self.location[0][0]:
                if i[1] >= self.location[0][1] and can_shoot == True:
                    all_bullets.append(Bullets(4, self.location[0][0], self.location[0][1]))
                    can_shoot = False
                elif can_shoot == True:
                    all_bullets.append(Bullets(0, self.location[0][0], self.location[0][1]))
                    can_shoot = False
            elif i[1] == self.location[0][1]:
                if i[0] >= self.location[0][0] and can_shoot == True:
                    all_bullets.append(Bullets(2, self.location[0][0], self.location[0][1]))
                    can_shoot = False
                elif can_shoot == True:
                    all_bullets.append(Bullets(6, self.location[0][0], self.location[0][1]))
                    can_shoot = False
            elif (i[1] - self.location[0][1]) == (i[0] - self.location[0][0]) and can_shoot == True:
                if i[0] >= self.location[0][0]:
                    all_bullets.append(Bullets(3, self.location[0][0], self.location[0][1]))
                    can_shoot = False
                elif can_shoot == True:
                    all_bullets.append(Bullets(7, self.location[0][0], self.location[0][1]))
                    can_shoot = False
            elif (i[1] - self.location[0][1]) == (-1 * (i[0] - self.location[0][0])) and can_shoot == True:
                if i[0] >= self.location[0][0]:
                    all_bullets.append(Bullets(1, self.location[0][0], self.location[0][1]))
                    can_shoot = False
                elif can_shoot == True:
                    all_bullets.append(Bullets(5, self.location[0][0], self.location[0][1]))
                    can_shoot = False

    def robot_moove(self):
        if self.move_steps == 0:
            need_change = True
            while need_change:
                self.dx = random.choice([1, 0, -1])
                self.dy = random.choice([1, 0, -1])
                self.move_steps = random.randint(20, 100)
                xs = []
                ys = []
                for i in self.location:
                    xs.append(i[0])
                    ys.append(i[1])
                if (min(xs) + (self.dx * self.move_steps)) > 0 and (min(ys) + (self.dy * self.move_steps)) > 0 and (max(xs) + (self.dx * self.move_steps)) < 127 and (max(ys) + (self.dy * self.move_steps)) < 95:
                    need_change = False

        for m in range(len(self.location)):
            self.location[m][0] += self.dx
            self.location[m][1] += self.dy
            pygame.draw.rect(screen, self.colour, Rect((self.location[m][0] - screen_pos[0]) * 10, (self.location[m][1] - screen_pos[1]) * 10, 10, 10))
        
        self.move_steps -= 1

robot_enemies = [Robots()]

class Obstacle():
    def __init__(self):
        self.location = [random.randint(0, 127), random.randint(0, 96)]
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def goo(self):
        pygame.draw.rect(screen, self.colour, Rect((self.location[0] - screen_pos[0]) * 10, (self.location[1] - screen_pos[1]) * 10, 10, 10))

obstacles = [Obstacle() for i in range(100)]

def check_screen_pos():
    global player_pack
    global screen_pos
    if player_pack[-1][0] <= 97 and player_pack[0][0] >= 30:
        screen_pos[0] = player_pack[0][0] - 30
    if player_pack[0][0] < 30:
        screen_pos[0] = 0
    if player_pack[-1][0] > 97:
        screen_pos[0] = 64

    if player_pack[-1][1] <= 73 and player_pack[0][1] >= 23:
        screen_pos[1] = player_pack[0][1] - 22
    if player_pack[0][1] < 23:
        screen_pos[1] = 0
    if player_pack[-1][1] > 73:
        screen_pos[1] = 48

def shooot():
    global player_pack
    global player_direction
    global all_bullets
    shoot_manager = [[0, 12], [12], [12, 15], [15], [15, 3], [3], [3, 0], [0]]
    for x in shoot_manager[player_direction]:
        all_bullets.append(Bullets(player_direction, player_pack[x][0], player_pack[x][-1]))
    

def pressed_key(event):
    global speed
    global dx
    global dy
    global player_direction
    if event.key == K_RIGHT:
        player_direction += 1
    if event.key == K_LEFT:
        player_direction -= 1
    if player_direction < 0:
        player_direction = 7
    if player_direction > 7:
        player_direction = 0
    
    if event.key == K_UP:
        if speed < max_speed:
            speed += 1
        else:
            speed = max_speed
    
    if event.key == K_DOWN:
        if speed > 0:
            speed -= 1
        else:
            speed = 0

    if event.key == K_SPACE:
        shooot()

    dx = speed * direction_manager[player_direction][0]
    dy = speed * direction_manager[player_direction][1]

def set_head(a, b, xc, yc):
    global player_head
    player_head = [[player_pack[a][0] + xc, player_pack[a][1] + yc], [player_pack[b][0] + xc, player_pack[b][1] + yc]]

def set_head_diag(a, xc, yc):
    global player_head
    player_head = [[player_pack[a][0] + xc, player_pack[a][1]], [player_pack[a][0], player_pack[a][1] + yc], [player_pack[a][0] + xc, player_pack[a][1] + yc]]

def move_player():
    global player_pack
    global player_direction
    global dx
    global dy
    if 1 <= (player_pack[0][0] + dx) <= 123:
        for i in range(len(player_pack)):
            player_pack[i][0] += dx
    if 1 <= (player_pack[0][1] + dy) <= 91:
        for i in range(len(player_pack)):
            player_pack[i][1] += dy
    
    move_dist = 1
    if player_direction == 0:
        set_head(4, 8, 0, (-move_dist))
    elif player_direction == 1:
        set_head_diag(12, move_dist, -move_dist)
    elif player_direction == 2:
        set_head(13, 14, move_dist, 0)
    elif player_direction == 3:
        set_head_diag(15, move_dist, move_dist)
    elif player_direction == 4:
        set_head(7, 11, 0, move_dist)
    elif player_direction == 5:
        set_head_diag(3, -move_dist, move_dist)
    elif player_direction == 6:
        set_head(1, 2, (-move_dist), 0)
    elif player_direction == 7:
        set_head_diag(0, -move_dist, -move_dist)

def check_screen():
    global player_pack
    global obstacles
    global all_bullets
    global player_head
    global robot_interval
    robot_interval += 1
    for g in obstacles:
        g.goo()
    for i in player_pack:
        pygame.draw.rect(screen, (255, 255, 255), Rect((i[0] - screen_pos[0]) * 10, (i[1] - screen_pos[1]) * 10, 10, 10))
    for d in player_head:
        pygame.draw.rect(screen, (255, 255,255), Rect((d[0] - screen_pos[0]) * 10, (d[1] - screen_pos[1]) * 10, 10, 10))
    for p in range(len(robot_enemies)):
        if robot_enemies[p].alive_now == True:
            robot_enemies[p].robot_moove()
            if robot_interval % 5 == 0:
                robot_enemies[p].robot_shoot()
    for k in all_bullets:
        k.bullet_moove()
        k.check_robot()
        k.check_player()

def check_text():
    global lives
    global lives_text_setup
    global all_bullets
    global score
    global score_text_setup
    global game_over
    lives = 15
    for i in range(len(all_bullets)):
        if all_bullets[i].hit_player == True:
            lives -= 1
    lives_text = lives_text_setup.render("number of lives: " + str(lives), True, (255,0,0))
    lives_rect = lives_text.get_rect()
    lives_rect.top = 0
    lives_rect.left = 0
    screen.blit(lives_text, lives_rect)
    if lives <= 0:
        game_over = True
    score_text = score_text_setup.render("score: " + str(score), True, (255, 0, 0))
    score_rect = score_text.get_rect()
    score_rect.top = 0
    score_rect.left = 320
    screen.blit(score_text, score_rect)

def check_robot():
    pass

def control_stage():
    global stage
    global robot_enemies
    global game_count
    if stage < 3:
        temp_count = 0
        for i in range(len(robot_enemies)):
            if robot_enemies[i].alive_now == True:
                temp_count += 1
        if temp_count == 0:
            robot_enemies.append(Robots())
            stage += 1
    else:
        game_count += 1
        if game_count % 50 == 0:
            robot_enemies.append(Robots())

def check_score():
    global score
    global score_timer_count
    global robot_enemies
    score = 0
    score_timer_count += 1
    
    score += (int(score_timer_count / 20) * 5)
    
    for i in range(len(robot_enemies)):
        if robot_enemies[i].alive_now == False:
            score += 88

def game_over_thing():
    global game_over_text_setup
    global score
    game_over_text = game_over_text_setup.render("GAME OVER", True, (255,0,0))
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (320, 120)
    screen.blit(game_over_text, game_over_rect)
    overall_score_text = game_over_text_setup.render("SCORE: " + str(score), True, (255,0,0))
    overall_score_rect = overall_score_text.get_rect()
    overall_score_rect.center = (320, 360)
    screen.blit(overall_score_text, overall_score_rect)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and game_over == False:
            pressed_key(event)
    screen.fill((0,0,0))
    
    if game_over == False:
        control_stage()
        check_robot()
        move_player()
        check_screen_pos()
        check_score()
    
        check_screen()
        check_text()
    else:
        game_over_thing()
    
    pygame.display.flip()
    fpsClock.tick(10)