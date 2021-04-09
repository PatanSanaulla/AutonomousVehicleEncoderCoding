import RPi.GPIO as gpio
import numpy as np
import time

##### INit the pins

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(31, gpio.OUT)
    gpio.setup(33, gpio.OUT)
    gpio.setup(35, gpio.OUT)
    gpio.setup(37, gpio.OUT)
    gpio.setup(36, gpio.OUT)
    gpio.output(36, False)
    gpio.setup(7, gpio.IN, pull_up_down = gpio.PUD_UP)
    gpio.setup(12, gpio.IN, pull_up_down = gpio.PUD_UP)
    
def gameover():
    gpio.output(31, False)
    gpio.output(33, False)
    gpio.output(35, False)
    gpio.output(37, False)
    
    gpio.cleanup()
    
#to write time delta in a file
file = open('encoder04.txt','a')
# main code
init()

counterBR = np.uint64(0)
counterFL = np.uint64(0)

buttonBR = int(0)
buttonFL = int(0)

# Initialize pwm signal to control motor
pwm1 = gpio.PWM(37, 50) #Right side
pwm2 = gpio.PWM(31, 50) #Left side
val = 22
pwm1.start(val)
pwm2.start(val)
time.sleep(0.1)


while True:
    #print("counterBR = ", counterBR,"counterFL = ", counterFL, "BR state: ", gpio.input(12), "FL state: ", gpio.input(7))
    file.write(str(counterBR)+","+str(counterFL)+","+str(gpio.input(12))+","+str(gpio.input(7))+'\n')
    if int(gpio.input(12)) != int(buttonBR):
        buttonBR = int(gpio.input(12))
        counterBR += 1
        
    if int(gpio.input(7)) != int(buttonFL):
        buttonFL = int(gpio.input(7))
        counterFL += 1
        #print(counter)
        
    if counterBR >= 960:
        pwm1.stop()
        
    if counterFL >= 960:
        pwm2.stop()
        
    if counterFL >= 960 and counterBR >= 960:
        pwm1.stop()
        pwm2.stop()
        gameover()
        break

file.close()
#print("counter = ", counter, "GPIO state: ", gpio.input(12))


