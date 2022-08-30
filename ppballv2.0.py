import pygame, sys, random
SCREEN_W, SCREEN_H = 1024, 600
BORDER_W = 10
ACCURACY, G, SPEEDY_MAX = 2, 0.01, 3
def create_new_mnet():
    x = random.randint(30, SCREEN_W - 30)
    y = random.randint(10, SCREEN_H - 150)
    w = random.randint(5, 20)
    h = random.randint(10, SCREEN_H - y)
    c = [random.randint(0, 255), random.randint(0, 255)]
    m = CLS_paddle(x, y, w, h, c)
    m.type = 1
    m.spdY = (random.random() - 0.5) * 2
    return m
def nikaiwen_show_txt( scr, txt, font, x, y, c ):
    img = font.render( txt, True, c )
    scr.blit( img, ( x, y ) )
def set_new_ball(ball):
    global gameStatus
    gameStatus = 0
    ball.x, ball.y = SCREEN_W // 2, 10
    ball.spdX = (random.random()*2 + 2) * (random.randint(0,1) * 2 - 1)
    ball.spdY = random.random()*2 + 1
def nikaiwen_draw(screen, pixel, x0, y0, scale):
    color = ( pygame.color.THECOLORS['black'],              
              pygame.color.THECOLORS['gray32'],
              pygame.color.THECOLORS['gray64'],
              pygame.color.THECOLORS['white'],
              pygame.color.THECOLORS['red'],
              pygame.color.THECOLORS['green'],
              pygame.color.THECOLORS['blue'],
              pygame.color.THECOLORS['orange'],
              pygame.color.THECOLORS['brown'],
              pygame.color.THECOLORS['purple'],
              pygame.color.THECOLORS['yellow'],
              pygame.color.THECOLORS['cyan'],
              pygame.color.THECOLORS['sienna'],
              pygame.color.THECOLORS['chocolate'],
              pygame.color.THECOLORS['coral'],
              pygame.color.THECOLORS['darkgreen'] )
    for y in range(len(pixel)):
        line = pixel[y]
        for x in range(len(line)):
            if "A" <= line[x] <= "F":
                c = color[ord(line[x]) - 55]
            elif "0" <= line[x] <= "9":
                c = color[eval(line[x])]
            else:
                continue
            pygame.draw.rect(screen, c, (x * scale + x0, y * scale + y0, scale, scale), 0)
class CLS_ball( object ):
    def __init__( self, x, y, spdX, spdY, scale ):
        self.x, self.y = x, y
        self.spdX, self.spdY = spdX, spdY
        self.scale = scale
        self.w, self.h = 0, 0
        self.interval = 16
        self.counter = 0
        self.picList = []
    def add_pic( self, pixel ):
        self.picList.append( pixel )
        self.w = len(pixel[0]) * self.scale
        self.h = len(pixel) * self.scale
    def move( self ):
        self.x += self.spdX
        self.spdY += G
        if self.spdY > SPEEDY_MAX:
            self.spdY = SPEEDY_MAX
        self.y += self.spdY
        if self.x < BORDER_W:
            self.spdX *= -1
        self.y += self.spdY
        if self.y < BORDER_W or self.y > SCREEN_H - self.h - BORDER_W:
            self.spdY *= -1
            soundPong2.play()
        self.collide( paddleL )
        self.collide( paddleR )
        self.collide( net )
        for m in mNetList:
            self.collide( m )
    def draw( self, scr ):
        nikaiwen_draw( scr, self.picList[int(self.counter / self.interval) % len(self.picList)], \
            self.x, self.y, self.scale )
        self.counter += self.spdX
    def collide( self, pad ):
        global gameStatus
        if gameStatus == 1:
            return
        if self.spdX < 0:
            distance = abs(pad.x + pad.w - self.x)
        else:
            distance = abs(self.x + self.w - pad.x)
        if distance <= ACCURACY:
            if pad.y <= self.y + self.h//2 <= pad.y + pad.h:
                self.spdX *= -1
                self.spdY += pad.spdY * pad.friction
                soundPong4.play()
            elif pad.type == 0:
                gameStatus = 1
                if self.spdX < 0:
                    paddleR.score += 1
                else:
                    paddleL.score += 1
class CLS_paddle( object ):
    def __init__( self, x, y, w, h, c = ( 200, 200, 0 ) ):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.spdY = 0
        self.c = c
        self.accY = 0
        self.friction = 0.5
        self.score = 0
        self.type = 0
    def move( self ):
        if self.type == 1:
            self.y += self.spdY
            if self.y < BORDER_W or self.y > SCREEN_H - self.h - BORDER_W:
                self.spdY *= -1
        self.spdY += self.accY
        if self.spdY <= -2 * SPEEDY_MAX:
            self.spdY = -2 * SPEEDY_MAX
        if self.spdY >= 2 * SPEEDY_MAX:
            self.spdY = 2 * SPEEDY_MAX
        self.y += self.spdY
        if self.y < BORDER_W:
            self.y = BORDER_W
            self.spdY = 0
        if self.y > SCREEN_H - self.h - BORDER_W:
            self.y = SCREEN_H - self.h - BORDER_W
            self.spdY = 0
    def draw( self,scr ):
        pygame.draw.rect(scr, self.c, (self.x, self.y, self.w, self.h), 0)
def draw_field( scr ):
    c = pygame.color.THECOLORS["brown"]
    pygame.draw.rect(scr, c, (0, 0, SCREEN_W, BORDER_W), 0)
    pygame.draw.rect(scr, c, (0, SCREEN_H - BORDER_W, SCREEN_W, BORDER_W), 0)
    nikaiwen_show_txt( scr, "倪凯文的游戏球", font64, 300, 200, (255, 255, 0) )
    nikaiwen_show_txt( scr, "SCORE:"+str(paddleL.score), font32, 50, 20, paddleL.c )
    nikaiwen_show_txt( scr, "SCORE:"+str(paddleR.score), font32, 850, 20, paddleR.c )
#----- pygame init -----
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("nikaiwen - PingPong Ball")
clock = pygame.time.Clock()
font64 = pygame.font.Font("simkai.ttf", 64)
font32 = pygame.font.Font("simkai.ttf", 32)
#----- data init -----
ball = CLS_ball(10, 10, 2, 2, 3)
paddleL = CLS_paddle(0, 200, 10, 150, c = (255,0,0))
paddleR = CLS_paddle(SCREEN_W - BORDER_W, 200, 10, 150, c = (0,0,255))
net = CLS_paddle(SCREEN_W // 2, SCREEN_H - 150, 10, 150, c = (128,128,128))
net.type = 1

pixel = [ ]
pixel.append("....DD....")
pixel.append("..DDAADD..")
pixel.append(".DDDAADDD.")
pixel.append(".DDDAADDD.")
pixel.append("DDDDAADDDD")
pixel.append("DDDDAADDDD")
pixel.append(".DDDAADDD.")
pixel.append(".DDDAADDD.")
pixel.append("..DDAADD..")
pixel.append("....DD....")
ball.add_pic( pixel )

pixel = [ ]
pixel.append("....DD....")
pixel.append("..DDDDDD..")
pixel.append(".DDDDDDAD.")
pixel.append(".DDDDDAAD.")
pixel.append("DDDDDAADDD")
pixel.append("DDDDAADDDD")
pixel.append(".DDAADDDD.")
pixel.append(".DAADDDDD.")
pixel.append("..DDDDDD..")
pixel.append("....DD....")
ball.add_pic( pixel )

pixel = [ ]
pixel.append("....DD....")
pixel.append("..DDDDDD..")
pixel.append(".DDDDDDDD.")
pixel.append(".DDDDDDDD.")
pixel.append("DAAAAAAAAD")
pixel.append("DAAAAAAAAD")
pixel.append(".DDDDDDDD.")
pixel.append(".DDDDDDDD.")
pixel.append("..DDDDDD..")
pixel.append("....DD....")
ball.add_pic( pixel )

pixel = [ ]
pixel.append("....DD....")
pixel.append("..DDDDDD..")
pixel.append(".DADDDDDD.")
pixel.append(".DAADDDDD.")
pixel.append("DDDAADDDDD")
pixel.append("DDDDAADDDD")
pixel.append(".DDDDAADD.")
pixel.append(".DDDDDAAD.")
pixel.append("..DDDDDD..")
pixel.append("....DD....")
ball.add_pic( pixel )

soundPong1 = pygame.mixer.Sound("pong1.wav")
soundPong2 = pygame.mixer.Sound("pong2.wav")
soundPong3 = pygame.mixer.Sound("pong3.wav")
soundPong4 = pygame.mixer.Sound("pong4.wav")
soundPong5 = pygame.mixer.Sound("pong5.wav")
soundGo = pygame.mixer.Sound("readygo.wav")
pygame.mixer.music.load("CCCP.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops = -1)
soundGo.play()
gameStatus = 0
mNetList = []
for i in range(10):
    mNetList.append(create_new_mnet())
while True:#----- main loop -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == ord("w"):
                paddleL.accY = -0.5
            elif event.key == ord("s"):
                paddleL.accY = 0.5
            elif event.key == pygame.K_UP:
                paddleR.accY = -0.5
            elif event.key == pygame.K_DOWN:
                paddleR.accY = 0.5
            elif event.key == pygame.K_SPACE:
                set_new_ball(ball)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddleR.spdY, paddleR.accY = 0, 0
            if event.key in (ord("w"), ord("s")):
                paddleL.spdY, paddleL.accY = 0, 0
    screen.fill((0, 64, 0))
    draw_field( screen )
    ball.move( )
    ball.draw( screen )
    paddleL.move( )
    paddleL.draw( screen )
    paddleR.move( )
    paddleR.draw( screen )
    net.move( )
    net.draw( screen )
    for m in mNetList:
        m.move()
        m.draw( screen )
    if random.random() < 0.001:
        mNetList.pop(random.randint(0, len(mNetList) - 1))
        mNetList.append(create_new_mnet())
    pygame.display.update()
    clock.tick(200)
