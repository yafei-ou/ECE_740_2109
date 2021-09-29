import RPi.GPIO as io
import time
import yaml
from ruamel import yaml as ryaml

buttonSwitchPin = 18
buttonAdjustArmPin = 13

io.setmode(io.BOARD)
io.setup(buttonAdjustArmPin, io.IN, pull_up_down=io.PUD_DOWN)
io.add_event_detect(buttonAdjustArmPin, io.RISING, bouncetime=200)
io.setup(buttonSwitchPin, io.IN, pull_up_down=io.PUD_DOWN)

with open("config.yaml",encoding="UTF-8") as configFile:
    configData = yaml.load(configFile, Loader=yaml.FullLoader)

    currentPositionPulse = configData["data"]["currentPositionPulse"]
    memorizedPositionPulse = configData["data"]["memorizedPositionPulse"]

flagInit = True
flagRestore = True

while True:
    
    if flagInit:
        print("servo reset to zero")
        print("motor reset to zero")
        flagInit = False

    if io.input(buttonSwitchPin):
        if flagRestore:
            print("arm restored to previous position")
            flagRestore = False

        print("head pose updated")

        if io.event_detected(buttonAdjustArmPin):
            print("adjust arm position")
            configData["data"]["memorizedPositionPulse"] = 123

        with open("config.yaml","w",encoding="UTF-8") as configFile:
            ryaml.dump(configData, configFile, Dumper=ryaml.RoundTripDumper)
        # time.sleep(2)