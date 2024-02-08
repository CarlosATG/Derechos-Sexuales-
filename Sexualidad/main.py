#from pygame import *
import pygame, sys
import spritesheet
from button import Button

pygame.init()
pygame.mixer.music.load("8bit.mp3")
pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely
pygame.mixer.music.set_volume(.05)
JumpS= pygame.mixer.Sound("assets/jump.mp3")
JumpS.set_volume(0.05)
JumpC = pygame.mixer.Sound('assets/Correct!.mp3')
JumpC.set_volume(0.5)
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
#Fondos
medalla = pygame.image.load('assets/Medallas1.png')
BG = pygame.image.load("assets/Arcoiris.png")
GBG = pygame.image.load("assets/gameBG.png")
Lab = pygame.image.load("assets/Lab.png")
Siguiente = pygame.image.load("assets/next.png").convert_alpha()
Back= pygame.image.load("assets/back.png").convert_alpha()
BG_Mensajes= pygame.image.load("assets/Messages.png").convert_alpha()
font =pygame.font.Font("assets/Pixel_like.ttf",24)
timer=pygame.time.Clock()
snip = font.render('', True, 'black')
speed= 2
done= False
flecha = pygame.image.load('assets/Pointer.png')
mute = pygame.image.load('assets/muteBtn.png').convert()
mute_rect= mute.get_rect()
mute_rect.center=(25,20 )
#Animaciones
RosaIdle= pygame.image.load("Rosa/Pink_Monster_Idle_4.png").convert_alpha()
RosaI = spritesheet.SpriteSheet(RosaIdle)
RosaWalkingR= pygame.image.load("Rosa/Pink_Monster_Walk_6.png").convert_alpha()
RosaWR = spritesheet.SpriteSheet(RosaWalkingR)
RosaWalkingLeft= pygame.transform.flip(RosaWalkingR, True, False)
RosaWL =spritesheet.SpriteSheet(RosaWalkingLeft)
RosaJumping= pygame.image.load("Rosa/Pink_Monster_Jump_8.png").convert_alpha()
RosaJ = spritesheet.SpriteSheet(RosaJumping)
#Lista de Animaciones
Rosa_idle = []
Rosa_walking_right= []
Rosa_walking_Left= []
Rosa_jumping=[]
animation_steps= [4, 6, 8]
Transparente = (0,0,0) #fondo de las animaciones
last_update = pygame.time.get_ticks()
animation_cooldown = 500
frame =0
for x in range (animation_steps[0]):
    Rosa_idle.append(RosaI.get_image(x, 32, 34, 7, Transparente))
for x in range (animation_steps[1]):
    Rosa_walking_right.append(RosaWR.get_image(x, 32, 34, 7, Transparente))
for x in range(animation_steps[2]):
    Rosa_jumping.append(RosaJ.get_image(x, 32, 34, 7, Transparente))
for x in range (animation_steps[1]):
    Rosa_walking_Left.append(RosaWL.get_image(x, 32, 34, 7, Transparente))
AzulIdle= pygame.image.load("Azul/Dude_Monster_Idle_4.png").convert_alpha()
AzulI = spritesheet.SpriteSheet(AzulIdle)
AzulWalkingR= pygame.image.load("Azul/Dude_Monster_Walk_6.png").convert_alpha()
AzulWR = spritesheet.SpriteSheet(AzulWalkingR)
AzulWalkingLeft= pygame.transform.flip(AzulWalkingR,True, False)
AzulWL =spritesheet.SpriteSheet(AzulWalkingLeft)
AzulJumping= pygame.image.load("Azul/Dude_Monster_Jump_8.png").convert_alpha()
AzulJ = spritesheet.SpriteSheet(AzulJumping)
#Lista de Animaciones
Azul_idle = []
Azul_walking_right= []
Azul_walking_Left= []
Azul_jumping=[]
animation_cooldown = 75
frame =0
for x in range (animation_steps[0]):
    Azul_idle.append(AzulI.get_image(x, 32, 34, 7, Transparente))
for x in range (animation_steps[1]):
    Azul_walking_right.append(AzulWR.get_image(x, 32, 34, 7, Transparente))
for x in range(animation_steps[2]):
    Azul_jumping.append(AzulJ.get_image(x, 32, 34, 7, Transparente))
for x in range (animation_steps[1]):
    Azul_walking_Left.append(AzulWL.get_image(x, 32, 34, 7, Transparente))
class boton():
    def __init__(self, x,y,image, scale):
        width=image.get_width()
        height = image.get_height()
        self.image= pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False
    def draw(self):
        pos= pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                print('CLICKED')
        SCREEN.blit(self.image,(self.rect.x,self.rect.y))

Btn_Siguiente=boton(1200,20,Siguiente, 0.05)
Btn_Back=boton(30,20,Back, 0.05)
Btn_Message=boton(0, 520, BG_Mensajes, 1)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/04B_30__.TTF", size)


def Tutorial(color):
    TutorialBg = pygame.image.load('assets/TutBG.png')
    if color == "Blue":
        Personaje = Azul_idle
        moveR = Azul_walking_right
        moveL = Azul_walking_Left
        Jump = Azul_jumping
    else:
        Personaje = Rosa_idle
        moveR = Rosa_walking_right
        moveL = Rosa_walking_Left
        Jump = Rosa_jumping
    counter = 0
    message=''
    jumping = False
    frame_rate= 3
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/Pixel_like.ttf", 24)
    screen_width, screen_height = SCREEN.get_size()
    last_update = pygame.time.get_ticks()
    frame =0
    Preguntas= ["Bienvenido! para moverte usa las felchas en tu teclado.",
                "Salta con Up si entendiste ",
                "A) Esta claro",
                "B) No entendi",
                "Ya estas listo, presiona ENTER para continuar...",
                ]
    SCREEN.fill((255, 255, 255))  # Clear screen
    x= 300
    y= 250
    Y_gravity= 1
    Jump_height =14
    Y_velocity =Jump_height
    level = 0
    Correcto =0
    jumpvfx = True
    music_paused = True
    while True:
        SCREEN.fill((255, 255, 255))  # Clear screen
        timer.tick(60)
        SCREEN.blit(TutorialBg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # Exit the
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    level += 1
                    if level >= 1:
                        SegundoNivel(color)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jumping =True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mute_rect.collidepoint(event.pos):
                    # Toggle the boolean variable.
                    music_paused = not music_paused
                    if music_paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        SCREEN.blit(mute, mute_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if x < 1100:
                x+= 10
                SCREEN.blit(moveR[frame], (x, y))
            else :SCREEN.blit(Personaje[frame], (x,y))
        elif keys[pygame.K_LEFT]:
            if x > 0:
                x-=10
                SCREEN.blit(moveL[frame], (x, y))
            else : SCREEN.blit(Personaje[frame], (x,y))
        else: SCREEN.blit(Personaje[frame], (x,y))
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(Rosa_idle): frame = 0
        # Display the message
        if level == 0:
            for i in range (4):
                speed = 3
                if counter < speed *len(Preguntas[i]):
                    counter +=1
                elif counter >=speed*len(Preguntas[i]):
                    done = True
                snip= font.render(Preguntas[i][0:counter//speed], True, 'Black')
                SCREEN.blit(snip,(38,560+(25*i)))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                speed = 3
                if counter < speed *len(Preguntas[4]):
                    counter +=1
                elif counter >=speed*len(Preguntas[4]):
                    done = True
                snip= font.render(Preguntas[4][0:counter//speed], True, 'Black')
                SCREEN.blit(snip,(38,560))
        if jumping:
            y -= Y_velocity
            Y_velocity -= Y_gravity
            if x >= 100 and x<= 270 and level == 0:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if x >= 850 and x <= 1050 and level == 0:
                Correcto = 2
            if Y_velocity <- Jump_height:
                jumping= False
                Y_velocity = Jump_height
                SCREEN.blit(Jump[frame], (x,y))
        if message:
            font = pygame.font.Font("assets/Pixel_like.ttf", 24)
            text = font.render(message, True, (0, 0, 0))
            SCREEN.blit(text, (screen_width // 4, screen_height // 2))
        pygame.display.flip()

def FirstLevel():
    counter = 0
    message=""
    font = pygame.font.Font("assets/Pixel_like.ttf", 24)
    screen_width, screen_height = SCREEN.get_size()
    last_update = pygame.time.get_ticks()
    frame =0
    running = True
    Primer_Mensaje= 'Escoge a tu personaje con las flechas del teclado y presiona enter...'
    SCREEN.fill((255, 255, 255))  # Clear screen
    Left = True
    music_paused= False
    while True:
        timer.tick(60)
        SCREEN.blit(GBG, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # Exit the function
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    Left = False
                if event.key == pygame.K_RETURN and Left == False:
                        Tutorial("Blue")
                elif event.key == pygame.K_LEFT:
                    Left = True
                if event.key == pygame.K_RETURN and Left == True:
                    Tutorial("Rosa")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        jumping = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mute_rect.collidepoint(event.pos):
                        # Toggle the boolean variable.
                        music_paused = not music_paused
                        if music_paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

        SCREEN.blit(mute, mute_rect)
        Btn_Message.draw()
        current_time = pygame.time.get_ticks()
        if Left == True: SCREEN.blit(flecha, (250, 150))
        else: SCREEN.blit(flecha, (770, 150))
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(Rosa_idle): frame = 0
        # Display the message
        if counter < speed *len(Primer_Mensaje):
            counter +=1
        elif counter >=speed*len(Primer_Mensaje):
            done = True
        snip= font.render(Primer_Mensaje[0:counter//speed], True, 'Black')
        SCREEN.blit(snip,(48,660))
        SCREEN.blit(Rosa_idle[frame], (300, 250))
        SCREEN.blit(Azul_idle[frame], (800, 250))
        if message:
            font = pygame.font.Font("assets/Pixel_like.ttf", 24)
            text = font.render(message, True, (0, 0, 0))
            SCREEN.blit(text, (screen_width // 4, screen_height // 2))

        pygame.display.flip()

def SegundoNivel(color):
    Dosopciones = pygame.image.load('assets/C2.png')
    Tresopciones = pygame.image.load('assets/C3.png')
    medalla = pygame.image.load('assets/Med1.png')
    BarraProg = pygame.image.load('assets/Prog2.png')
    jumpvfx = True
    music_paused= False
    racha1 = True
    if color == "Blue":
        Personaje = Azul_idle
        moveR = Azul_walking_right
        moveL = Azul_walking_Left
        Jump = Azul_jumping
    else:
        Personaje = Rosa_idle
        moveR = Rosa_walking_right
        moveL = Rosa_walking_Left
        Jump = Rosa_jumping
    counter = 0
    message=''
    jumping = False
    frame_rate= 3
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/Pixel_like.ttf", 24)
    screen_width, screen_height = SCREEN.get_size()
    last_update = pygame.time.get_ticks()
    frame =0
    running = True
    Preguntas= ["Las hormonas son sustancias químicas que comunican células a larga distancia.",
                "Entre estas hormonas, las sexuales, como la testosterona, el estradiol y ",
                "la progesterona, desarrollan los caracteres sexuales de un individuo. ",
                "Se ha observado que los hombres con mucha testosterona son musculosos,",
                "tienen la voz más gruesa y tienen mucha barba. Presiona Enter para continuar",
                '¿Crees que un nivel bajo de testosterona en hombres',
                ' haga que les gusten los hombres?',
                'A) SI',
                'B) NO',
                '¡Correcto! Aunque las hormonas sexuales desempeñan un papel importante en el ',
                'desarrollo de caracteres sexuales secundarios, la elección de parejas es una ',
                'expresión compleja que se ve afectada por múltiples factores, no simplemente ',
                'por los niveles hormonales. Presiona Enter para continuar',
                'Nombre, estas loco',
                "Los genes, almacenan toda clase de información",
                "Desde el color de tu pelo, hasta muchas de tus conductas.",
                "En base a esto, ¿Crees que existe un gen homosexual?",
                'A) SI',
                'B) NO',
                'Piénsalo de nuevo',
                "Así es: Existen múltiples genes, en distintos cromosomas que se creen",
                "impactan en la orientación sexual de un individuo.Presiona Enter para continuar",
                "¿Cuál de las siguientes hipótesis tienen más evidencia en el desarrollo ",
                "de la orientación sexual?",
                "A)Jugar con juguetes de niño si eres niña.",
                "B)La respuesta inmune de tu madre durante el embarazo.",
                "C) Una alta densidad molecular en la concentración de feromonas masculinas ",
                "en el sistema exocrino femenino.",
                "Una de las posibles hipótesis es la de la respuesta inmune durante el embarazo,",
                "misma que aumenta conforme va teniendo más hijos. Enter para continuar",
                "Felicidades, ya tienes la medalla de este nivel!",
                "Continua aprendiendo para ganar mas"
                ]
    SCREEN.fill((255, 255, 255))  # Clear screen
    x= 300
    y= 250
    Y_gravity= 1
    Jump_height =14
    Y_velocity =Jump_height
    level = 0
    Correcto =0
    while True:
        SCREEN.fill((255, 255, 255))  # Clear screen
        timer.tick(60)
        SCREEN.blit(Lab, (0,0))
        SCREEN.blit(BarraProg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # Exit the
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    level += 1
                    Correcto =0
                    jumpvfx = True
                    if level >= 5:
                        TercerNivel(color, racha1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    JumpS.play()
                    jumping =True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mute_rect.collidepoint(event.pos):
                        # Toggle the boolean variable.
                        music_paused = not music_paused
                        if music_paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

        SCREEN.blit(mute, mute_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if x < 1100:
                x+= 20
                SCREEN.blit(moveR[frame], (x, y))
            else :SCREEN.blit(Personaje[frame], (x,y))
        elif keys[pygame.K_LEFT]:
            if x > 0:
                x-=20
                SCREEN.blit(moveL[frame], (x, y))
            else : SCREEN.blit(Personaje[frame], (x,y))
        #elif keys[pygame.K_UP]:
            #jumping = True
        else: SCREEN.blit(Personaje[frame], (x,y))
        Btn_Message.draw()
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(Rosa_idle): frame = 0
        # Display the message
        if level == 0:
            for i in range (5):
                speed = 3
                if counter < speed *len(Preguntas[i]):
                    counter +=1
                elif counter >=speed*len(Preguntas[i]):
                    done = True
                snip= font.render(Preguntas[i][0:counter//speed], True, 'Black')
                SCREEN.blit(snip,(38,560+(25*i)))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    level = 1
                    return
        if level == 1:
            for i in range(5,9):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * (i-4))))
            SCREEN.blit(Dosopciones, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(9, 13):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 8))))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[13]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[13]):
                        done = True
                    snip = font.render(Preguntas[13][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 2:
            for i in range(14,19):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * (i-14))))
            SCREEN.blit(Dosopciones, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(20, 22):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 20))))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[19]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[19]):
                        done = True
                    snip = font.render(Preguntas[19][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 3:
            for i in range(22,28):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (22 * (i-22))))
            SCREEN.blit(Tresopciones, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(28, 30):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 28))))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[19]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[19]):
                        done = True
                    snip = font.render(Preguntas[19][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 4 and racha1 == True:
            SCREEN.blit(medalla, (0,0))
            for i in range(30, 32):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * (i - 30))))
        if jumping:
            y -= Y_velocity
            Y_velocity -= Y_gravity
            #JumpS.play()
            if x >= 100 and x<= 270 and level == 1:
                Correcto = 2
                racha1 = False
            if x >= 850 and x <= 1050 and level == 1:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx= False
            if x >= 100 and x<= 270 and level == 2:
                Correcto = 2
                racha1 = False
            if x >= 950 and x <= 1150 and level == 2:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx= False
            if x >= 100 and x <= 270 and level == 3:
                    Correcto = 2
                    racha1 = False
            if x >= 500 and x <= 750 and level == 3:
                    Correcto = 1
                    if jumpvfx:
                        JumpC.play()
                        jumpvfx= False
            if x >= 850 and x<= 1050 and level == 3:
                Correcto = 2
                racha1 = False
            if Y_velocity <- Jump_height:
                jumping= False
                Y_velocity = Jump_height
                SCREEN.blit(Jump[frame], (x,y))
        if message:
            font = pygame.font.Font("assets/Pixel_like.ttf", 24)
            text = font.render(message, True, (0, 0, 0))
            SCREEN.blit(text, (screen_width // 4, screen_height // 2))
        pygame.display.flip()
############################################################################################################
def TercerNivel(colour, racha1):
    music_paused = False
    NeuroBG= pygame.image.load('assets/Neuro.png')
    DosopcionesND = pygame.image.load('assets/NeuroOpc.png')
    medalla = pygame.image.load('assets/Med1.png')
    BarraProg = pygame.image.load('assets/Prog3.png')
    racha2 = True
    if colour == "Blue":
        Personaje = Azul_idle
        moveR = Azul_walking_right
        moveL = Azul_walking_Left
        Jump = Azul_jumping
    else:
        Personaje = Rosa_idle
        moveR = Rosa_walking_right
        moveL = Rosa_walking_Left
        Jump = Rosa_jumping
    counter = 0
    message=''
    jumping = False
    frame_rate= 3
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/Pixel_like.ttf", 24)
    screen_width, screen_height = SCREEN.get_size()
    last_update = pygame.time.get_ticks()
    frame =0
    running = True
    Preguntas= ["Tu cerebro se comunica por químicos, llamados neurotransmisores. Estos están",
                "involucrados en todos los aspectos de la conducta y la cognición. La serotonina",
                "(que no es el neurotransmisor feliz) nos impulsa a tener conductas sexuales"
                " y afectivas. ¿Crees que la serotonina de las personas ",
                " homosexuales sea diferentea la de los heterosexuales?",
                'A) SI      B) NO',
                '¡Así es! No hay diferencia en la forma o función de los neurotransmisores',
                'de personas heterosexuales u homosexuales. Aunque existe evidencia que ',
                'parece indicar diferencias sutiles en dichos sistemas de neurotransmisión.',
                "Enter para continuar",
                'Piénsalo de nuevo',
                'La oxitocina es un neurotransmisor involucrado en la conducta de afiliación,',
                'cariño y monogamia.Las personas solemos buscar la sensación que este sistema ',
                'de neurotransmisión nos da, pues se relaciona con el placer y el bienestar?',
                '¿Generar mucha oxitocina/sentirme bien con personas del mismo sexo me vuelve homosexual?',
                'A) SI      B) NO',
                'Efectivamente. Ningún neurotransmisor puede, por sí solo, “enamorarte de una ',
                'persona”, es más, podemos liberar dicho químico con personas a las que estimamos',
                'mucho, como nuestros amigos y familiares cercanos. Enter para continuar',
                "Felicidades, ya tienes la medalla de este nivel!",
                "Continua aprendiendo para ganar mas",
                "No obtuviste le medalla, continua al siguiente nivel"
                ]
    SCREEN.fill((255, 255, 255))  # Clear screen
    x= 300
    y= 250
    Y_gravity= 1
    Jump_height =14
    Y_velocity =Jump_height
    level = 1
    Correcto =0
    jumpvfx = True
    while True:
        SCREEN.fill((255, 255, 255))  # Clear screen
        timer.tick(60)
        SCREEN.blit(NeuroBG, (0,0))
        SCREEN.blit(BarraProg, (0, 0))
        if racha1 == True:
            SCREEN.blit(medalla, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # Exit the
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    level += 1
                    Correcto = 0
                    jumpvfx = True
                    if level >= 4:
                        CuartoNivel(colour, racha1, racha2)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jumping =True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mute_rect.collidepoint(event.pos):
                        # Toggle the boolean variable.
                        music_paused = not music_paused
                        if music_paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

        SCREEN.blit(mute, mute_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if x < 1100:
                x+= 10
                SCREEN.blit(moveR[frame], (x, y))
            else :SCREEN.blit(Personaje[frame], (x,y))
        elif keys[pygame.K_LEFT]:
            if x > 0:
                x-=10
                SCREEN.blit(moveL[frame], (x, y))
            else : SCREEN.blit(Personaje[frame], (x,y))
        #elif keys[pygame.K_UP]:
            #jumping = True
        else: SCREEN.blit(Personaje[frame], (x,y))
        Btn_Message.draw()
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(Rosa_idle): frame = 0
        # Display the message
        if level == 1:
            for i in range(5):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * i)))
            SCREEN.blit(DosopcionesND, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(5, 9):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 5))))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[9]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[9]):
                        done = True
                    snip = font.render(Preguntas[9][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 2:
            for i in range(10,15):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * (i-10))))
            SCREEN.blit(DosopcionesND, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(15,18):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 15))))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[9]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[9]):
                        done = True
                    snip = font.render(Preguntas[9][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 3:
            if racha2 == True:
                medallados = pygame.image.load('assets/Med2.png')
                SCREEN.blit(medallados, (0,0))
                for i in range(18, 20):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 18))))
            else:
                SCREEN.blit(BG_Mensajes, (0, 520))
                speed = 3
                if counter < speed * len(Preguntas[20]):
                    counter += 1
                elif counter >= speed * len(Preguntas[20]):
                    done = True
                snip = font.render(Preguntas[20][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560))
        if jumping:
            y -= Y_velocity
            Y_velocity -= Y_gravity
            if x >= 100 and x<= 270 and level == 1:
                Correcto = 2
                racha2 =False
            if x >= 850 and x <= 950 and level == 1:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if x >= 100 and x<= 270 and level == 2:
                Correcto = 2
                racha2 = False
            if x >= 850 and x <= 950 and level == 2:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if Y_velocity <- Jump_height:
                jumping= False
                Y_velocity = Jump_height
                SCREEN.blit(Jump[frame], (x,y))
        if message:
            font = pygame.font.Font("assets/Pixel_like.ttf", 24)
            text = font.render(message, True, (0, 0, 0))
            SCREEN.blit(text, (screen_width // 4, screen_height // 2))
        pygame.display.flip()
############################################################# NIvel de Unicornios
def CuartoNivel(colour, racha1, racha2):
    music_paused=False
    RainBG= pygame.image.load('assets/Rainbow.png')
    DosopcionesRB = pygame.image.load('assets/2RB.png')
    TresopcionesRB = pygame.image.load('assets/3RB.png')
    medallados = pygame.image.load('assets/Med2.png')
    medallauno = pygame.image.load('assets/Med1.png')
    BarraProg = pygame.image.load('assets/Prog4.png')
    jumpvfx = True
    racha3= True
    if colour == "Blue":
        Personaje = Azul_idle
        moveR = Azul_walking_right
        moveL = Azul_walking_Left
        Jump = Azul_jumping
    else:
        Personaje = Rosa_idle
        moveR = Rosa_walking_right
        moveL = Rosa_walking_Left
        Jump = Rosa_jumping
    counter = 0
    message=''
    jumping = False
    frame_rate= 3
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/Pixel_like.ttf", 24)
    screen_width, screen_height = SCREEN.get_size()
    last_update = pygame.time.get_ticks()
    frame =0
    running = True
    Preguntas= ["Tu cerebro guía tu comportamiento.",
                "Absolutamente todas tus conductas están en tu cerebro. Se reflejan en ",
                "patrones de activación ¿Crees que los patrones de activación de hombres ",
                "homosexuales se parecen a los de las mujeres, y viceversa?",
                'A) SI ',
                'B) NO',
                "Sí, pero esto no explica la homosexualidad. Enter para continuar",
                "jajaja, perdón te engañe otra vez",
                "Tenemos una vía cerebral que se activa cada vez que vemos a alguien que ",
                "nos gusta. ¿Qué crees que cambie en la activación de dicha vía en personas",
                "homosexuales?",
                "A)Su patrón de activación de ondas Beta",
                "B)La persona que activa dicha vía",
                "C)No existe dicha activación en personas homosexuales",
                "muy bien, eres como Kandel. Enter para continuar",
                "¿Crees que existe algo diferente en la forma del cerebro homosexual?",
                'A) SI ',
                'B) NO',
                'Muy bien, tqm. Enter para continuar ',
                "Felicidades, ya tienes la medalla de este nivel!",
                "Continua aprendiendo para ganar mas",
                "No obtuviste le medalla, continua al siguiente nivel"
                ]
    SCREEN.fill((255, 255, 255))  # Clear screen
    x= 300
    y= 250
    Y_gravity= 1
    Jump_height =14
    Y_velocity =Jump_height
    level = 1
    Correcto =0
    while True:
        SCREEN.fill((255, 255, 255))  # Clear screen
        timer.tick(60)
        SCREEN.blit(RainBG, (0,0))
        SCREEN.blit(BarraProg, (0, 0))
        if racha1 == True:
            SCREEN.blit(medallauno, (0, 0))
        if racha2 == True:
            SCREEN.blit(medallados, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # Exit the
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    level += 1
                    Correcto = 0
                    jumpvfx = True
                    if level >= 5:
                        QuintoNivel(colour, racha1, racha2,racha3)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jumping =True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mute_rect.collidepoint(event.pos):
                        # Toggle the boolean variable.
                        music_paused = not music_paused
                        if music_paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

        SCREEN.blit(mute, mute_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if x < 1100:
                x+= 10
                SCREEN.blit(moveR[frame], (x, y))
            else :SCREEN.blit(Personaje[frame], (x,y))
        elif keys[pygame.K_LEFT]:
            if x > 0:
                x-=10
                SCREEN.blit(moveL[frame], (x, y))
            else : SCREEN.blit(Personaje[frame], (x,y))
        #elif keys[pygame.K_UP]:
            #jumping = True
        else: SCREEN.blit(Personaje[frame], (x,y))
        Btn_Message.draw()
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(Rosa_idle): frame = 0
        # Display the message
        if level == 1:
            for i in range(6):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (22 * i)))
            SCREEN.blit(DosopcionesRB, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                speed = 3
                if counter < speed * len(Preguntas[6]):
                    counter += 1
                elif counter >= speed * len(Preguntas[6]):
                    done = True
                snip = font.render(Preguntas[6][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 ))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[7]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[7]):
                        done = True
                    snip = font.render(Preguntas[7][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 2:
            for i in range(8,14):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (22 * (i-8))))
            SCREEN.blit(TresopcionesRB, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                speed = 3
                if counter < speed * len(Preguntas[14]):
                    counter += 1
                elif counter >= speed * len(Preguntas[14]):
                    done = True
                snip = font.render(Preguntas[14][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + 25 ))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[7]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[7]):
                        done = True
                    snip = font.render(Preguntas[7][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 3:
            for i in range(15,18):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (22 * (i-15))))
            SCREEN.blit(DosopcionesRB, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                speed = 3
                if counter < speed * len(Preguntas[18]):
                    counter += 1
                elif counter >= speed * len(Preguntas[18]):
                    done = True
                snip = font.render(Preguntas[18][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 ))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[7]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[7]):
                        done = True
                    snip = font.render(Preguntas[7][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 4:
            if racha3 == True:
                medallatres = pygame.image.load('assets/Med3.png')
                SCREEN.blit(medallatres, (0,0))
                for i in range(19, 21):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 18))))
            else:
                SCREEN.blit(BG_Mensajes, (0, 520))
                speed = 3
                if counter < speed * len(Preguntas[20]):
                    counter += 1
                elif counter >= speed * len(Preguntas[20]):
                    done = True
                snip = font.render(Preguntas[20][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560))
        if jumping:
            y -= Y_velocity
            Y_velocity -= Y_gravity
            if x >= 100 and x<= 270 and level == 1:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if x >= 950 and x <= 1200 and level == 1:
                Correcto = 2
                racha3=False
            if x >= 75 and x <= 180 and level == 2:
                    Correcto = 2
                    racha3 = False
            if x >= 500 and x <= 790 and level == 2:
                    Correcto = 1
                    if jumpvfx:
                        JumpC.play()
                        jumpvfx = False
            if x >= 950 and x<= 1150 and level == 2:
                    Correcto = 2
                    racha3 = False
            if x >= 110 and x <= 220 and level == 3:
                    Correcto = 2
                    racha3 = False
            if x >= 950 and x <= 1200 and level == 3:
                    Correcto = 1
                    if jumpvfx:
                        JumpC.play()
                        jumpvfx = False
            if Y_velocity <- Jump_height:
                jumping= False
                Y_velocity = Jump_height
                SCREEN.blit(Jump[frame], (x,y))
        if message:
            font = pygame.font.Font("assets/Pixel_like.ttf", 24)
            text = font.render(message, True, (0, 0, 0))
            SCREEN.blit(text, (screen_width // 4, screen_height // 2))
        pygame.display.flip()
#####################################################################################################################
def QuintoNivel(colour, racha1,racha2,racha3):
    music_paused=False
    LoveBG= pygame.image.load('assets/LoveBG.png')
    TresopcionesLv = pygame.image.load('assets/LvLootBox.png')
    medallauno = pygame.image.load('assets/Med1.png')
    medallados = pygame.image.load('assets/Med2.png')
    medallatres = pygame.image.load('assets/Med3.png')
    BarraProg = pygame.image.load('assets/Prog5.png')
    jumpvfx = True
    racha4=True
    if colour == "Blue":
        Personaje = Azul_idle
        moveR = Azul_walking_right
        moveL = Azul_walking_Left
        Jump = Azul_jumping
    else:
        Personaje = Rosa_idle
        moveR = Rosa_walking_right
        moveL = Rosa_walking_Left
        Jump = Rosa_jumping
    counter = 0
    message=''
    jumping = False
    frame_rate= 3
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/Pixel_like.ttf", 24)
    screen_width, screen_height = SCREEN.get_size()
    last_update = pygame.time.get_ticks()
    frame =0
    running = True
    Preguntas= ["¿Consideras que la manera en la que expresas tu orientación sexual se",
                "aprende?",
                "A) Si",
                "B) No, viene en mis genes",
                "C) No",
                "Respuesta correcta, nadie nace sabiendo cómo realizar distintos ",
                "actos de ámbito sexual, por ejemplo cómo cortejar. Enter para continuar",
                "respuesta incorrectaaaaa",
                "¿Se nace o se hace la orientación sexual? ",
                "A) Se nace",
                "B) Se hace",
                "C) Es una combincacion",
                'La orientación sexual es una conducta compleja que está determinada por',
                'gran variedad de factores, muchos aquí expuestos, incluyendo al ',
                'aprendizaje, la combinación de todos ellos posibilida la muestra de algún',
                'tipo de orientación sexual. Enter para continuar',
                "No obtuviste le medalla, continua al siguiente nivel"
                ]
    SCREEN.fill((255, 255, 255))  # Clear screen
    x= 300
    y= 250
    Y_gravity= 1
    Jump_height =14
    Y_velocity =Jump_height
    level = 1
    Correcto =0
    while True:
        SCREEN.fill((255, 255, 255))  # Clear screen
        timer.tick(60)
        SCREEN.blit(LoveBG, (0,0))
        SCREEN.blit(BarraProg, (0, 0))
        if racha1 == True:
            SCREEN.blit(medallauno, (0, 0))
        if racha2 == True:
            SCREEN.blit(medallados, (0, 0))
        if racha3 ==True:
            SCREEN.blit(medallatres, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # Exit the
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    level += 1
                    Correcto = 0
                    jumpvfx = True
                    if level >= 3:
                        SextoNivel(colour,racha1,racha2,racha3,racha4)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jumping =True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mute_rect.collidepoint(event.pos):
                        # Toggle the boolean variable.
                        music_paused = not music_paused
                        if music_paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

        SCREEN.blit(mute, mute_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if x < 1100:
                x+= 10
                SCREEN.blit(moveR[frame], (x, y))
            else :SCREEN.blit(Personaje[frame], (x,y))
        elif keys[pygame.K_LEFT]:
            if x > 0:
                x-=10
                SCREEN.blit(moveL[frame], (x, y))
            else : SCREEN.blit(Personaje[frame], (x,y))
        #elif keys[pygame.K_UP]:
            #jumping = True
        else: SCREEN.blit(Personaje[frame], (x,y))
        Btn_Message.draw()
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(Rosa_idle): frame = 0
        # Display the message
        if level == 1:
            for i in range(5):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * i)))
            SCREEN.blit(TresopcionesLv, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(5, 7):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 5))))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[7]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[7]):
                        done = True
                    snip = font.render(Preguntas[7][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 2:
            for i in range(8,12):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * (i-8))))
            SCREEN.blit(TresopcionesLv, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(12,16):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 12))))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[7]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[7]):
                        done = True
                    snip = font.render(Preguntas[7][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 3:
            if racha4 == True:
                medallacuatro = pygame.image.load('assets/Med4.png')
                SCREEN.blit(medallacuatro, (0,0))
                for i in range(12, 16):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 18))))
            else:
                SCREEN.blit(BG_Mensajes, (0, 520))
                speed = 3
                if counter < speed * len(Preguntas[16]):
                    counter += 1
                elif counter >= speed * len(Preguntas[16]):
                    done = True
                snip = font.render(Preguntas[16][0:counter // speed], True, 'Black')

        if jumping:
            y -= Y_velocity
            Y_velocity -= Y_gravity
            if x >= 75 and x <= 180 and level == 1:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if x >= 500 and x <= 790 and level == 1:
                Correcto = 2
                racha4 = False
            if x >= 950 and x <= 1150 and level == 1:
                Correcto = 2
                racha4 = False
            if x >= 75 and x <= 180 and level == 2:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if x >= 500 and x <= 790 and level == 2:
                Correcto = 2
                racha4 = False
            if x >= 950 and x <= 1150 and level == 2:
                Correcto = 2
                racha4 = False
            if Y_velocity <- Jump_height:
                jumping= False
                Y_velocity = Jump_height
                SCREEN.blit(Jump[frame], (x,y))
        if message:
            font = pygame.font.Font("assets/Pixel_like.ttf", 24)
            text = font.render(message, True, (0, 0, 0))
            SCREEN.blit(text, (screen_width // 4, screen_height // 2))
        pygame.display.flip()
##########################################################
def SextoNivel(colour,racha1,racha2,racha3,racha4):
    music_paused = False
    LawBG= pygame.image.load('assets/LawBG.png')
    TresopcionesLaw = pygame.image.load('assets/LawLB.png')
    medallauno = pygame.image.load('assets/Med1.png')
    medallados = pygame.image.load('assets/Med2.png')
    medallatres = pygame.image.load('assets/Med3.png')
    medallacuatro = pygame.image.load('assets/Med4.png')
    BarraProg = pygame.image.load('assets/Prog6.png')
    if colour == "Blue":
        Personaje = Azul_idle
        moveR = Azul_walking_right
        moveL = Azul_walking_Left
        Jump = Azul_jumping
    else:
        Personaje = Rosa_idle
        moveR = Rosa_walking_right
        moveL = Rosa_walking_Left
        Jump = Rosa_jumping
    counter = 0
    message=''
    jumping = False
    frame_rate= 3
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/Pixel_like.ttf", 24)
    screen_width, screen_height = SCREEN.get_size()
    last_update = pygame.time.get_ticks()
    frame =0
    running = True
    Preguntas= ["¿Sabías que existen los derechos sexuales? ",
                "A) No",
                "B) Si",
                "C) Que es eso?",
                "Los derechos sexuales se refieren a la idea de que todas las personas",
                "tienen el derecho a la autonomía, integridad y libre expresión de su",
                "sexualidad, sin discriminación, coerción o violencia.Estos derechos están",
                "fundamentados en principios de igualdad, dignidad humana y libertad.",
                "La conceptualización de los derechos sexuales ha evolucionado con el tiempo",
                "y se ha incorporado en diversos documentos y declaraciones internacionales",
                "El siguiente es un derecho sexual",
                "A)Derecho a expresar mi sexualidad en las redes sociales",
                "B) Derecho a la identidad sexual",
                "C) El respeto al derecho ajeno es la paz",
                'El derecho a la identidad sexual incluye variedad',
                'de aspectos, entre ellos se destaca a la orientación sexual.',
                'Este avala que cada individuo es libre a tener una orientación ',
                'sexual y a vivir su vida de acuerdo con esa orientación sin sufrir',
                'discriminación, persecución o violencia.',
                'Don Benito',
                'nop',
                '¿La orientación sexual es una condición que debe de ser modificada?',
                "A)No, Yo respeto pero  que lo hagan en privado, anda de besos",
                "B)Sí, es una condición patológica que debe de involucrar intervención ",
                "psicológica, psiquiátrica y neurológica",
                "C) No, la orientación sexual es una conducta más que está determinada por",
                "muchos factores",
                "Es tu cuerpo, tu mente y tu vida, disfrutala y busca profesionales si tienes dudas",
                "Quierete <3"
                ]
    SCREEN.fill((255, 255, 255))  # Clear screen
    x= 300
    y= 250
    Y_gravity= 1
    Jump_height =14
    Y_velocity =Jump_height
    level = 1
    Correcto =0
    jumpvfx = True
    while True:
        SCREEN.fill((255, 255, 255))  # Clear screen
        timer.tick(60)
        SCREEN.blit(LawBG, (0,0))
        SCREEN.blit(BarraProg, (0, 0))
        if racha1 == True:
            SCREEN.blit(medallauno, (0, 0))
        if racha2 == True:
            SCREEN.blit(medallados, (0, 0))
        if racha3 ==True:
            SCREEN.blit(medallatres, (0, 0))
        if racha4 ==True:
            SCREEN.blit(medallacuatro, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # Exit the
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    level += 1
                    Correcto = 0
                    jumpvfx = True
                    if level >= 4:
                        main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jumping =True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mute_rect.collidepoint(event.pos):
                        # Toggle the boolean variable.
                        music_paused = not music_paused
                        if music_paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

        SCREEN.blit(mute, mute_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if x < 1100:
                x+= 10
                SCREEN.blit(moveR[frame], (x, y))
            else :SCREEN.blit(Personaje[frame], (x,y))
        elif keys[pygame.K_LEFT]:
            if x > 0:
                x-=10
                SCREEN.blit(moveL[frame], (x, y))
            else : SCREEN.blit(Personaje[frame], (x,y))
        #elif keys[pygame.K_UP]:
            #jumping = True
        else: SCREEN.blit(Personaje[frame], (x,y))
        Btn_Message.draw()
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(Rosa_idle): frame = 0
        # Display the message
        if level == 1:
            for i in range(4):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * i)))
            SCREEN.blit(TresopcionesLaw, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(4, 10):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (22 * (i - 4))))
        if level == 2:
            for i in range(10,14):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * (i-10))))
            SCREEN.blit(TresopcionesLaw, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(14,18):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 14))))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[20]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[20]):
                        done = True
                    snip = font.render(Preguntas[20][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
            if Correcto == 3:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[19]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[19]):
                        done = True
                    snip = font.render(Preguntas[19][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 3:
            for i in range(21,27):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (22 * (i-21))))
            SCREEN.blit(TresopcionesLaw, (0,0))
            if Correcto == 1:
                SCREEN.blit(BG_Mensajes, (0, 520))
                for i in range(27,29):
                    speed = 3
                    if counter < speed * len(Preguntas[i]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[i]):
                        done = True
                    snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 + (25 * (i - 27))))
            if Correcto == 2:
                    SCREEN.blit(BG_Mensajes, (0, 520))
                    speed = 3
                    if counter < speed * len(Preguntas[20]):
                        counter += 1
                    elif counter >= speed * len(Preguntas[20]):
                        done = True
                    snip = font.render(Preguntas[20][0:counter // speed], True, 'Black')
                    SCREEN.blit(snip, (38, 560 ))
                    Correcto = 0
        if level == 4:
            medallacuatro = pygame.image.load('assets/Medallas4.png')
            SCREEN.blit(medallacuatro, (0,0))
            for i in range(12, 16):
                speed = 3
                if counter < speed * len(Preguntas[i]):
                    counter += 1
                elif counter >= speed * len(Preguntas[i]):
                    done = True
                snip = font.render(Preguntas[i][0:counter // speed], True, 'Black')
                SCREEN.blit(snip, (38, 560 + (25 * (i - 12))))
        if jumping:
            y -= Y_velocity
            Y_velocity -= Y_gravity
            if x >= 75 and x <= 180 and level == 1:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if x >= 500 and x <= 790 and level == 1:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if x >= 950 and x <= 1150 and level == 1:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if x >= 75 and x <= 180 and level == 2:
                Correcto = 2
            if x >= 500 and x <= 790 and level == 2:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if x >= 950 and x <= 1150 and level == 2:
                Correcto = 3
            if x >= 75 and x <= 180 and level == 3:
                Correcto = 2
            if x >= 500 and x <= 790 and level == 3:
                Correcto = 2
            if x >= 950 and x <= 1150 and level == 3:
                Correcto = 1
                if jumpvfx:
                    JumpC.play()
                    jumpvfx = False
            if Y_velocity <- Jump_height:
                jumping= False
                Y_velocity = Jump_height
                SCREEN.blit(Jump[frame], (x,y))
        if message:
            font = pygame.font.Font("assets/Pixel_like.ttf", 24)
            text = font.render(message, True, (0, 0, 0))
            SCREEN.blit(text, (screen_width // 4, screen_height // 2))
        pygame.display.flip()
def play():
    music_paused=False
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mute_rect.collidepoint(event.pos):
                        # Toggle the boolean variable.
                        music_paused = not music_paused
                        if music_paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

        SCREEN.blit(mute, mute_rect)

        pygame.display.update()
    
def options():
    QR=pygame.image.load('assets/Resources.png')
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Escanea el codigo para conocer mas.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 60))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SCREEN.blit(QR, (340,100))
        OPTIONS_BACK = Button(image=None, pos=(1100, 600),
                            text_input="Regresar", font=get_font(40), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        #pygame.mixer.music.play(-1)  # The -1 means the music will loop indefinitely
        MENU_TEXT = get_font(40).render("Descubriendo la orientacion sexual", True, "#000000")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="JUGAR", font=get_font(75), base_color="#FFB2B2", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="INFO", font=get_font(75), base_color="#ffac2a", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        pos=pygame.mouse.get_pos()
        print(pos)
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #play()
                    FirstLevel()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()
