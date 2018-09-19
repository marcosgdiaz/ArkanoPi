import pygame,sys
import os
import time
import RPi.GPIO as GPIO
from random import randint
from pygame.locals import *

#Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL=(0,0,255)
VERDE=(0,255,0)
AMARILLO=(255,255,0)
GRIS=(192,192,192)
CIAN=(0,255,255)
NARANJA=(255,128,0)
MAGENTA=(128,0,128)


#Variables globales
Ancho=320
Alto=240
pared1=pygame.Rect(0,0,1,Alto)
pared2=pygame.Rect(Ancho,0,1,Alto)
pared3=pygame.Rect(0,0,Ancho,1)
pared4=pygame.Rect(0,Alto,Ancho,1)
listaParedes=[pared1,pared2,pared3,pared4]

#texto=fuente.render("Presione e para empezar",True,BLANCO)

#texto2=fuente.render("Victoria, presione e para volver a empezar",True,BLANCO)

 

#Clases

			
class Raqueta(pygame.sprite.Sprite):
	def __init__(self,posy):
		pygame.sprite.Sprite.__init__(self)
		self.rect1=pygame.Rect(16*10,posy,16,8)
		self.rect2=pygame.Rect(16*10+16,posy,16,8)
		self.rect3=pygame.Rect(16*10+16*2,posy,16,8)
		self.rect4=pygame.Rect(16*10+16*3,posy,16,8)
		self.velocidadRaqueta=5
		self.velocidadBola=6
		self.endisparo=False
		self.listaDisparo=[]

	def MovimientoIzq(self):
		if self.rect4.right>16:
			self.rect1.left-=self.velocidadRaqueta
			self.rect2.left-=self.velocidadRaqueta
			self.rect3.left-=self.velocidadRaqueta
			self.rect4.left-=self.velocidadRaqueta

	def MovimientoDech(self):
		if self.rect1.left < Ancho-16:
			self.rect1.left+=self.velocidadRaqueta
			self.rect2.left+=self.velocidadRaqueta
			self.rect3.left+=self.velocidadRaqueta
			self.rect4.left+=self.velocidadRaqueta

	def MovimientoDisparo(self,BloqueLadrillos):
		if self.endisparo:
			if self.bola.colliderect(listaParedes[2]):
				self.endisparo=False
			else:
				for i in BloqueLadrillos:
					if self.bola.colliderect(i.rect):
						self.endisparo=False
						BloqueLadrillos.remove(i)	
			self.bola.top-=self.velocidadBola

	def disparo(self):
		if len(self.listaDisparo)>0 and self.endisparo==False:
			self.bola=pygame.Rect(self.rect2.centerx,self.rect2.top+16,2,8)
			self.listaDisparo.pop(len(self.listaDisparo)-1)
			self.endisparo=True

	def dibujar(self,superficie):
		pygame.draw.rect(superficie,GRIS,self.rect1,0)
		pygame.draw.rect(superficie,GRIS,self.rect2,0)
		pygame.draw.rect(superficie,GRIS,self.rect3,0)
		pygame.draw.rect(superficie,GRIS,self.rect4,0)
		if self.endisparo:
			pygame.draw.rect(superficie,NARANJA,self.bola,0)

class Pelota(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.ImagenPelota=pygame.image.load('Imagenes/ball.gif')
		self.rect=pygame.Rect(16*10,32*3,8,8)
		self.velocidadPelotax=0
		self.velocidadPelotay=3
		self.jugando=True
		self.activando=False
		self.velocidadActivador=2  

	def dibujar(self,superficie):
		pygame.draw.circle(superficie,CIAN,self.rect.center,4,0)
		if self.activando:
			pygame.draw.rect(superficie,NARANJA,self.activador,0)

	def MovimientoActivador(self,Raqueta):
		if self.activando:
			if self.activador.colliderect(Raqueta.rect1) or self.activador.colliderect(Raqueta.rect2) or self.activador.colliderect(Raqueta.rect3) or self.activador.colliderect(Raqueta.rect4):
				self.activando=False
				Raqueta.listaDisparo.append(1)
			elif self.activador.colliderect(listaParedes[3]):
				self.activando=False	
			self.activador.top+=self.velocidadActivador
		
				
	def MovimientoPelota(self,BloqueLadrillos,Raqueta):
		num=self.rect.collidelistall(BloqueLadrillos)
		if self.rect.colliderect(Raqueta.rect1):
			self.velocidadPelotay=-3
			self.velocidadPelotax=-3
		elif self.rect.colliderect(Raqueta.rect2):
			self.velocidadPelotax=-1
			self.velocidadPelotay=-4
		elif self.rect.colliderect(Raqueta.rect3):
			self.velocidadPelotax=1
			self.velocidadPelotay=-4
		elif self.rect.colliderect(Raqueta.rect4):
			self.velocidadPelotax=3
			self.velocidadPelotay=-3					
		elif self.rect.colliderect(listaParedes[0]) or self.rect.colliderect(listaParedes[1]):
			self.velocidadPelotax*=-1
		elif self.rect.colliderect(listaParedes[2]):
			self.velocidadPelotay*=-1
		elif self.rect.colliderect(listaParedes[3]):
			self.jugando=False
		elif len(BloqueLadrillos)==0:
			self.jugando=False
		elif len(num)>0:
			if randint(0,3)==0 and self.activando==False:
		 		self.activador=pygame.Rect(BloqueLadrillos[num[0]].rect.centerx,BloqueLadrillos[num[0]].rect.centery+16,2,8)
                                self.activando=True
			contador=0
			dif=0
			for i in num:
				if self.rect.colliderect(BloqueLadrillos[i-contador].ParedRigh) or self.rect.colliderect(BloqueLadrillos[i-contador].ParedLeft):
					dif+=1	
				BloqueLadrillos.remove(BloqueLadrillos[i-contador])
				contador+=1
			if dif>0:
				self.velocidadPelotax*=-1
			elif len(num)-dif>0:
				self.velocidadPelotay*=-1	
		self.rect.top+=self.velocidadPelotay
		self.rect.left+=self.velocidadPelotax

	def MovimientoPong(self,Raqueta1,Raqueta2):
		if self.rect.colliderect(Raqueta1.rect1):
			self.velocidadPelotay=-3
			self.velocidadPelotax=-3
		elif self.rect.colliderect(Raqueta1.rect2):
			self.velocidadPelotax=-1
			self.velocidadPelotay=-4
		elif self.rect.colliderect(Raqueta1.rect3):
			self.velocidadPelotax=1
			self.velocidadPelotay=-4
		elif self.rect.colliderect(Raqueta1.rect4):
			self.velocidadPelotax=3
			self.velocidadPelotay=-3	
		elif self.rect.colliderect(Raqueta2.rect1):
			self.velocidadPelotay=3
			self.velocidadPelotax=-3
		elif self.rect.colliderect(Raqueta2.rect2):
			self.velocidadPelotax=-1
			self.velocidadPelotay=4
		elif self.rect.colliderect(Raqueta2.rect3):
			self.velocidadPelotax=1
			self.velocidadPelotay=4
		elif self.rect.colliderect(Raqueta2.rect4):
			self.velocidadPelotax=3
			self.velocidadPelotay=3		
		elif self.rect.colliderect(listaParedes[0]) or self.rect.colliderect(listaParedes[1]):
			self.velocidadPelotax*=-1
		elif self.rect.colliderect(listaParedes[2]) or self.rect.colliderect(listaParedes[3]):
			self.jugando=False	
		self.rect.top+=self.velocidadPelotay
		self.rect.left+=self.velocidadPelotax											

class Ladrillo(pygame.sprite.Sprite):
	def __init__(self,x,y,color):
		pygame.sprite.Sprite.__init__(self)
		self.rect=pygame.Rect(x,y,31,15)
		self.ParedRigh=pygame.Rect(x+31,y-1,1,13)
		self.ParedLeft=pygame.Rect(x,y-1,1,13)
		self.color=color	

	def dibujar(self,superficie):
		pygame.draw.rect(superficie,self.color,self.rect,0)	

class Arkanoid():
	def __init__(self):
		listaBloque=[]
		self.jugador=Raqueta(Alto-8)
		self.pelota=Pelota()
		self.listaColores=[ROJO,AMARILLO,AZUL,VERDE]
		self.listaBloque=BloqueLadrillos(listaBloque,self.listaColores)
		self.tiempo=pygame.time.get_ticks()/1000
		self.contador=0

	def DibujarBloque(self,superficie):
		for i in range(len(self.listaBloque)):
			self.listaBloque[i].dibujar(superficie)

	def MovimientoBloque(self):
		for i in self.listaBloque:
			i.rect.top+=16			
		for i in range(10):
			self.listaBloque.append(Ladrillo(i*32,0,MAGENTA))

	def dibujar(self,superficie):
		self.pelota.dibujar(superficie)					
		self.jugador.dibujar(superficie)
		self.DibujarBloque(superficie)			

class Pong():
	def __init__(self):
		self.jugador=Raqueta(Alto-8)
		self.jugador2=Raqueta(0)
		self.pelota=Pelota()

	def dibujar(self,superficie):
		pygame.draw.line(superficie,BLANCO,(0,119),(320,119),2)
		pygame.draw.circle(superficie,BLANCO,(159,119),30,2)
		self.pelota.dibujar(superficie)
		self.jugador2.dibujar(superficie)
		self.jugador.dibujar(superficie)	

class GameState():
	def __init__(self,superficie):
		self.state=0
		self.superficie=superficie
		self.__MensajeInicial()
		
	def __MensajeInicial(self):
		fuente=pygame.font.Font(None,30)
		texto=fuente.render("Izq->Arkano Derch->Pong",True,BLANCO)
		self.superficie.blit(texto,[10,120])

	def InicializaJuegoArkano(self):
		self.juego=Arkanoid()
		self.state=1

	def InicializaJuegoPong(self):
		self.juego=Pong()
		self.state=2

	def __FinalizaJuegoArkano(self):
		self.state=0
		fuente=pygame.font.Font(None,26)
		texto1=fuente.render("Game over",True,BLANCO)
		texto2=fuente.render("Victoria, su tiempo es: "+str(self.juego.contador*22+pygame.time.get_ticks()/1000-self.juego.tiempo),True,BLANCO)
		if len(self.juego.listaBloque)>0:
			self.superficie.blit(texto1,[10,60])

		else:
			self.superficie.blit(texto2,[10,60])
		self.__MensajeInicial()	
		

	def __FinalizaJuegoPong(self):
		self.state=0
		self.__MensajeInicial()
				
	
	def transiciones(self):
		if self.state==1:
			self.juego.pelota.MovimientoPelota(self.juego.listaBloque,self.juego.jugador)
			self.juego.jugador.MovimientoDisparo(self.juego.listaBloque)
			self.juego.pelota.MovimientoActivador(self.juego.jugador)
			if pygame.time.get_ticks()/1000-self.juego.tiempo>=22:
				self.juego.tiempo=pygame.time.get_ticks()/1000
				self.juego.MovimientoBloque()
				self.juego.contador+=1
			self.superficie.fill(NEGRO)
			self.juego.dibujar(self.superficie)
			if self.juego.pelota.jugando==False:
				self.__FinalizaJuegoArkano()
		elif self.state==2:
			self.juego.pelota.MovimientoPong(self.juego.jugador,self.juego.jugador2)
			self.superficie.fill(NEGRO)
			self.juego.dibujar(self.superficie)
			if self.juego.pelota.jugando==False:
				self.__FinalizaJuegoPong()		
				
	
			



def BloqueLadrillos(listaBloque,listaColores):
	for i in range(10):
		for k in range(4):
			listaBloque.append(Ladrillo(i*32,(k*16)+32,listaColores[k]))
	return listaBloque


def ArkanoPi():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarning(False)
	GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(23,GPIO.FALLING)
	GPIO.add_event_detect(22,GPIO.FALLING)
	os.putenv('SDL_FBDEV','/dev/fb1')
	pygame.init()
	ventana=pygame.display.set_mode((Ancho,Alto),pygame.FULLSCREEN)
	pygame.mouse.set_visible(0)
	ventana.fill(NEGRO)
	estado=0
	Maquina=GameState(ventana)
 	reloj=pygame.time.Clock()
	while True:
		reloj.tick(60)
		
		# #CONTROL POR BOTONES
		if GPIO.input(23)==False:
			if Maquina.state==2:
				Maquina.juego.jugador2.MovimientoIzq()
		elif GPIO.input(22)==False:
			if Maquina.state==2:
				Maquina.juego.jugador2.MovimientoDech()	
		if GPIO.input(27)==False:
			if Maquina.state==1 or Maquina.state==2:
				Maquina.juego.jugador.MovimientoIzq()	
		elif GPIO.input(18)==False:
			if Maquina.state==1 or Maquina.state==2:
				Maquina.juego.jugador.MovimientoDech()	

		if GPIO.event_detected(23):
			if Maquina.state==1:
				Maquina.juego.jugador.disparo()				
			elif Maquina.state==0:
				Maquina.InicializaJuegoArkano()			
		elif GPIO.event_detected(22):
			if Maquina.state==0:
				Maquina.InicializaJuegoPong()
			elif Maquina.state==1:
				Maquina.InicializaJuegoArkano()

		#CONTROL POR TECLADO ESTANDAR
		keys=pygame.key.get_pressed()		
		if keys[pygame.K_LEFT]:
			if Maquina.state==1 or Maquina.state==2:
				Maquina.juego.jugador.MovimientoIzq()	
		elif keys[pygame.K_RIGHT]:
			if Maquina.state==1 or Maquina.state==2:
				Maquina.juego.jugador.MovimientoDech()	
		if keys[pygame.K_a]:
			if Maquina.state==2:
				Maquina.juego.jugador2.MovimientoIzq()	
		elif keys[pygame.K_d]:
			if Maquina.state==2:
				Maquina.juego.jugador2.MovimientoDech()		


		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == K_a:
					if Maquina.state==1:
						Maquina.juego.jugador.disparo()				
					elif Maquina.state==0:
						Maquina.InicializaJuegoArkano()
				elif event.key == K_d:
					if Maquina.state==0:
						Maquina.InicializaJuegoPong()
					elif Maquina.state==1:
						Maquina.InicializaJuegoArkano()				
				elif event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				
								
		Maquina.transiciones()
		pygame.display.update() 

ArkanoPi()
