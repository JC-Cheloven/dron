# -*- coding: utf-8 -*-
#
#  dron.py
#  
#  Copyright 2021 
#  Author: Juan Carlos del Caño
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 3 as 
#  published by the Free Software Foundation. 
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  Or you can check the online version of the license at 
#  https://www.gnu.org/licenses/licenses.html
#  


import pygame
import os
import numpy as np

class Tieso (pygame.sprite.Sprite):
    '''Clase base para duendes que no cambian de orientación, como el dron y
    las bases móviles. Tambien lo uso con velocidad nula para las bases fijas.
    '''
    def __init__(self, image, pos, vel):
        pygame.sprite.Sprite.__init__(self) 
        self.image=image
        self.pos=np.array(pos)
        self.vel=np.array(vel)
        self.rect=self.image.get_rect()
        self.rect.center= self.pos
        self.vida= 0
        self.hecho= False
        self.cuentatras= -1

    def borra(self, display, fondo):
        display.blit(fondo, self.rect, self.rect)

    def traza(self, display):
        display.blit(self.image, self.rect)

    def update(self, destino, fondo):
        destino.blit(fondo, self.rect, self.rect)
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect.center= self.pos
        if self.hecho: # seria mejor controlar alpha desde fuera, solo cuando cambie...**
            self.image.set_alpha(80) # 120? pero parece trazarse 2 veces
        else:
            self.image.set_alpha(255)
        destino.blit(self.image, self.rect)
        self.vida +=1 
        self.cuentatras -= 1
        if self.cuentatras== -5555: self.cuentatras=-1

class Misil(pygame.sprite.Sprite):
    '''Clase para duendes que cambian de orientacion, normalmente con 
    pygame.transform.rotate (misiles en este caso). La image_tiesa inicial
    debe apuntar hacia la derecha.
    '''
    def __init__(self,image_tiesa, pos, vel):
        pygame.sprite.Sprite.__init__(self) 
        self.image_tiesa= image_tiesa
        self.pos=np.array(pos)
        self.vel=np.array(vel)
        self.vida=0
        self.vidamax=np.random.default_rng().integers(300,400) # igual en misil & bala, ok
        self.rect=self.image_tiesa.get_rect()
        self.image=self.image_tiesa

    def traza(self, display):
        display.blit(self.image, self.rect)

    def borra(self, display, fondo):
        display.blit(fondo, self.rect, self.rect)
    
    def update(self, destino, fondo):
        destino.blit(fondo, self.rect, self.rect) # borrar
        self.teta=-np.arctan2(self.vel[1],self.vel[0])*180/np.pi # rotar y mover
        self.image= pygame.transform.rotate(self.image_tiesa, self.teta)
        self.rect= self.image.get_rect()
        self.rect[0], self.rect[1]= self.pos[0], self.pos[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        destino.blit(self.image, self.rect) # trazar el nuevo
        self.vida +=1


def do_crash(*args):
    global acaba
    dron.borra(v0,fondo_img)
    if args : args[0].borra(v0, fondo_img)
    
    a= crash_img1.get_rect()
    a.center=dron.rect.center
    v0.blit(crash_img1, a)
    pygame.display.flip()
    
    pygame.mixer.music.fadeout(200)
    crash_sound.play()
    pygame.time.wait(1000)
    
    a= crash_img2.get_rect()
    a.center=dron.rect.center
    v0.blit(crash_img2, a)
    pygame.display.flip()
    pygame.time.wait(2500)
    
    a= byebye_img.get_rect()
    a.center= 0.8*np.array(dron.rect.center) + 0.1*np.array([aa,bb])
    v0.blit(byebye_img, a)
    pygame.display.flip()
    pygame.time.wait(1500)
    
    for i in range(60):
        v0.fill((4,3,3), special_flags=pygame.BLEND_RGB_ADD)
        pygame.display.flip()
        pygame.time.wait(20)
    pygame.time.wait(400)
    
    

def pausar():
    pygame.display.iconify()
    while True:
        pygame.event.clear()
        pygame.time.wait(200)
        for tocau in pygame.event.get():
            if tocau.type == pygame.QUIT:
                pygame.quit()
                
            if tocau.type == pygame.KEYDOWN:
                return()


pygame.init()
la_pantalla= pygame.display.Info() 
pantalla_w, pantalla_h= 0.9*la_pantalla.current_w, 0.9*la_pantalla.current_h

aa,bb=1200,900 # este es el tamaño nominal. 
if aa<=pantalla_w and bb<=pantalla_h:
    escalar_cosas=False
else:
    escalar_cosas=True
    scal= min(pantalla_w/aa, pantalla_h/bb) # factores <1 (al menos uno)
    aa,bb = int(scal*aa), int(scal*bb)


v0=pygame.display.set_mode((aa,bb))
pygame.display.set_caption('dron by JC')


# cargamos font, imagenes y sonidos

cwd= dir_path = os.path.dirname(os.path.realpath(__file__))
#print('directorio que entiende: ', cwd)

kk= pygame.image.load(os.path.join(cwd, 'fondo_terrain1.png')).convert()
fondo_img=pygame.transform.scale(kk, (aa,bb))
fondo_img2= fondo_img.copy() # para re-borrar bases
rect_fondo= fondo_img.get_rect()

if escalar_cosas: # me tomo esta molestia porque rotozoom emborrona aunq sea scal=1.

    kk = pygame.image.load(os.path.join(cwd,'dron.png')).convert()
    dron_img= pygame.transform.rotozoom(kk,0,scal)
    dron_img.set_colorkey((255,255,255))

    kk = pygame.image.load(os.path.join(cwd,'dron_mediogas.png')).convert()
    dron_mediogas = pygame.transform.rotozoom(kk,0,scal)
    dron_mediogas.set_colorkey((255,255,255))

    kk = pygame.image.load(os.path.join(cwd,'dron_singas.png')).convert()
    dron_singas = pygame.transform.rotozoom(kk,0,scal)
    dron_singas.set_colorkey((255,255,255))

    kk = pygame.image.load(os.path.join(cwd,'dron_negro.png')).convert()
    dron_negro = pygame.transform.rotozoom(kk,0,scal)
    dron_negro.set_colorkey((255,255,255))

    kk= pygame.image.load(os.path.join(cwd,'basefija.png')).convert()
    castle_img= pygame.transform.rotozoom(kk,0,scal)
    castle_img.set_colorkey((255,255,255))

    kk= pygame.image.load(os.path.join(cwd,'basefija_roja.png')).convert()
    castlerojo_img= pygame.transform.rotozoom(kk,0,scal)
    castlerojo_img.set_colorkey((255,255,255))

    kk= pygame.image.load(os.path.join(cwd,'misil.png')).convert()
    misil_img_tiesa= pygame.transform.rotozoom(kk,0,scal)
    misil_img_tiesa.set_colorkey((255,255,255))

    kk= pygame.image.load(os.path.join(cwd,'bala.png')).convert()
    bala_img_tiesa= pygame.transform.rotozoom(kk,0,scal)
    bala_img_tiesa.set_colorkey((255,255,255))

    kk= pygame.image.load(os.path.join(cwd,'nube_roja1.png')).convert()
    crash_img1= pygame.transform.rotozoom(kk,0,scal)
    crash_img1.set_colorkey((255,255,255))

    kk= pygame.image.load(os.path.join(cwd,'nube_roja2.png')).convert()
    crash_img2= pygame.transform.rotozoom(kk,0,scal)
    crash_img2.set_colorkey((255,255,255))

    kk= pygame.image.load(os.path.join(cwd,'gate.png')).convert()
    gate_img= pygame.transform.rotozoom(kk,0,scal)
    gate_img.set_colorkey((255,255,255))

    kk= pygame.image.load(os.path.join(cwd,'basemovil.png')).convert()
    panzer_img= pygame.transform.rotozoom(kk,0,scal)
    panzer_img.set_colorkey((255,255,255))

    kk= pygame.image.load(os.path.join(cwd,'basemovil_roja.png')).convert()
    panzerojo_img= pygame.transform.rotozoom(kk,0,scal)
    panzerojo_img.set_colorkey((255,255,255))
    
    kk= pygame.image.load(os.path.join(cwd,'dronfinal.png')).convert()
    dronfinal= pygame.transform.rotozoom(kk,0,scal)
    dronfinal.set_colorkey((255,255,255))
    
    kk= pygame.image.load(os.path.join(cwd,'byebye.png')).convert()
    byebye_img= pygame.transform.rotozoom(kk,0,scal)
    byebye_img.set_colorkey((255,255,255))
    
else:
    dron_img = pygame.image.load(os.path.join(cwd,'dron.png')).convert()
    dron_img.set_colorkey((255,255,255))

    dron_mediogas = pygame.image.load(os.path.join(cwd,'dron_mediogas.png')).convert()
    dron_mediogas.set_colorkey((255,255,255))

    dron_singas = pygame.image.load(os.path.join(cwd,'dron_singas.png')).convert()
    dron_singas.set_colorkey((255,255,255))

    dron_negro = pygame.image.load(os.path.join(cwd,'dron_negro.png')).convert()
    dron_negro.set_colorkey((255,255,255))

    castle_img= pygame.image.load(os.path.join(cwd,'basefija.png')).convert()
    castle_img.set_colorkey((255,255,255))

    castlerojo_img= pygame.image.load(os.path.join(cwd,'basefija_roja.png')).convert()
    castlerojo_img.set_colorkey((255,255,255))

    misil_img_tiesa= pygame.image.load(os.path.join(cwd,'misil.png')).convert()
    misil_img_tiesa.set_colorkey((255,255,255))

    bala_img_tiesa= pygame.image.load(os.path.join(cwd,'bala.png')).convert()
    bala_img_tiesa.set_colorkey((255,255,255))

    crash_img1= pygame.image.load(os.path.join(cwd,'nube_roja1.png')).convert()
    crash_img1.set_colorkey((255,255,255))

    crash_img2= pygame.image.load(os.path.join(cwd,'nube_roja2.png')).convert()
    crash_img2.set_colorkey((255,255,255))

    gate_img= pygame.image.load(os.path.join(cwd,'gate.png')).convert()
    gate_img.set_colorkey((255,255,255))

    panzer_img= pygame.image.load(os.path.join(cwd,'basemovil.png')).convert()
    panzer_img.set_colorkey((255,255,255))

    panzerojo_img= pygame.image.load(os.path.join(cwd,'basemovil_roja.png')).convert()
    panzerojo_img.set_colorkey((255,255,255))
    
    dronfinal= pygame.image.load(os.path.join(cwd,'dronfinal.png')).convert()
    dronfinal.set_colorkey((255,255,255))
    
    byebye_img= pygame.image.load(os.path.join(cwd,'byebye.png')).convert()
    byebye_img.set_colorkey((255,255,255))


# (la musica se pone luego dependiendo del nivel)

crash_sound= pygame.mixer.Sound(os.path.join(cwd,'explosion-01.ogg'))
caerse_sound= pygame.mixer.Sound(os.path.join(cwd,'fiuuu.ogg'))

dron_arranca= pygame.mixer.Sound(os.path.join(cwd,'dron_arranca2.ogg'))
dron_para= pygame.mixer.Sound(os.path.join(cwd,'dron_para2.ogg'))

click_camara= pygame.mixer.Sound(os.path.join(cwd,'click_camara.oga'))
nivel_completo= pygame.mixer.Sound(os.path.join(cwd,'nivel_completo.ogg'))
aparece_gate= pygame.mixer.Sound(os.path.join(cwd,'aparece_gate.oga'))

# creamos un generador de secuencias de enteros aleatorios. Se usa asi:
# mi_random(0,5,27) -> 27 nums aleatorios entre 0 y 4. Sin el 27 genera un solo numero.
mi_random=np.random.default_rng().integers
# y un clock para usar clock.tick(framerate):
clock=pygame.time.Clock() 


# pantalla de presentacion


texto= '''
                                        **********
                                        ** DRON **
                                        **********
                                    
                        El programilla para matar el rato by JC

Tu dron está en campo enemigo con la misión de fotografíar sus bases y sus panzers móviles. Para 
sacar una foto a una base el dron debe estar al menos un instante completamente encima con poca 
velocidad. Cuando eso ocurre la foto se dispara (se oye un click) y la base se oscurece. Para 
fotografiar un panzer el dron puede pasar por encima con cualquier velocidad.

Una vez fotografíadas todas las bases y panzers, aparece la plataforma de rescate. El dron debe 
aterrizar en ella con una velocidad pequeña que debe ser puramente horizontal.

El dron tiene una cierta autonomía (creciente con el nivel). El dron se torna amarillo y luego 
marrón según se agota la autonomía.

Las bases dispararán misiles de cabeza buscadora y los panzers dispararán balas al dron. Un 
momento antes de disparar el elemento correspondiente se vuelve rojo.

Si necesitas pausar el juego pulsa la barra espaciadora. Los sonidos se detienen y la ventana se 
minimiza (por si viene tu jefe). Para continuar restaura la ventana y pulsa una tecla. Para  dejar 
de jugar simplemente cierra la ventana.

El dron se controla con las cuatro flechas del teclado. Para un control más fino de la velocidad 
es aconsejable dar toques de tecla en lugar de mantenerla pulsada. Si en tu monitor no cabe una
ventana de 1200x900 (la resolución nativa del juego), el juego se escalará a un tamaño posible,
aunque el tacto del control no será el previsto.

El juego Dron es software libre bajo licencia GPL v3. Consulta la cabecera del código.

Para que parecza que hay opciones, dime tu nivel de kun-fu:
      0= soy normal, me mancho con la sopa;   1= miro el móvil sin chocarme con con las farolas; 
      2= comprendo la santísima trinidad;      3= leo el pensamiento y puedo dividir por cero.

                                >> Pulsa 0-3 para comenzar <<
'''

v0.blit(fondo_img2, (0,0))
v0.blit(dronfinal, (0.5*aa,0.05*bb))
v0.fill((120,120,120), special_flags=pygame.BLEND_RGB_ADD)

font_jc =  pygame.font.SysFont('Chilanka', 14, bold=True)
lineas = texto.splitlines()
for i, l in enumerate(lineas):
    v0.blit(font_jc.render(l, True, (10,10,10)), (0.05*aa, 0.03*bb+14*i))

mirando=True
while mirando:
    pygame.display.flip()
    pygame.event.clear()
    pygame.time.wait(300)
    kung_fu=7
    for tocau in pygame.event.get():
        if tocau.type == pygame.QUIT: 
            pygame.quit()
            
        elif tocau.type == pygame.KEYDOWN:
            ch= tocau.key
            if   ch in (pygame.K_0 , pygame.K_KP0) : kung_fu=0
            elif ch in (pygame.K_1 , pygame.K_KP1) : kung_fu=1
            elif ch in (pygame.K_2 , pygame.K_KP2) : kung_fu=2
            elif ch in (pygame.K_3 , pygame.K_KP3) : kung_fu=3
            else: pygame.event.pump()

        if kung_fu < 4:
            print('kung-fu elegido = ', kung_fu)
            mirando=False
            break


font_jc = pygame.font.SysFont("serif", 42) # para rotulos del juego

for nivel in range(5):
    
    # musica maestro!
    if nivel in (0,1):
        pygame.mixer.music.load(os.path.join(cwd,'dron_vuela3.ogg'))
    elif nivel in (2,3):
        pygame.mixer.music.load(os.path.join(cwd,'StochGrains_cecilia.ogg'))
    else:
        pygame.mixer.music.load(os.path.join(cwd,'fantasmal_pa_dron.ogg'))
    pygame.mixer.music.play(loops=-1)#, fade_ms=600)
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.pause()
    
    # definimos Sprites() y agrupamos los castillos & panzers
    dron= Tieso(image=dron_img, pos=(aa-22,bb/2), vel=(0,0))
    castles = []
    for i in range(2):
        for j in range(2):
            rx,ry = mi_random(25, aa/2-25), mi_random(25, bb/2-25)
            rx=aa*i/2 + rx
            ry=bb*j/2 + ry
            castle=Tieso(image=castle_img.copy(), pos=(rx,ry), vel=(0,0))
            castles.append(castle)
    castles_group= pygame.sprite.Group(castles)
    misiles_group= pygame.sprite.Group()

    panzers=[]
    for ipanzer in range(nivel): # el nivel 0 sin panzers
        p = np.array([mi_random(30,aa-30), mi_random(25,bb-25)])
        v= np.array([mi_random(-2,3), mi_random(-2,3)])
        panzer=Tieso(image=panzer_img.copy(), pos=p, vel=v)
        panzers.append(panzer)
    panzers_group=pygame.sprite.Group(panzers)
    balas_group= pygame.sprite.Group()

    # trazado inicial (el fondo se oscurece con el nivel)
    a= 18*nivel
    fondo_img2.fill((a,a,a), special_flags=pygame.BLEND_RGB_SUB)
    fondo_img=fondo_img2.copy()
    v0.blit(fondo_img, (0,0))
    
    gate_rect=gate_img.get_rect()
    gate_rect.midright= (aa, bb/2)
    v0.blit(gate_img,gate_rect)
    
    dron.traza(v0)
    castles_group.update(v0, fondo_img2)
    panzers_group.update(v0, fondo_img)
    
    texto= f'Nivel {nivel}'
    cuadrotexto= font_jc.render(texto, True, (255,165,0) )
    su_rect= cuadrotexto.get_rect().move(aa/3,bb/4)
    v0.blit(cuadrotexto, su_rect)
    pygame.display.flip()
    dron_arranca.play()
    pygame.time.wait(3000)
    
    v0.blit(fondo_img, gate_rect, gate_rect)
    v0.blit(fondo_img, su_rect, su_rect )
    castles_group.update(v0, fondo_img2)
    dron.traza(v0)
    
    pygame.display.flip()

    # fondo limpio
    fondo_img=fondo_img2.copy()
    pygame.time.wait(1000)
    
    # retomamos la musica
    pygame.mixer.music.unpause()
    
    jcount, acaba, gatepuesto = 1, False, False
    castles_hechos, panzers_hechos = 0,0

    while not acaba:
        
        # Update castles, osea redibujarlos pq tienen vel=0. Lo hago antes del delay pq 
        # asi el dron se ve sobre los castles.
        # Sobre fondo_img (no sobre v0) pa ver la transparencia del dron sobre el castle.
        # Con el apaño ss evito un blit completo v0.blit(fondo_img, (0,0)) por ciclo. Es 
        # como hacerlo con dirty_rects pero mejor, usando la flexibilidad del update()
        # que he construido
        
        castles_group.update(fondo_img, fondo_img2) 
        castles_group.update(v0,fondo_img)

        pygame.time.wait(60)
        #clock.tick(16) # los ciclos no superarán esa framerate

        eventos= pygame.event.get() # para quit si, evento
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                

        '''
        # usar eventos SDL de teclado hace que el control del juego sea pesado:
        eventos= pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key== pygame.K_LEFT: 
                    dron.vel[0] -= 1
                elif event.key== pygame.K_RIGHT: 
                    dron.vel[0] += 1
                elif event.key== pygame.K_UP: 
                    dron.vel[1] -= 1
                elif event.key== pygame.K_DOWN: 
                    dron.vel[1] += 1
                elif event.key== pygame.K_SPACE:
                    pygame.mixer.music.pause()
                    pausar()
                    pygame.time.delay(200)
                    pygame.mixer.music.unpause()
        pygame.event.pump()

        '''
        
        # controlamos mirando el estado del device directamente:
        keys = pygame.key.get_pressed()
        ''' # es mas natural con ifs independientes (acordes...)
        if keys[pygame.K_LEFT]:  dron.vel[0] -= 1
        elif keys[pygame.K_RIGHT]: dron.vel[0] += 1
        elif keys[pygame.K_UP]:    dron.vel[1] -= 1
        elif keys[pygame.K_DOWN]:  dron.vel[1] += 1
        elif keys[pygame.K_SPACE]:  
            pygame.mixer.music.pause()
            pausar()
            pygame.time.delay(200)
            pygame.mixer.music.unpause()
        '''
        
        '''
        # esta es sencilla y posible pero da mas vel diagonal que en xóy
        if keys[pygame.K_LEFT]:  dron.vel[0] -= 1
        if keys[pygame.K_RIGHT]: dron.vel[0] += 1
        if keys[pygame.K_UP]:    dron.vel[1] -= 1
        if keys[pygame.K_DOWN]:  dron.vel[1] += 1
        if keys[pygame.K_SPACE]:  
            pygame.mixer.music.pause()
            pausar()
            pygame.time.delay(200)
            pygame.mixer.music.unpause()
        
        if dron.vel[0]< -5: dron.vel[0]=-5
        elif dron.vel[0]>5: dron.vel[0]= 5
        if dron.vel[1]< -5: dron.vel[1]=-5
        elif dron.vel[1]>5: dron.vel[1]= 5
        '''
        
        # control mas realista (vel = en diagonal que en xy):
        if keys[pygame.K_LEFT]:  dron.vel[0] -= 1
        if keys[pygame.K_RIGHT]: dron.vel[0] += 1
        if keys[pygame.K_UP]:    dron.vel[1] -= 1
        if keys[pygame.K_DOWN]:  dron.vel[1] += 1
        if keys[pygame.K_SPACE]:  
            pygame.mixer.music.pause()
            pausar()
            pygame.time.delay(200)
            pygame.mixer.music.unpause()
        kk, a = 6,  np.linalg.norm(dron.vel) # kk-1= vel max en cualquier dir
        if a>kk: 
            dron.vel[0] = round(kk*(dron.vel[0]/a))
            dron.vel[1] = round(kk*(dron.vel[1]/a))
        
        dron.update(v0, fondo_img)

        # gestion de choque con paredes
        if not rect_fondo.contains(dron.rect):
            do_crash()
            pygame.quit()
            

        # gestion de sacar foto
        a= pygame.sprite.spritecollideany(dron, castles_group)
        if a :
            if not a.hecho:
                if a.rect.contains(dron.rect) and all(abs(v)<2 for v in dron.vel) :
                    a.hecho=True
                    castles_hechos += 1
                    click_camara.play()
                    fondo_img.blit(fondo_img2, a.rect, a.rect)
        
        a= pygame.sprite.spritecollideany(dron, panzers_group)
        if a :
            if dron.rect.contains(a.rect) and a.hecho==False :
                a.hecho= True
                panzers_hechos += 1
                click_camara.play()

        # gestion de color y combustible del dron 
        b=[0., 0.4, 2., 3., 5.] # funcion no lineal del nivel
        a= int( (75+11*kung_fu)*b[nivel] )
        if dron.vida == 1:
            dron.image= dron_img
        elif dron.vida == 600 + a:
            dron.image = dron_mediogas
        elif dron.vida == 900 + a:
            dron.image = dron_singas
        elif dron.vida == 1200 + a:
            pygame.mixer.music.fadeout(600)
            dron.borra(v0,fondo_img)
            
            dron.image= dron_negro
            dron.rect=dron.image.get_rect()
            dron.rect.center = dron.pos
            dron.traza(v0)
            pygame.display.flip()
            dron_para.play()
            pygame.time.delay(1200)

            caerse_sound.play()
            pygame.time.delay(300)

            for kk in range(3):
                dron.borra(v0,fondo_img)
                dron.rect[2], dron.rect[3]= int(dron.rect[2]*0.7), int(dron.rect[3]*0.7)
                dron.image= pygame.transform.scale(dron.image, dron.rect[2:])
                dron.traza(v0)
                pygame.display.flip()
                pygame.time.delay(400)

            do_crash()
            pygame.quit()
            

        # gestion de programar y lanzar misiles
        for a in castles_group:
            kk=370-32*kung_fu
            if jcount % mi_random(kk-16*nivel,kk+10+16*nivel)==0 and a.cuentatras<-125+4*nivel: 
                # programar misil
                a.cuentatras = 40
                a.image= castlerojo_img
        for a in castles_group:
            if a.cuentatras == 0:
                a.cuentatras = -1
                a.image= castle_img
                vel= np.array(dron.rect.center) - np.array(a.rect.center)
                v= np.linalg.norm(vel)
                if v: 
                    vel= 4*vel/v # esto es solo inicial, para vel_misil tocar parrafo ss
                    misil= Misil (misil_img_tiesa, a.rect.center, vel)
                    misiles_group.add(misil)
        
        # gestion de actualizar misiles
        for b in misiles_group:
            b.vel= np.array(dron.rect.center) - np.array(b.rect.center)
            v= np.linalg.norm(b.vel)
            kk= 2.1+nivel/10.+kung_fu/6. # con kk=2 aburrido; con 4 es aun jugable, con 5 no
            b.vel= kk*b.vel/v if v else np.array([0,0])
            b.vel += 0.04*(nivel+kung_fu/2.)*dron.vel # un poco de anticipativa y kung-fu
        misiles_group.update(v0,fondo_img)
        for b in misiles_group: 
            if b.vida > b.vidamax:
                b.borra(v0,fondo_img)
                misiles_group.remove(b)

        # gestion de colision con misiles
        b= pygame.sprite.spritecollideany(dron, misiles_group, collided=
                    pygame.sprite.collide_rect_ratio(0.7))
        if b: 
            do_crash(b)
            pygame.quit()
            

        # mover panzers
        panzers_group.update(v0,fondo_img)
        for b in panzers_group:
            if not rect_fondo.contains(b.rect):
                b.vel = -b.vel
            elif b.vida % (60 + mi_random(-3,3))==0:
                b.vel = np.array((mi_random(-2,3), mi_random(-2,3)))

        # gestion de programar y lanzar balas
        for b in panzers_group:
            kk=280-22*kung_fu
            if b.vida % (kk + mi_random(-30,30))==0 and b.cuentatras <-130+3*(nivel+kung_fu): 
                # programar unas balas
                b.cuentatras = 34
                b.image = panzerojo_img
        for b in panzers_group:
            if b.cuentatras == 0:
                b.cuentratras = -1
                b.image = panzer_img
                vel_bala= 8. # velocidad base de las balas (estaria mejor fuera, pero legibilidad)
                
                d0= dron.pos - b.pos
                d= np.linalg.norm(d0)
                n0= d0/d
                v1= vel_bala*n0 # v1 apunta adonde esta el dron
                
                w0=np.array([-n0[1],n0[0]])
                v2=v1 + mi_random(-8,9)*w0/10 # v2 apunta random en un cono +-45º de v1
                
                v_rel= vel_bala - np.dot(dron.vel,n0)
                v3= n0*v_rel + dron.vel # v3 apunta adonde estimo q estara (normalizar si eso**)
                
                bala1=Misil(bala_img_tiesa, pos=b.pos, vel=v1)
                bala2=Misil(bala_img_tiesa, pos=b.pos, vel=v2)
                bala3=Misil(bala_img_tiesa, pos=b.pos, vel=v3)
                

                '''Esto de aqui tira a dar si el dron mantuviese vel cte. Pero
                5*sqr(2)=7.07=vel max dron, y si vel bala = 6 (como queria),  a veces 
                sin(tota)= v(y',dron)/v(bala)  >1 -> error (cuando y' está muy alineado
                con la vel del dron y este va rapido). Podría hacer elseno=np.sign(elseno)
                cuando abs(elseno)>1, o subir la vel de bala. De todas formas este "hacerlo bien"
                requiere demasiadas funciones costosas... pensar un simplificau ¿?
                
                d0= dron.pos - b.pos
                alfa = np.arctan2(d0[1],d0[0])
                elseno= (dron.vel[1]*np.cos(alfa)-dron.vel[0]*np.sin(alfa))/vel_bala
                tota = np.arcsin(elseno)
                a= alfa + tota
                v= vel_bala * np.array([np.cos(a), np.sin(a)])
                desvi= 0.5236 # 30 grados en rad
                
                bala1=Misil(bala_img_tiesa, pos=b.pos, vel=v)
                v= vel_bala * np.array([np.cos(a+desvi), np.sin(a+desvi)])
                bala2=Misil(bala_img_tiesa, pos=b.pos, vel=v)
                v= vel_bala * np.array([np.cos(a-desvi), np.sin(a-desvi)])
                bala3=Misil(bala_img_tiesa, pos=b.pos, vel=v)
                '''
                
                '''Esto es un tiro a la pos actual del dron corregido un poco con la 
                vel del dron. Todo en plan chapu. Funciona pero no me convence.
                
                v= dron.pos - b.pos
                d= np.linalg.norm(v) or 1.
                t= d/vel_bala # estimacion del t de impacto. Vel sin corregir sería v/t
                correc= dron.vel * t /2 # una correccion moderada
                v= (v+correc)/t  
                bala1=Misil(bala_img_tiesa, pos=b.pos, vel=v)
                v[0] += 1
                bala2=Misil(bala_img_tiesa, pos=b.pos, vel=v)
                v[1] -= 1
                bala3=Misil(bala_img_tiesa, pos=b.pos, vel=v)
                '''
                
                balas_group.add(bala1,bala2,bala3)

        # gestion de actualizar balas
        balas_group.update(v0,fondo_img)
        for b in balas_group:
            if b.vida > b.vidamax:
                b.borra(v0,fondo_img)
                balas_group.remove(b)

        # gestion de colision con balas
        b= pygame.sprite.spritecollideany(dron, balas_group, collided=
            pygame.sprite.collide_rect_ratio(0.7))
        if b: 
            do_crash(b)
            pygame.quit()
            

        pygame.display.flip()
        jcount += 1
        if jcount== 2547:  jcount=1


        # gestion de todo hecho
        if panzers_hechos + castles_hechos == len(panzers_group.sprites()) +4:
            if not gatepuesto :
                aparece_gate.play()
                gate_rect=gate_img.get_rect()
                gate_rect.midright= (aa, bb/2)
                gatepuesto=True
                
            # hay que gestionar el gate como si fuese un castle, pero no puedo
            # añadirlo a castles_group porque lanzaría misiles, se le sacaria
            # foto, etc. Lo hago ad hoc:
            fondo_img.blit(gate_img, gate_rect)
            v0.blit(fondo_img, gate_rect, gate_rect)
                
                
            if gate_rect.contains(dron.rect) and dron.vel[1]==0 and dron.vel[0]<3:
                acaba=True
                pygame.mixer.music.pause()
                dron_para.play()
                pygame.time.wait(4100)
                #print('Valor de jcount= ',jcount)

                if nivel==4:
                    brass= pygame.mixer.Sound(os.path.join(cwd,'brass_final.ogg'))
                    brass.play()
                    
                    fondo_img2=pygame.image.load(os.path.join(cwd, 'fondo_terrain1.png')).convert()
                    v0.blit(fondo_img2, (0,0))
                    v0.blit(dronfinal, (150,150))
                    texto= '¡Dron Campeón!'
                    cuadrotexto= font_jc.render(texto, True, (255,165,0) )
                    su_rect= cuadrotexto.get_rect().move(0.5*aa, 0.7*bb)
                    v0.blit(cuadrotexto, su_rect)
                    pygame.display.flip()
                    pygame.time.wait(6000)
                    pygame.quit()
                    



    

