import RPi.GPIO as GPIO
import sys, traceback, json
from time import sleep
from re import findall
from subprocess import check_output

interval = 1

def get_temp():
    temp = check_output(["vcgencmd", "measure_temp"]).decode()
    temp = float(findall(r'\d+\.\d+', temp)[0])
    return temp

def count_pulse(channel):
    global pulse_count
    pulse_count += 1

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

try:
    settings = read_json("settings.json")
    tempOn = int(settings['tempOn'])
    tempOff = int(settings['tempOff'])
    mode = settings['mode']
    
    controlPin = 14
    pinState = False

    tachPin = 12
    pulse_count = 0
    rpm = 0
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(controlPin, GPIO.OUT, initial=0)
    GPIO.setup(tachPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(tachPin, GPIO.FALLING, callback=count_pulse)

    while True:
        settings = read_json("settings.json")
        tempOn = int(settings['tempOn'])
        tempOff = int(settings['tempOff'])
        mode = settings['mode']

        temp = get_temp()
        pulse_count = 0

        if mode == 'smart':
            if temp > tempOn and not pinState or temp < tempOff and pinState:
                pinState = not pinState
                GPIO.output(controlPin, pinState)
        elif mode == 'normal':
            if temp > tempOn:
                pinState = True
                GPIO.output(controlPin, pinState)
            elif temp < tempOn:
                pinState = False
                GPIO.output(controlPin, pinState)
        else:
            pinState = True
            GPIO.output(controlPin, pinState)

        sleep(1)
        rpm = (pulse_count / 2) * (60 / interval)

        data = {
            "Temperature": temp,
            "Fan State": 'On' if pinState else 'Off',
            "RPM": rpm
        }
        
        write_json("current.json", data)
        print(f"Temperature: {temp}°C, Fan State: {'On' if pinState else 'Off'}, RPM: {rpm}, Mode: {mode}, TempOn: {tempOn}, TempOff: {tempOff}")
        

except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")
except Exception as e:
    print("Other Exception")
    print("--- Start Exception Data:")
    traceback.print_exc(limit=2, file=sys.stdout)
    print("--- End Exception Data:")
finally:
    print("CleanUp")
    GPIO.cleanup()
    print("End of program")
