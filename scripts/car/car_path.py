import airsim
import cv2
import numpy as np0
import os
import time
import tempfile

# connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection() 
client.enableApiControl(True)
print("API Control enabled: %s"
      % client.isApiControlEnabled())
car_controls = airsim.CarControls()

tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_car")
print ("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

drive = True
while drive:
    # get state of the car
    car_state = client.getCarState()
    print("Speed %d, Gear %d" % (car_state.speed, car_state.gear))

    # go forward
    car_controls.throttle = 10
    car_controls.steering = 0
    client.setCarControls(car_controls)
    print("Go Forward")
    time.sleep(8)   # let car drive a bit

    # go reverse
    car_controls.throttle = -3
    car_controls.is_manual_gear = True
    car_controls.manual_gear = -1
    car_controls.steering = 1
    client.setCarControls(car_controls)
    print("Go reverse, steer right")
    time.sleep(7)   # let car drive a bit
    car_controls.is_manual_gear = False # change back gear to auto
    car_controls.manual_gear = 0
    
    
    # go forward
    car_controls.throttle = 10
    car_controls.steering = 0
    client.setCarControls(car_controls)
    print("Go Forward")
    time.sleep(6)   # let car drive a bit

    # Go forward + steer left
    car_controls.throttle = 4.5
    car_controls.steering = 1
    car_controls.steering = -1
    client.setCarControls(car_controls)
    print("Go Forward, steer right")
    time.sleep(6)   # let car drive a bit
    
    # go reverse
    # go forward
    # car_controls.throttle = 1.5
    # car_controls.steering = 0
    # client.setCarControls(car_controls)
    # print("Go Forward")
    # time.sleep(5)   # let car drive a bit
    
    # go reverse
    car_controls.throttle = -6.5
    car_controls.is_manual_gear = True
    car_controls.manual_gear = -1
    car_controls.steering = 1
    client.setCarControls(car_controls)
    print("Go reverse, steer right")
    time.sleep(7)   # let car drive a bit
    car_controls.is_manual_gear = False # change back gear to auto
    car_controls.manual_gear = 0
    
    # apply brakes
    car_controls.brake = 1
    client.setCarControls(car_controls)
    print("Apply brakes")
    time.sleep(3)   # let car drive a bit
    car_controls.brake = 0 #remove brake

#restore to original state
client.reset()

client.enableApiControl(False)
