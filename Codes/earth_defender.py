#pgzero
import pgzrun
import random

#To-do
#-Balancear o sistema de spawn de asteroides(confia---)(pronto!1!!1)
#-Arrumar o sistema de bonus(pronto!!!)
#-Mini-reset depois da fase 5 + aumentar a dificuldade(pronto!!!)
#-Testar o jogo comigo e depois com a família(confia)

#Comando -> python Codes/earth_defender.py
FPS = 1
WIDTH = 500
HEIGHT = 300
TITLE = "Earth Defender"
# ---------------------------
# VARIÁVEIS GERAIS

mode = "menu"
level = 1
life = 3
pontos = 0
pontos_count = 0
movimento = 4

botao = 0
bonus = False
tempo = 0

tutorial_agendado = False

# ---------------------------
# ATORES
#mudar os nomes para diminutivos depois(pronto!!!)
asteroide_tut = Actor("asteroid", (250, -200))
background = Actor("back", (WIDTH / 2, HEIGHT / 2))
menu = Actor("menu", (WIDTH / 2, HEIGHT / 2))
planeta = Actor("planet", (WIDTH / 2, 275))

butaon = Actor("comecar", (250, 150))
butaon_rec = Actor("recomecar", (350, 250))
cursor_tutorial = Actor("tutorial", (-100, 100))
game_over = Actor("game_over", planeta.pos)

vida = None #Ator da vida(bonus)
ast = None #Ator do asteroide(inimigo)

# ---------------------------
# ASTEROIDES

asteroides = []

def new_asteroide():
    global ast
    if mode == "game":
        x = random.randint(50, 450)
        y = random.randint(-300, 0)
        ast = Actor("asteroid", (x, y))
        
        if level == 5:
            ast.vel = 0.025
        elif level < 5:
            ast.vel = (level / 2) * 0.04
        else:
            ast.vel = (level / 2) * 0.03
            
        asteroides.append(ast)

def movimento_ast():
    for ast in asteroides:
        dx = planeta.x - ast.x
        dy = planeta.y - ast.y
        ast.x += dx * ast.vel
        ast.y += dy * ast.vel

# ---------------------------
# BÔNUS

def criar_bonus():
    global vida
    x = random.randint(50, 450)
    y = random.randint(50, 225)
    vida = Actor("vida", (x, y))

# ---------------------------
# TUTORIAL

def tut():
    global botao
    animate(cursor_tutorial, tween="bounce_end", duration=1, pos=asteroide_tut.pos)
    botao = 1

# ---------------------------
# RESET

def reset():
    global botao, level, movimento, pontos, life, pontos_count
    
    global mode, asteroides, bonus, tempo, vida, tutorial_agendado

    life = 3
    pontos = 0
    pontos_count = 0
    asteroides = []
    level = 1
    movimento = 4
    botao = 0
    bonus = False
    tempo = 0
    vida = None
    tutorial_agendado = False

    mode = "tutorial"
    planeta.pos = (WIDTH / 2, 275)
    asteroide_tut.pos = (250, -200)
    cursor_tutorial.pos = (-100, 100)

# ---------------------------
# DRAW (APENAS DESENHO)

def draw():
    screen.clear()

    if mode == "menu":
        menu.draw()
        butaon.draw()

    elif mode == "tutorial":
        background.draw()
        planeta.draw()
        asteroide_tut.draw()
        cursor_tutorial.draw()

        if botao == 1:
            butaon.draw()

    elif mode == "game":
        background.draw()
        planeta.draw()

        screen.draw.text("Vidas: " + str(life), center=(50, 20), fontsize=20)
        screen.draw.text("Pontos: " + str(pontos), center=(250, 20), fontsize=20)
        screen.draw.text("Level: " + str(level), center=(450, 20), fontsize=20)

        for ast in asteroides:
            ast.draw()

        if bonus == True:
            vida.draw()
        
        if level >= 15:
            screen.draw.text("Nem ferrando", center=planeta.pos)
        
    elif mode == "game_over":
        background.draw()
        game_over.draw()
        screen.draw.text("Pontuação final: " + str(pontos), center=(250, 200))
        screen.draw.text("Fase: " + str(level), center=(250, 250))
        butaon_rec.draw()

# ---------------------------
# UPDATE

def update(dt):
    global pontos_count, level, movimento, tempo, bonus
    global mode, tutorial_agendado

    if mode == "tutorial" and not tutorial_agendado:
        animate(asteroide_tut, tween="decelerate", duration=1, pos=(WIDTH / 2, 100))
        clock.schedule(tut, 1)
        tutorial_agendado = True

    if mode == "game":
        movimento_ast()
        collisions()
        
        if pontos_count >= 5 and level == 1 or pontos_count >= 10 and level == 2:
            pontos_count = 0
            level += 1
        
        if pontos_count >= 15:  
            pontos_count = 0
            level += 1
            
        if level >= 5:
            if tempo >= 5 and not bonus:#(false)
                bonus = True
                criar_bonus()
            else:
                tempo += dt

    if level == movimento:
        if planeta.x >= 450:
            animate(planeta, duration=3, x=50)
        else:
            animate(planeta, duration=3, x=450)
        movimento += 2

    if life <= 0:
        mode = "game_over"
        animate(game_over, tween="decelerate", duration=1, pos=(WIDTH / 2, 100))

# ---------------------------
# COLISÕES

def collisions():
    global life
    for ast in asteroides[:]:
        if planeta.colliderect(ast):
            asteroides.remove(ast)
            life -= 1
            clock.schedule(new_asteroide, random.uniform(0.3, 0.5))

# ---------------------------
# INPUT

def on_mouse_down(button, pos):
    global mode, pontos, pontos_count, life, bonus, vida, tempo

    if mode == "menu" and butaon.collidepoint(pos):
        mode = "tutorial"

    elif mode == "tutorial" and butaon.collidepoint(pos):
        mode = "game"
        clock.schedule(new_asteroide, 0.5)

    elif mode == "game":
        for ast in asteroides[:]:
            if ast.collidepoint(pos):
                asteroides.remove(ast)
                pontos += 10
                pontos_count += 1
                clock.schedule(new_asteroide, random.uniform(0.3, 0.5))
                
        if vida:#(existe)
            if vida.collidepoint(pos):
                tempo = 0
                bonus = False 
                vida = None
                life += 1

    elif mode == "game_over" and butaon_rec.collidepoint(pos):
        reset()

pgzrun.go()
