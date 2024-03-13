import airsim
import numpy as np
import os
import time
from datetime import datetime
import csv

# connect to the AirSim simulator
client = airsim.MultirotorClient()

# by default the api control will be enabled, api control mode is required to move the vehicle programmatically
# the below line disables api control which switches control type to keyboard
# client.enableApiControl(False)

# the output path to save the images
outputPath = 'C:/Users/praga/OneDrive/Desktop/research/images/'

capture = True

# this keeps track of picture count
# if the collection for a given environment needs to be restarted this number will have to be updated to the number of collected images + 1 so as not to overwrite collected images
# for example if you have collect 10 images and something stops the script, then picture will have to be updated to 11 to no override existing images
picture = 1

# used to calcuate a time interval to collect images
last_time = time.time()

# the name of the environment the data is being collected from, this will be the folder that will be 
# created in the specified outputPath which will contain the images
environment = "BarnyardMegapack"

# the depth the data is being collected at
depthMeter = str(120)

# create a rgb dictionary with the rgb value as the key and id as the value
# airsim automatically assigns a id to each object and the corresponding rgb values are provided by airsim
# the file is rgb_ids.csv which was provided by airsim
# this is used to keep track of all of the ids seen in an environment which can be mapped to a specific rgb and is used for post processing 
objectCount = {}
fieldNames = []
filename = "../../rgb_ids.csv"
rgbDict = {}
with open(filename,'r') as data:
    for line in csv.reader(data, delimiter='\t'):
        rgbDict[line[1]] = int(line[0])
        
# the below checks to see if a class count already exists for the above environment on today's date and if so adds the count the object count.
# this is incase the environment collection needs to be restarted
today_date = f"{datetime.now():%Y-%m-%d}" 
fileName = environment + '_' + today_date + '.csv'
file_exists = os.path.isfile('C:/Users/praga/OneDrive/Desktop/research/classcount/' + fileName) 

if(file_exists):      
    with open('C:/Users/praga/OneDrive/Desktop/research/classcount/' + fileName , 'r') as objectCountFile:
        reader = csv.reader(objectCountFile)
        for line in reader:
            if line != []:
                objectCount[int(line[0])] = int(line[1])

# capturing the images                        
while capture:
    response = client.simGetImages([airsim.ImageRequest(3, airsim.ImageType.Scene, False, False), 
                               airsim.ImageRequest(3, airsim.ImageType.DepthPerspective, False, False),
                               airsim.ImageRequest(3, airsim.ImageType.Segmentation, False, False)
                               ])    
    
    pose = {}
    orientation = response[0].camera_orientation
    position = response[0].camera_position
    camera_pose = str(position.x_val) + ' ' + str(position.y_val) + ' ' + str(position.z_val) + ' ' + str(orientation.w_val) + ' ' + str(orientation.x_val) + ' ' + str(orientation.y_val) + ' ' + str(orientation.z_val)

    rgb = response[0]
    depth = response[1]
    seg = response[2]
    
    # get numpy array
    img1d_rgb = np.fromstring(rgb.image_data_uint8, dtype=np.uint8) 
    img1d_depth = np.fromstring(depth.image_data_uint8, dtype=np.uint8)
    img1d_seg = np.fromstring(seg.image_data_uint8, dtype=np.uint8) 
    
    # reshape array to 4 channel image array H X W X 4
    img_rgb = img1d_rgb.reshape(rgb.height, rgb.width, 3)
    img_depth = img1d_depth.reshape(depth.height, depth.width, 3)
    img_seg = img1d_seg.reshape(seg.height, seg.width, 3)

    current_date = datetime.now()
    current_time = current_date.time()
    today_date = f"{datetime.now():%Y-%m-%d}"
    
    # write to png 
    current_time = time.time()
    time_span = current_time - last_time
    if(time_span > 2):
        img_name = environment + '_' + today_date + "_" + str(picture) + "_" + "fpv"
        
        # sa images 
        airsim.write_png(os.path.normpath(outputPath + environment + '/' + depthMeter + '/rgb/' + img_name + 'dw_rgb' + '.png'), img_rgb) 
        airsim.write_png(os.path.normpath(outputPath + environment + '/' + depthMeter + '/depth/' + img_name + 'dw_depth' + '.png'), img_depth) 
        airsim.write_png(os.path.normpath(outputPath + environment + '/' + depthMeter + '/segmentation/' + img_name + 'dw_segmentation' + '.png'), img_seg) 
        
        # collect the camera pose to a pre specified csv file    
        output_camerapose_folder = 'C:/Users/praga/OneDrive/Desktop/research/camerapose/'
        with open(output_camerapose_folder + environment + '_' + today_date + 'dw.csv', 'w+') as d:
            writer = csv.writer(d)
            row_array = [img_name,camera_pose]
            writer.writerow(row_array)
        
        # this creates a class count file of the number of times a given id is seen in the environment
        # the count is then saved to specified folder         uniqueObjectsRGB = np.unique(img_seg.reshape(-1, img_seg.shape[2]), axis=0)
        output_class_count_folder = 'C:/Users/praga/OneDrive/Desktop/research/classcount/';
        uniqueObjectsRGB = np.unique(img_seg.reshape(-1, img_seg.shape[2]), axis=0)
        uniqueObjectsRGB = np.flip(uniqueObjectsRGB).tolist()
        for rgb in uniqueObjectsRGB:
            rgb = str(rgb).replace(",", "")
            if rgb in rgbDict:
                if rgbDict[rgb] in objectCount:
                    objectCount[int(rgbDict[rgb])] += 1
                else:
                    fieldNames.append(rgbDict[rgb])
                    objectCount[int(rgbDict[rgb])] = 1
        
        # change file name to reflect objectCount        
        with open(output_class_count_folder + fileName, 'w+') as objectCountFile:
            writer = csv.writer(objectCountFile)
            for objCt in objectCount:
                row_array = [objCt,objectCount[objCt]]
                writer.writerow(row_array)
                print(row_array)
        
        last_time = time.time()
        picture = picture + 1 
