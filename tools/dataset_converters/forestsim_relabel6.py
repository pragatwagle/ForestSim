import argparse
import os.path as osp
import numpy as np
import mmcv
# import cv2
from PIL import Image
import mmengine.fileio as fileio
import shutil

unknownColors = []
vail_dir = "./data/vail/"
annotation_folder = "annotations/"
# annotation_folder = "annotations/test/"

CLASSES = ('grass', 'tree', 'pole', 'water', 'sky',
                 'vehicle', 'container generic object', 'asphalt', 'gravel',
                 'mulch', 'rockbed', 'log', 'bicycle', 'person', 'fence', 'bush',
                 'sign', 'rock', 'bridge', 'concrete', 'table', 'building', 'void',
                 'generic ground')

PALETTE = [[ 0, 102, 0 ], [ 3, 213, 5 ], [ 9, 130, 130 ], [ 0, 128, 255 ], [ 0, 0, 255 ],
            [ 255, 255, 1 ], [ 255, 0, 127 ], [ 64, 64, 64 ], [ 255, 128, 0 ],
            [ 154, 76, 0 ], [ 102, 102, 0 ], [ 102, 0, 0 ], [ 0, 255, 128 ],[ 204, 153, 255 ], [ 101, 0, 205 ], [ 255, 153, 204 ],
            [ 0, 102, 101 ], [ 153, 204, 255 ], [ 102, 255, 255 ], [ 101, 101, 11 ], [ 114, 85, 47 ], [ 66, 0, 0 ], [ 7, 39, 194 ],
            [ 187, 70, 156 ]]

Groups = [2, 5, 5, 4, 0, 
          5, 5, 1, 2, 
          2, 3, 5, 5, 5, 5, 5, 
          0, 3, 5, 1, 3, 5, 0,
          1]


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


with open(osp.join(vail_dir, 'train.txt'), 'r') as r:
    i = 0
    for l in r:
        print("train: {}".format(i))
        # w.writelines(l[:-5] + "\n")
        # w.writelines(l.split(".")[0] + "\n")
        print(l)
        if "_" in l:
            folderpath = l.split("_")[1].split(".")[0] + '/'
        else:
            folderpath = l.split(" ")[0] + "/"         
     
        file_client_args=dict(backend='disk')        
        img_or_path = vail_dir + annotation_folder + l.strip()
        file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
        img_bytes = file_client.get(img_or_path) 
        gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
        gt_semantic_seg[:, :] = gt_semantic_seg[:, :, ::-1]
        out = rgb2mask(gt_semantic_seg)
        out = out[:, :, 0]
        
        #copy file over to converted image train directory
        path = l.split("/")
        top_folder = path[0] + '/'
        img_name = path[1].strip()
        print(top_folder)
        print(img_name)
        dir = "./data/vail/converted/images/train/" 
        curDir = "./data/vail/images/"+ top_folder + img_name
        shutil.copy(curDir, dir)

        # mmcv.imwrite(out, vail_dir + annotation_folder + folderpath + "orig" + l.strip()+ "_orig.png")
        out2 = raw_to_seq(out)
        mmcv.imwrite(out2, vail_dir + "converted/annotations/train/" + img_name + "_group6.png")

        i += 1


with open(osp.join(vail_dir, 'val.txt'), 'r') as r:
    i = 0
    for l in r:
        print("val: {}".format(i))
        if "_" in l:
            folderpath = l.split("_")[1].split(".")[0] + '/'
        else:
            folderpath = l.split(" ")[0] + "/"        
        # print(folderpath)     
        # w.writelines(l[:-5] + "\n")
        # w.writelines(l.split(".")[0] + "\n")
        file_client_args=dict(backend='disk')
        img_or_path = vail_dir + annotation_folder + l.strip()
        file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
        img_bytes = file_client.get(img_or_path)
        gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
        gt_semantic_seg[:, :] = gt_semantic_seg[:, :, ::-1]
        out = rgb2mask(gt_semantic_seg)
        out = out[:, :, 0]

        #copy file over to converted image val directory
        path = l.split("/")
        top_folder = path[0] + '/'
        img_name = path[1].strip()
        print(top_folder)
        print(img_name)
        dir = "./data/vail/converted/images/val/" 
        curDir = "./data/vail/images/"+ top_folder + img_name
        shutil.copy(curDir, dir)

        out2 = raw_to_seq(out)
        mmcv.imwrite(out2, vail_dir + "converted/annotations/val/" + img_name + "_group6.png")

        i += 1



with open(osp.join(vail_dir, 'test.txt'), 'r') as r:
    i = 0
    for l in r:
        print("test: {}".format(i))        
        if "_" in l:
            folderpath = l.split("_")[1].split(".")[0] + '/'
        else:
            folderpath = l.split(" ")[0] + "/"               
            # w.writelines(l[:-5] + "\n")
        # w.writelines(l.split(".")[0] + "\n")
        # print(folderpath)     
        file_client_args=dict(backend='disk')
        img_or_path = vail_dir + annotation_folder + l.strip()
        file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
        img_bytes = file_client.get(img_or_path) 
        gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
        gt_semantic_seg[:, :] = gt_semantic_seg[:, :, ::-1]
        out = rgb2mask(gt_semantic_seg)
        out = out[:, :, 0]

        #copy file over to converted image test directory
        path = l.split("/")
        top_folder = path[0] + '/'
        img_name = path[1].strip()
        print(top_folder)
        print(img_name)
        dir = "./data/vail/converted/images/test/" 
        curDir = "./data/vail/images/"+ top_folder + img_name    
        shutil.copy(curDir, dir)

        out2 = raw_to_seq(out)
        mmcv.imwrite(out2, vail_dir + "converted/annotations/test/" + img_name + "_group6.png")

        i += 1

print("successful")
print(unknownColors)