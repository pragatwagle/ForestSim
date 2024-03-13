import argparse
import os.path as osp
import numpy as np
import mmcv
# import cv2
from PIL import Image
import mmengine.fileio as fileio
import shutil

rugd_dir = "./data/rugd/"
annotation_folder = "RUGD_annotations/"

#remove group_all from images
CLASSES = ("dirt", "sand", 
           "grass", "tree", "pole", "water", "sky", 
        "vehicle", "container/generic-object", "asphalt", "gravel", 
        "building", "mulch", "rock-bed", "log", "bicycle", "person", 
        "fence", "bush", "sign", "rock", "bridge", "concrete", "table" 'void')

PALETTE = [ [ 108, 64, 20 ], [ 255, 229, 204 ],
            [ 0, 102, 0 ],[ 0, 255, 0 ], [ 0, 153, 153 ],[ 0, 128, 255 ], [ 0, 0, 255 ],
            [ 255, 255, 0 ],[ 255, 0, 127 ], [ 64, 64, 64 ], [ 255, 128, 0 ],
            [ 255, 0, 0 ],[ 153, 76, 0 ],[ 102, 102, 0 ], [ 102, 0, 0 ],[ 0, 255, 128 ],[ 204, 153, 255 ]
            [ 102, 0, 204 ],[ 255, 153, 204 ], [ 0, 102, 102 ], [ 153, 204, 255 ],[ 102, 255, 255 ],[ 101, 101, 11 ],[ 114, 85, 47 ], [ 7, 39, 194 ]
          ]

Groups = [23, 23,
          0, 1, 2, 3, 4,
          5, 6, 7, 8, 
          21, 9, 10, 11, 12, 13, 
          14, 15, 16, 17, 18, 19, 20, 22]


# 0 -- Background: void, sky, sign
# 1 -- Level1 (smooth) - Navigable: concrete, asphalt
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
            if tuple(img[i, j]) in color_id:
                out[i][j] = color_id[tuple(img[i, j])]
            else:
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


# with open(osp.join(rugd_dir, 'train_ours.txt'), 'r') as r:
#     i = 0
#     for l in r:
#         print("train: {}".format(i))
#         # w.writelines(l[:-5] + "\n")
#         # w.writelines(l.split(".")[0] + "\n")
#         path = l.split("/")
#         top_folder = path[0] + '/'
#         img_name = path[1].strip()
#         print(top_folder)
#         print(img_name)
#         file_client_args=dict(backend='disk')
#         img_or_path = rugd_dir + annotation_folder + l.strip()
#         file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
#         img_bytes = file_client.get(img_or_path) 
#         gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
#         gt_semantic_seg[:, :] = gt_semantic_seg[:, :, ::-1]
#         out = rgb2mask(gt_semantic_seg)
#         out = out[:, :, 0]
        
#         #copy file over to converted_one_dim image train directory
#         path = l.split("/")
#         top_folder = path[0] + '/'
#         img_name = path[1].strip()
#         dir = "./data/rugd/converted_one_dim/images/train/" 
#         curDir = "./data/rugd/RUGD_frames-with-annotations/" + top_folder + img_name
#         shutil.copy(curDir, dir)

#         # mmcv.imwrite(out, rugd_dir + annotation_folder + l.strip()+ "_orig.png")
#         out2 = raw_to_seq(out)
#         mmcv.imwrite(out2, rugd_dir + "converted_one_dim/annotations/train/" + img_name + ".png")

#         i += 1


# with open(osp.join(rugd_dir, 'val_ours.txt'), 'r') as r:
#     i = 0
#     for l in r:
#         print("val: {}".format(i))
#         # w.writelines(l[:-5] + "\n")
#         # w.writelines(l.split(".")[0] + "\n")
#         file_client_args=dict(backend='disk')
#         img_or_path = rugd_dir + annotation_folder + l.strip()
#         file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
#         img_bytes = file_client.get(img_or_path) 
#         gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
#         gt_semantic_seg[:, :] = gt_semantic_seg[:, :, ::-1]
#         out = rgb2mask(gt_semantic_seg)
#         out = out[:, :, 0]
        
#         #copy file over to converted_one_dim image test directory
#         path = l.split("/")
#         top_folder = path[0] + '/'
#         img_name = path[1].strip()
#         print(top_folder)
#         print(img_name)

#         dir = "./data/rugd/converted_one_dim/images/val/" 
#         curDir = "./data/rugd/RUGD_frames-with-annotations/" + top_folder + img_name
#         shutil.copy(curDir, dir)
        
#         # mmcv.imwrite(out, rugd_dir + annotation_folder + l.strip()+ "_orig.png")
#         out2 = raw_to_seq(out)
#         mmcv.imwrite(out2, rugd_dir + "converted_one_dim/annotations/val/" + img_name + ".png")

#         i += 1



with open(osp.join(rugd_dir, 'test_ours.txt'), 'r') as r:
    i = 0
    for l in r:
        print("test: {}".format(i))        
        
        path = l.split("/")
        top_folder = path[0] + '/'
        img_name = path[1].strip()
        # w.writelines(l[:-5] + "\n")
        # w.writelines(l.split(".")[0] + "\n")
        file_client_args=dict(backend='disk')
        img_or_path = rugd_dir + annotation_folder + l.strip()
        file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
        img_bytes = file_client.get(img_or_path) 
        gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
        gt_semantic_seg[:, :] = gt_semantic_seg[:, :, ::-1]
        out = rgb2mask(gt_semantic_seg)
        out = out[:, :, 0]

        #copy file over to converted_one_dim image test directory
        path = l.split("/")
        top_folder = path[0] + '/'
        img_name = path[1].strip()
        print(top_folder)
        print(img_name)
        
        dir = "./data/rugd/converted_one_dim/images/test/" 
        curDir = "./data/rugd/RUGD_frames-with-annotations/" + top_folder + img_name
        shutil.copy(curDir, dir)

        # mmcv.imwrite(out, rugd_dir + annotation_folder + l.strip()+ "_orig.png")
        out2 = raw_to_seq(out)
        mmcv.imwrite(out2, rugd_dir + "converted_one_dim/annotations/test/" + img_name + ".png")

        i += 1

print("successful")