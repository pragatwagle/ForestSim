import cv2
import os
import pandas as pd
import numpy as np

# the environment that will be post processed
environment = 'OpenWorldsMediterrean'

# the location of the segmentation images collected from airsim for that environment
file_location = f'/Users/pragatwagle/Desktop/research/images/Labeled/{environment}/segmentation/pre_processed'
   
# the mapping file created where you mapped each rgb id to an object                
labelFileName = 'openworlds-mediterrean-labeled.csv'

# the exact location of the mapping file
labels = f"/Users/pragatwagle/Desktop/research/labels/labeled/csv/{labelFileName}"
labels_df = pd.read_csv(labels)
print(labels_df)

# labels of Labels and seg ids
labels_name_segids = labels_df[['Label', 'Seg Ids']]

# the mapping for the label to chosen rgb value for that label to be
object_with_rgbs = "./LabelsWRGBS.csv"
objects_df = pd.read_csv(object_with_rgbs)
objects_label_rgbs = objects_df[["Label", "RGB"]]

#make value of rgbs as numpy.ndarray
objects_label_rgbs_dict = dict(zip(objects_label_rgbs.Label, objects_label_rgbs.RGB))
print(objects_label_rgbs_dict)


# cv2 when it reads the images flips the rgb order and thus the rgb_ids.csv file had to be flipped
seg_id_rgb_mapping = pd.read_csv("./flipped_rgb_ids.csv", delimiter=',')
ids_array = []

# labels with all rgb values
# find the rgb values of each seg id and assign to the dictionary the rgb values 
label_rgbs = {}
for row in labels_name_segids.values:
    label = row[0]
    seg_ids = []
    for val in row[1:len(row)]:
        print(val)
        seg_ids = val.split(', ')
        for id in seg_ids:
            if label in label_rgbs:
                label_rgbs[label].append(seg_id_rgb_mapping\
                .loc[seg_id_rgb_mapping['ID'] == int(id)]\
                ["RGB"].values)
            else:
                label_rgbs[label] = [seg_id_rgb_mapping\
                .loc[seg_id_rgb_mapping['ID'] == int(id)]\
                ["RGB"].values]
 
#create a dictionary of rgb's to label:
rgbstolabel = {}

for label in label_rgbs:
    for rgb in label_rgbs[label]:
        rgbstolabel[rgb[0]] = label
 
print(rgbstolabel)

 # get all iamges names 
image_names = os.listdir(file_location)

# convert and write the image files
rgbs_not_labeled = []
for img_name in image_names:
    
    #output folder
    folder_path = f"/Users/pragatwagle/Desktop/research/images/Labeled/{environment}/segmentation/"
    
    pre_path = folder_path + "pre_processed/"
    post_path = folder_path + "post_processed/"
    img_path = pre_path + f'{img_name}'
    img = cv2.imread(img_path)
    output_img_name = img_name.split(".")[0] + '_post_processed.png'
    print(output_img_name)
    for row in range(1024):
        for i in range(2048):
            if img is not None:
                if img[row] is not None:
                    if img[row][i] is not None:
                        pixel_rgb_value = img[row][i]
                        # print(type(pixel_rgb_value))
                        rgbtostring = ''
                        for val in pixel_rgb_value:
                            rgbtostring = str(rgbtostring) + ' ' +  str(val)
                        rgbtostring = rgbtostring.strip()
                        
                        if rgbtostring in rgbstolabel:
                            label = rgbstolabel[rgbtostring]
                        else:
                            rgbs_not_labeled.append(rgbtostring)
                            label = "grass"

                        if label != "Generic Ground":
                            correctedRgb = objects_label_rgbs_dict[label]
                            correctedRgb = correctedRgb.replace("]", "")
                            correctedRgb = correctedRgb.replace("[", "")
                            correctedRgb = correctedRgb.split(" ")
                            img[row][i] = [correctedRgb[0], correctedRgb[1] ,correctedRgb[2]]
                        else:
                            correctedRgb = objects_label_rgbs_dict["Generic Ground"]
                            correctedRgb = correctedRgb.replace("]", "")
                            correctedRgb = correctedRgb.replace("[", "")
                            correctedRgb = correctedRgb.split(" ")
                            img[row][i] = [correctedRgb[0], correctedRgb[1] ,correctedRgb[2]]    
    if img is not None:            
        output_path =   post_path + output_img_name
        print(output_path)          
        cv2.imwrite(output_path, img)
    
print("Successfully Completed")