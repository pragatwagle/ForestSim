import airsim

import sys
import time

print("""This script is designed to fly on the streets of the Neighborhood environment
and assumes the unreal position of the drone is [160, -1500, 120].""")

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

print("arming the drone...")
client.armDisarm(True)

state = client.getMultirotorState()
if state.landed_state == airsim.LandedState.Landed:
    print("taking off...")
    client.takeoffAsync().join()
else:
    client.hoverAsync().join()

time.sleep(1)

state = client.getMultirotorState()
if state.landed_state == airsim.LandedState.Landed:
    print("take off failed...")
    sys.exit(1)

# the depth at which to collect the iamge
depths = [-120]

# have to repeat for time period 
for j in range(len(depths)):
    # AirSim uses NED coordinates so negative axis is up.
    # z of -5 is 5 meters above the original launch point.
    z = depths[j]
    print("make sure we are hovering at {} meters...".format(-z))
    client.moveToZAsync(z, 3).join()

    print("flying on path...")
    x = 100
    y = 100
    for i in range(3):
        # moves in square
        result = client.moveOnPathAsync([airsim.Vector3r(0,y,z),
                                    airsim.Vector3r(x,y,z),
                                    airsim.Vector3r(x,0,z),
                                    airsim.Vector3r(x,-y,z),
                                    airsim.Vector3r(-x,-y,z),
                                    airsim.Vector3r(-x,0,z),
                                    airsim.Vector3r(-x,y,z),                                
                                    ],
                            20, 120,
                            airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0), 20, 1).join()
        y = y + 50
        x= x + 50
        print(i)
        
# drone will over-shoot so we bring it back to the start point before landing.
client.moveToPositionAsync(0,0,z,1).join()
print("landing...")
client.landAsync().join()
print("disarming...")
client.armDisarm(False)
client.enableApiControl(False)
print("done.")

