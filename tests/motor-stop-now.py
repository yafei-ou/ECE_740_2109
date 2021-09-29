import RPi.GPIO as io
from motorl298n import MotorL298N
from servo import Servo

# --------------- Motor Initialization ---------------
pinL298NIn = [38, 40]
pinEncoder = 29

motor = MotorL298N(pinL298NIn, pinEncoder, 0)
# --------------- Servo Initialization ---------------
servoPin = 7
myServo = Servo(servoPin)

myServo.changeAngle(90)
myServo.stop()
motor.setDirection(1)
motor.updatePWM(0)
io.cleanup()