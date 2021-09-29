import time
import RPi.GPIO as io
from simple_pid import PID
from motorl298n import MotorL298N



pinL298NIn = [38, 40]
pinEncoder = 29
EncoderNum = 0

motor = MotorL298N(pinL298NIn, pinEncoder)

def motorPositionCtrl(dest):
    currentPosition = motor.getPosition()
    if abs(dest-currentPosition)<10:
        return True
    elif dest>currentPosition:
        # motor forward
        motor.setDirection(1)

        pidPosition = PID(30, 0, 0)
        pidSpeed = PID(1, 0, 0)

        pidPosition.output_limits = (0, 500)
        pidSpeed.output_limits = (0, 100)
        pidPosition.setpoint = dest

        pLast = motor.getPosition()
        timeLast = time.perf_counter()

        isStoppedCounter = 0
        while True:
            timeNow = time.perf_counter()
            pNow = motor.getPosition()
            ## Position Loop
            pLoopOut = pidPosition(pNow)

            ## Speed Loop
            pidSpeed.setpoint = pLoopOut
            dtime = timeNow - timeLast
            speed = (pNow - pLast)/dtime
            if (dtime>5e-3):
                sLoopOut = pidSpeed(speed)
                motor.updatePWM(sLoopOut)

            if pLast==pNow:
                isStoppedCounter += 1
            else:
                isStoppedCounter = 0

            if isStoppedCounter > 5:
                motor.setDirection(0)
                motor.updatePWM
                break
            
            timeLast = timeNow
            pLast = pNow
            
            print(motor.getPosition())
            time.sleep(0.1)

    else:
        # motor backward
        motor.setDirection(-1)

        pidPosition = PID(15, 0, 0)
        pidSpeed = PID(1, 0, 0)

        pidPosition.output_limits = (0, 500)
        pidSpeed.output_limits = (0, 100)

        realCurrentPosition = motor.getPosition()
        pidPosition.setpoint = 2*realCurrentPosition - dest

        pLast = realCurrentPosition
        timeLast = time.perf_counter()

        isStoppedCounter = 0

        while True:
            timeNow = time.perf_counter()
            pNow = 2*realCurrentPosition - motor.getPosition()
            ## Position Loop
            pLoopOut = pidPosition(pNow)

            ## Speed Loop
            pidSpeed.setpoint = pLoopOut
            dtime = timeNow - timeLast
            speed = (pNow - pLast)/dtime
            if (dtime>5e-3):
                sLoopOut = pidSpeed(speed)
                motor.updatePWM(sLoopOut)
                
            if pLast==pNow:
                isStoppedCounter += 1
            else:
                isStoppedCounter = 0

            if isStoppedCounter > 5:
                motor.setDirection(0)
                motor.updatePWM
                break

            timeLast = timeNow
            pLast = pNow
            print(motor.getPosition())
            #print(pNow)
            time.sleep(0.1)

# while True:
#     motorPositionCtrl(200)
#     time.sleep(1)
#     motorPositionCtrl(-300)
#     time.sleep(1)

motorPositionCtrl(-2000)
# motor.setDirection(-1)
# motor.updatePWM(100)
# time.sleep(5)
io.cleanup()