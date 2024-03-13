import argparse
import os.path as osp
import numpy as np
import mmcv
# import cv2
from PIL import Image
import mmengine.fileio as fileio
import shutil

unknownColors = []

# the main output directory for the segmentation images and rgb images
vail_dir = "./data/vail_all/"

# directory of unconverted segmentation images
annotation_folder = "unconverted_annotations/"

# output path of converted segmentation images
converted_annotation_folder = "annotations/"

# directory containg all rgb images
all_images_dir = "images_all/"

# output path of rgb images, this is just so that as we converted the segmentation images the rgb images is copied over to the images folder
images_dir = "images/"

# the full output path of the converted segmentation images
convertedDir = vail_dir + converted_annotation_folder

# this is used also move segmentation images to a folder by their split
unconverted_split_annotations = 'unconverted_split_annotations/'

CLASSES = ('grass', 'tree', 'pole', 'water', 'sky',
                 'vehicle', 'container generic object', 'asphalt', 'gravel',
                 'mulch', 'rockbed', 'log', 'bicycle', 'person', 'fence', 'bush',
                 'sign', 'rock', 'bridge', 'concrete', 'table', 'building',
                 'void', 'generic ground')

PALETTE = [[ 0, 102, 0 ], [ 3, 213, 5 ], [ 9, 130, 130 ], [ 0, 128, 255 ], [ 0, 0, 255 ],
            [ 255, 255, 1 ], [ 255, 0, 127 ], [ 64, 64, 64 ], [ 255, 128, 0 ],
            [ 154, 76, 0 ], [ 102, 102, 0 ], [ 102, 0, 0 ], [ 0, 255, 128 ],[ 204, 153, 255 ], [ 101, 0, 205 ], [ 255, 153, 204 ],
            [ 0, 102, 101 ], [ 153, 204, 255 ], [ 102, 255, 255 ], [ 101, 101, 11 ], [ 114, 85, 47 ], [ 66, 0, 0 ],
            [ 7, 39, 194 ], [ 187, 70, 156 ]]

Groups = [0, 1, 2, 3, 4, 
          5, 6, 7, 8, 
          9, 10, 11, 12, 13, 14, 15, 
          16, 17, 18, 19, 20, 21, 22,
          23]


# 0 -- Background: void, sky, sign
# 1 -- Level1 (smooth) - Navigable: concrete, asphalt, generic ground
# 2 -- Level2 (rough) - Navigable: gravel, grass, dirt, sand, mulch
# 3 -- Level3 (bumpy) - Navigable: Rock, Rock-bed
# 4 -- Non-Navigable (forbidden) - water
# 5 -- Obstacle - tree, pole, vehicle, container/generic-object, building, log, 
#                 bicycle(could be removed), person, fence, bush, picnic-table, bridge,

color_id = {tuple(c):i for i, c in enumerate(PALETTE)}
color_id[tuple([0, 0, 0])] = 255

def rgb2mask(img):
    # assert len(img) == 3
    h, w, c = img.shape
    out = np.ones((h, w, c)) * 255
    for i in range(h):
        for j in range(w):
            # print(img[i, j])
            if tuple(img[i, j]) in color_id:
                out[i][j] = color_id[tuple(img[i, j])]
            else:
                unknownColors.append(tuple(img[i, j]))
                # exit(0)
                out[i][j] = color_id[(7, 39, 194)]

    return out


def raw_to_seq(seg):
    h, w = seg.shape
    out = np.zeros((h, w))
    for i in range(len(Groups)):
        out[seg==i] = Groups[i]

    out[seg==255] = 0
    return out

def relabel(dir, txtfile, split):
    ###


    ###
    currCount = 0
    with open(f'{dir}/{txtfile}', 'r') as imageNames:
        for name in imageNames:
            print(f"{split} : {currCount}")
            print(name)
            name = name.strip()
            currCount = currCount + 1
            file_client_args=dict(backend='disk')        
            img_or_path = dir + annotation_folder + name
            file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
            img_bytes = file_client.get(img_or_path) 
            gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
            gt_semantic_seg[:, :] = gt_semantic_seg[:, :, ::-1]
            out = rgb2mask(gt_semantic_seg)
            out = out[:, :, 0]
            out2 = raw_to_seq(out)
            mmcv.imwrite(out2, vail_dir + f"annotations/{split}/" + name)

            #images
            curImgPathDir = vail_dir + all_images_dir + name
            toImgDir = f"{vail_dir}{images_dir}{split}/{name}"
            shutil.copy(curImgPathDir, toImgDir)

            #segmentation
            curSegDir =f'{vail_dir}{annotation_folder}'
            curSegImg = f'{curSegDir}{name}'
            toSegImg = f'{vail_dir}{unconverted_split_annotations}{split}/{name}'
            shutil.copy(curSegImg, toSegImg)

# the directory containing the text file with the splits, the text file name, and the split
# the train and test splits to use should be specified in a txt file 
relabel(vail_dir, "train.txt", "train")