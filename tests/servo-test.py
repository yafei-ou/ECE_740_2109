import RPi.GPIO as io
from servo import Servo
from servowiringpi import ServoWiringpi
import time

# servoPin=7
# io.setmode(io.BOARD)
# io.setup(servoPin,io.OUT,initial=False)
# pwmServo=io.PWM(servoPin,50)
# pwmServo.start(0)

# angle = 90
# pwmServo.ChangeDutyCycle(2.5+angle/18)

# time.sleep(2)
# io.cleanup()

# myServo =  Servo(7)
# myServo.changeAngle(60)
# time.sleep(1)
# myServo.changeAngle(90)
# io.cleanup()

myservo = ServoWiringpi(1)
myservo.changeAngle(93)