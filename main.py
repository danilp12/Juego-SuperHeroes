#   Imports

import pygame,random,time,sys
from pygame.locals import *

#   Instanciar Modulo

pygame.init()
pygame.font.init()
pygame.mixer.init()


#   Variables Globales


ancho = 800
alto = 600
size = (ancho,alto)
negro = 0,0,0
blanco = 255,255,255
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()



def pausa():
    fuente = pygame.font.Font(None,65)
    texto = fuente.render("Juego en Pausa",0,(255,120,120),negro)
    texto2 = fuente.render(f"Presione Enter para Regresar",0,(255,120,120),negro)
    pausa = True
    pygame.mixer.music.pause()
    while pausa:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_RETURN: 
                    pausa = False
                    pygame.mixer.music.play()
                elif event.key == pygame.K_ESCAPE: 
                    menu()
            screen.blit(texto, (200,ancho/2-200))
            screen.blit(texto2, (100,ancho/2))
            pygame.display.update()
#   Variables del juego


disparado = False
cant_disparos = 6
dificultad = "Facil"
tiempo_enemigos = 250
recarga = pygame.sprite.Group()
explosion = pygame.sprite.Group()
health = pygame.sprite.Group()
enemies = pygame.sprite.Group()
disparos = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#   Sonidos

collision_sound = pygame.mixer.Sound("colision.mp3")
vida_sound = pygame.mixer.Sound("vida.mp3")
muerte_sound = pygame.mixer.Sound("game-over.mp3")
recargar_sound = pygame.mixer.Sound("recargar.mp3")
#   Temporizadores

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, tiempo_enemigos)
ADDHEALTH = pygame.USEREVENT + 2
pygame.time.set_timer(ADDHEALTH,2500)
CLEAN = pygame.USEREVENT +3
pygame.time.set_timer(CLEAN,150)
RECARGA = pygame.USEREVENT +4
pygame.time.set_timer(RECARGA,6500)
def temporizadores():
    tiempo_dificultad = time.time()
    tiempo_inicio = time.time()
    tiempo_tempo = tiempo_inicio
    return tiempo_dificultad,tiempo_inicio,tiempo_tempo
def seleccionskin(skin):
    if skin == "Spiderman":
        Skins = ["spider.gif","spider_mov_der.gif","spider_mov_izq.gif","red.gif"]
        return Skins
    elif skin == "Hulk":
        Skins = ["skinhulk.gif","hulk_mov_izq.gif","hulk_mov_der.gif","roca.gif"]
        return Skins
    elif skin == "Capitan":
        Skins= ["capitan.gif","capitan_mov_izq.gif","capitan_mov_der.gif","escudo.gif"]
        return Skins
def iniciar_partida(skin):
    #   Objetos
    Skin = seleccionskin(skin)
    pygame.mixer.music.load("musica.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.2)
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load(Skin[0]).convert()
            self.rect = self.surf.get_rect()
            self.rect.topleft = (ancho/2-self.rect.width,0)
            self.health = 100
            self.score = 0
        def update(self, pressed_keys):
            if pressed_keys[pygame.K_LEFT]:
                self.surf = pygame.image.load(Skin[2]).convert()
                self.rect.move_ip(-8, 0)
            elif pressed_keys[pygame.K_RIGHT]:
                self.surf = pygame.image.load(Skin[1]).convert()
                self.rect.move_ip(8, 0)
            else:
                self.surf = pygame.image.load(Skin[0]).convert()
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > 800:
                self.rect.right = 800
            if player.health < 0:
                global run
                muerte_sound.play()
                finalizar(player)
                player.kill()
                run = False
                return run
            
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pygame.image.load("enemigo.gif").convert()
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(0, 800),
                    random.randint(600+20, 600+100),
                )
            )
            if dificultad == "Facil":
                self.speed = random.randint(5, 8)
            elif dificultad == "Medio":
                self.speed = random.randint(8,13)
            elif dificultad == "Dificil":
                self.speed = random.randint(13,18)
            elif dificultad == "Extremo":
                self.speed = random.randint(20,25)
        def update(self):
            global Score
            self.rect.move_ip(0,-self.speed)
            if self.rect.top < 0:
                self.kill()
            if pygame.sprite.spritecollideany(player,enemies):
                player.health -= 25
                player.score -= 10
                self.kill()
            if pygame.sprite.groupcollide(disparos,enemies,False,True):
                new_explosion = Explosion(self.rect.centerx,self.rect.centery)
                explosion.add(new_explosion)
                all_sprites.add(new_explosion)
                collision_sound.play()
                player.score +=20
                enemies.remove()
                
        def setSpeed(self,velocidad):
            self.speed = velocidad
            return True
    class Health(pygame.sprite.Sprite):
        def __init__(self):
            super(Health, self).__init__()
            self.surf = pygame.image.load("vida.gif").convert()
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(0, 800),
                    random.randint(600+20, 600+100),
                )
            )
            self.speed = random.randint(5, 8)

        def update(self):
            self.rect.move_ip(0,-self.speed)
            if self.rect.top < 0:
                self.kill()
            if pygame.sprite.spritecollideany(player,health):
                global Score
                if player.health < 100:
                    player.health += 25
                    vida_sound.play()
                    player.score += 15
                    self.kill()
    class Recarga(pygame.sprite.Sprite):
        def __init__(self):
            super(Recarga, self).__init__()
            self.surf = pygame.image.load("balas.gif").convert()
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(0, 800),
                    random.randint(600+20, 600+100),
                )
            )
            self.speed = random.randint(5, 8)

        def update(self):
            self.rect.move_ip(0,-self.speed)
            if self.rect.top < 0:
                self.kill()
            if pygame.sprite.spritecollideany(player,recarga):
                    global cant_disparos
                    recargar_sound.play()
                    cant_disparos += 5
                    self.kill()
    class Disparo(pygame.sprite.Sprite):
        def __init__(self):
            super(Disparo, self).__init__()
            self.surf = pygame.image.load(Skin[3]).convert()
            self.rect = self.surf.get_rect(
                center = (player.rect.centerx,player.rect.centery)
            )
            self.speed = 10
            self.disparo = True

        def update(self):
            global disparado
            self.rect.move_ip(0,self.speed)
            if alto < self.rect.bottom:
                self.kill()
                disparado = False
                return disparado
    class Explosion(pygame.sprite.Sprite):
        def __init__(self,x,y):
            super(Explosion, self).__init__()
            self.surf = pygame.image.load("explosion.gif").convert()
            self.rect = self.surf.get_rect(
                center = (x,y)
            )

        def update(self):
            explosion.remove()
            self.kill()
    run = True
    player = Player()
    all_sprites.add(player)
    tiempo_dificultad,tiempo_inicio,tiempo_tempo = temporizadores()

    #   Funciones

    def score():
        fuente = pygame.font.Font(None,35)
        texto = fuente.render("SCORE:"+str(player.score),0,(0,255,0),negro)
        return texto
    def finalizar (player):
        fuente = pygame.font.Font(None,65)
        texto = fuente.render("Game Over - 'ESC' o 'Enter' para salir",0,(255,120,120),negro)
        texto2 = fuente.render(f"Tu Puntuacion: {player.score}",0,(255,120,120),negro)
        pausa = True
        pygame.mixer.music.stop()
        while pausa:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE: 
                        pausa = False
                        limpiar(player)
                        menu()

                screen.blit(texto, (5,ancho/2-100))
                screen.blit(texto2, (200,ancho/2))
                pygame.display.update()
    def limpiar(player):
        global fase, disparado,cant_disparos,dificultad
        del(player)
        all_sprites.empty()
        enemies.empty()
        health.empty()
        recarga.empty()
        disparos.empty()
        explosion.empty()
        fase = 1
        disparado = False
        cant_disparos = 6
        dificultad = "Facil"
    def vida():
        fuente = pygame.font.Font(None,35)
        texto = fuente.render("VIDA:"+str(player.health if player.health != 0 else "1")+"%",0,(0,255,0),negro)
        return texto
    def cantbalas():
        global cant_disparos
        fuente = pygame.font.Font(None,35)
        if cant_disparos < 4:
            texto = fuente.render("Disparos Disponibles:"+str(cant_disparos),0,(255,0,0),negro)
        else:
            texto = fuente.render("Disparos Disponibles:"+str(cant_disparos),0,(0,255,0),negro)
        return texto
    def setdifitultad():
        global dificultad
        
        fuente = pygame.font.Font(None,35)
        if dificultad == "Extremo":
            texto = fuente.render("Dificultad:"+str(dificultad),0,(255,0,0),negro)
        else:
            texto = fuente.render("Dificultad:"+str(dificultad),0,(0,255,0),negro)
        return texto
    def cambiardificultad(dif,tiempo):
        global cant_disparos, tiempo_enemigos,dificultad
        if dif == "Extrema":
            tiempo_enemigos = 150
            return dificultad, tiempo_enemigos
        elif dif == "Dificil" and 45.00 <= tiempo: 
            dificultad = "Extremo"
            tiempo_enemigos = 200
            return dificultad, tiempo_enemigos
        elif dif == "Medio" and 30.00 <= tiempo:
            dificultad = "Dificil"
            tiempo_enemigos = 230
            return dificultad, tiempo_enemigos
        elif dif == "Facil" and 15.00 <= tiempo:
            dificultad = "Medio"
            return dificultad, tiempo_enemigos
    def tiempo(tiempo_dificultad,tiempo_inicio,tiempo_tempo):
        global Score,dificultad
        
        fuente = pygame.font.Font(None,20)
        tempo_dificultad = time.time()-tiempo_dificultad
        tempo = time.time()-tiempo_tempo
        tiempo = time.time()-tiempo_inicio
        texto = fuente.render("TIEMPO:"+str(tiempo)[0:5]+" Seg",0,(0,255,0),negro)
        if 5.00 <= tempo :
            tempo = 0 
            tiempo_tempo = time.time()
            player.score +=50
        if 10.00 <= tempo_dificultad:
            tempo_dificultad = 0
            tiempo_dificultad = time.time()
            cambiardificultad(dificultad,tiempo)
            
                

        return texto, tiempo_tempo
    
    #   loop del juego
    while run:
        global disparado,cant_disparos,dificultad,tiempo_enemigos
        
        fondo = pygame.image.load("fondo.png").convert()
        screen.blit(fondo,(0,0))

    #       Handler de eventos del juego

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finalizar(player)
                    run = False
                elif event.key == pygame.K_SPACE:
                    disparo = Disparo()
                    if disparado == False:
                        if cant_disparos != 0:
                            disparos.add(disparo)
                            all_sprites.add(disparo)
                            disparado = True
                            cant_disparos -=1
                elif event.key == pygame.K_p:
                    pausa()
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == ADDHEALTH:
                new_health = Health()
                health.add(new_health)
                all_sprites.add(new_health)
            elif event.type == CLEAN:
                explosion.update()
            elif event.type == RECARGA:
                new_recarga = Recarga()
                recarga.add(new_recarga)
                all_sprites.add(new_recarga)
            
        cronometro,tiempo_tempo = tiempo(tiempo_dificultad,tiempo_inicio,tiempo_tempo)
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        screen.blit(vida(),(0,550))
        screen.blit(cronometro,(0,580))
        screen.blit(score(),(140,550))
        screen.blit(cantbalas(),(140,580))
        screen.blit(setdifitultad(),(500,580))
        enemies.update()
        health.update()
        disparos.update()
        recarga.update()
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        pygame.display.update()
        clock.tick(30)
def salir():
    fuente = pygame.font.Font(None,65)
    texto = fuente.render("Seguro que desea salir?",0,(255,120,120),negro)
    texto2 = fuente.render(f"S/N",0,(255,120,120),negro)
    pausa = True
    while pausa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_n: 
                    pausa = False
                elif event.key == pygame.K_s: 
                    pygame.quit()
                    quit()
            screen.blit(texto, (160,ancho/2-100))
            screen.blit(texto2, (360,ancho/2))
            pygame.display.update()
def menu():
    pygame.mixer.music.load("main.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.2)
    menuprincipal = True
    while menuprincipal:
        fondo = pygame.image.load("fondoprincipal.png").convert()
        screen.blit(fondo,(0,0))
        mx,my = pygame.mouse.get_pos()
        fuente = pygame.font.Font(None,50)
        texto1 = fuente.render("Iniciar Partida",0,(0,255,0),negro)
        obj1 = texto1.get_rect()
        texto2 = fuente.render("Salir",0,(0,255,0),negro)
        obj2 = texto2.get_rect()
        start = pygame.Rect(100,100,obj1.width,obj1.height)
        boton2 = pygame.Rect(100,200,obj2.width,obj2.height)
        
        
        screen.blit(texto1,start)
        screen.blit(texto2,boton2)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    salir()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if start.collidepoint((mx,my)):
            if click:
                
                seleccion()
                menuprincipal = False
        if boton2.collidepoint((mx,my)):
            if click:
                salir()
        pygame.display.update()
        clock.tick(30)
    pygame.mixer.quit()
    pygame.quit()
def seleccion():
    seleccion = True
    while seleccion:
        
        fondo = pygame.image.load("fondoprincipal.png").convert()
        screen.blit(fondo,(0,0))
        mx,my = pygame.mouse.get_pos()
        fuente = pygame.font.Font(None,50)
        titulo = fuente.render("Selecciona Tu Personaje",0,(0,255,0),negro)
        tit = titulo.get_rect()
        personaje1 = pygame.image.load("spider.png")
        obj1 = personaje1.get_rect()
        personaje2 = pygame.image.load("hulk.png")
        obj2 = personaje2.get_rect()
        personaje3 = pygame.image.load("capitan.png")
        obj3 = personaje3.get_rect()
        texto = fuente.render("Atras",0,(0,255,0),negro)
        objtext = texto.get_rect()
        controles1 = fuente.render("Controles: Movimientos flecha der-izq ",0,(0,255,0),negro)
        controles2 = fuente.render("Disparo: Tecla Espacio",0,(0,255,0),negro)
        objt4 = controles1.get_rect()
        objt5 = controles2.get_rect()
        Titulo = pygame.Rect(200,10,tit.width,tit.height)
        boton1 = pygame.Rect(10,100,obj1.width,obj1.height)
        boton2 = pygame.Rect(240,100,obj2.width,obj2.height)
        boton3 = pygame.Rect(480,100,obj3.width,obj3.height)
        salir = pygame.Rect(40,550,objtext.width,objtext.height)
        cntrl1 = pygame.Rect(10,400,objt4.width,objt4.height)
        cntrl2 = pygame.Rect(10,460,objt5.width,objt5.height)
        
        screen.blit(titulo,Titulo)
        screen.blit(personaje1,boton1)
        screen.blit(personaje2,boton2)
        screen.blit(personaje3,boton3)
        screen.blit(texto,salir)
        screen.blit(controles1,cntrl1)
        screen.blit(controles2,cntrl2)
        personaje = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    seleccion = False
                    menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    personaje = True
        if boton1.collidepoint((mx,my)):
            if personaje:
                skin = "Spiderman"
                pygame.mixer.stop()
                iniciar_partida(skin)
                seleccion = False
        if boton2.collidepoint((mx,my)):
            if personaje:
                skin = "Hulk"
                pygame.mixer.stop()
                iniciar_partida(skin)
                seleccion = False
        if boton3.collidepoint((mx,my)):
            if personaje:
                skin = "Capitan"
                pygame.mixer.stop()
                iniciar_partida(skin)
                seleccion = False
        if salir.collidepoint((mx,my)):
            if personaje:
                seleccion = False
                menu()
        pygame.display.update()
        clock.tick(30)
menu()




