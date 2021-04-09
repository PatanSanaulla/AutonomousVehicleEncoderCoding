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
    gpio.setup(12, gpio.IN, pull_up_down = gpio.PUD_UP)
    gpio.output(36, False)
    
def gameover():
    gpio.output(31, False)
    gpio.output(33, False)
    gpio.output(35, False)
    gpio.output(37, False)
    
    gpio.cleanup()
    
    
# main code
init()

#to write time delta in a file
file = open('encoder02.txt','a')

counter = np.uint64(0)
button = int(0)

# Initialize pwm signal to control meter
pwm = gpio.PWM(37, 50)
val = 14
pwm.start(val)
time.sleep(0.1)


while True:
    #print("counter = ", counter, "GPIO state: ", gpio.input(12))
    file.write(str(counter)+","+str(gpio.input(12))+'\n')    
    if int(gpio.input(12)) != int(button):
        button = int(gpio.input(12))
        counter += 1
        #print(counter)
        
    if counter >= 960:
        pwm.stop()
        gameover()
        print("Thanks for playing")
        break

file.close()
#print("counter = ", counter, "GPIO state: ", gpio.input(12))
