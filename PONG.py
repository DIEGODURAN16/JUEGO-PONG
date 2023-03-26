from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import time

sensorizquierdo = ADC(Pin(14))
sensorderecho = ADC(Pin(26))
sensorizquierdo.atten(ADC.ATTN_11DB)
sensorizquierdo.width(ADC.WIDTH_12BIT)
sensorderecho.atten(ADC.ATTN_11DB)
sensorderecho.width(ADC.WIDTH_12BIT)

i2c = I2C(0, scl=Pin(12), sda=Pin(13))
oled = SSD1306_I2C(128, 64, i2c)


# Posición de las paletas
paletaizquierda = 25
paletaderecha = 25

# Posición de la pelota
pelotax = 64
pelotay = 32

# Dirección de la pelota
pelotadx = 1
pelotady = 1

# Puntos de cada jugador
puntosizquierda = 0
puntosderecha = 0

def dibujar():
    oled.fill(0)
    oled.rect(0, paletaizquierda-10, 5, 20, 1)
    oled.rect(123, paletaderecha-10, 5, 20, 1)
    oled.rect(pelotax-2, pelotay-2, 4, 4, 1)
    oled.text("PUNTUACION:", 20,0,1)
    oled.text(str(puntosizquierda), 40, 10)
    oled.text(str(puntosderecha), 80, 10)
    oled.show()

while True:
    # Mover las paletas
    paletaizquierda = int((4095 - sensorizquierdo.read()) / 40.95)
    paletaderecha = int((4095 - sensorderecho.read()) / 40.95)
    
    # Mover la pelota
    pelotax += pelotadx
    pelotay += pelotady
    
    # Detectar colisiones con los bordes y las paletas
    if pelotay < 4:
        pelotady = 1
    elif pelotay > 60:
        pelotady = -1
    elif pelotax < 7 and paletaizquierda-10 <= pelotay <= paletaizquierda+10:
        pelotadx = 1
    elif pelotax > 120 and paletaderecha-10 <= pelotay <= paletaderecha+10:
        pelotadx = -1
    elif pelotax < 0:
        puntosderecha += 1
        if puntosderecha >= 5:
            oled.fill(0)
            oled.text("Jugador dos", 20, 20)
            oled.text("gana!", 45, 35)
            oled.show()
            break
        pelotax = 64
        pelotay = 32
        pelotadx = 1
        pelotady = 1
    elif pelotax > 128:
        puntosizquierda += 1
        if puntosizquierda >= 5:
            oled.fill(0)
            oled.text("Jugador uno", 15, 20)
            oled.text("gana!", 45, 35)
            oled.show()
            break
        pelotax = 64
        pelotay = 32
        pelotadx = -1
        pelotady = 1
    
    # Dibujar los elementos del juego
    dibujar()
    
    # Esperar un breve periodo de tiempo para evitar que el juego se ejecute demasiado rápido
    time.sleep(0.001)
