import argparse
import os.path as osp
import numpy as np
import mmcv
# import cv2
from PIL import Image
import mmengine.fileio as fileio
import shutil


rellis_dir = "./data/rellis/"
annotation_folder = "annotation/"
label_folder = "pylon_camera_node_label_id/"
outDir =  "./data/rellis/converted/"

IDs =    [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 17, 18, 19, 23, 27, 31, 33, 34]
Groups = [0, 2, 2, 5, 5, 4, 0, 5, 5, 1, 5, 5, 5, 5, 4, 1, 5, 4, 3, 3]

ID_seq = {}
ID_group = {}
for n, label in enumerate(IDs):
    ID_seq[label] = n
    ID_group[label] = Groups[n]

# 0 -- Background: void, sky, sign
# 1 -- Level1 (smooth) - Navigable: concrete, asphalt
# 2 -- Level2 (rough) - Navigable: gravel, grass, dirt, sand, mulch
# 3 -- Level3 (bumpy) - Navigable: Rock, Rock-bed
# 4 -- Non-Navigable (forbidden) - water
# 5 -- Obstacle - tree, pole, vehicle, container/generic-object, building, log, 
#                 bicycle(could be removed), person, fence, bush, picnic-table, bridge,

CLASSES = ("void", "dirt", "grass", "tree", "pole", "water", "sky", "vehicle", 
            "object", "asphalt", "building", "log", "person", "fence", "bush", 
            "concrete", "barrier", "puddle", "mud", "rubble")

PALETTE = [[0, 0, 0], [108, 64, 20], [0, 102, 0], [0, 255, 0], [0, 153, 153], 
            [0, 128, 255], [0, 0, 255], [255, 255, 0], [255, 0, 127], [64, 64, 64], 
            [255, 0, 0], [102, 0, 0], [204, 153, 255], [102, 0, 204], [255, 153, 204], 
            [170, 170, 170], [41, 121, 255], [134, 255, 239], [99, 66, 34], [110, 22, 138]]


def raw_to_seq(seg):
    h, w = seg.shape
    out1 = np.zeros((h, w))
    out2 = np.zeros((h, w))
    for i in IDs:
        out1[seg==i] = ID_seq[i]
        out2[seg==i] = ID_group[i]

    return out1, out2




with open(osp.join(rellis_dir, 'train.txt'), 'r') as r:
    i = 0
    for l in r:
        print("train: {}".format(i))
        # w.writelines(l[:-5] + "\n")
        # w.writelines(l.split(".")[0] + "\n")
        file_client_args=dict(backend='disk')
        path = l.split("/")
        top_folder = path[0] + '/'
        img_name = path[1].strip()
        print(img_name)
        img_or_path = rellis_dir + annotation_folder + top_folder + label_folder + img_name.strip() + '.png'
        file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
        img_bytes = file_client.get(img_or_path) 
        gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
        out1, out2 = raw_to_seq(gt_semantic_seg)
        # find same file but of image and copy to train image
        dir = "./data/rellis/converted/images/train/" 
        curDir = "./data/rellis/image/" + top_folder + "pylon_camera_node" + "/" + img_name + ".jpg"
        shutil.copy(curDir, dir)

        # mmcv.imwrite(out1, rellis_dir + annotation_folder + l.strip() + "_orig.png")
        # mmcv.imwrite(out2, rellis_dir + annotation_folder + l.strip() + "_group6.png")
        mmcv.imwrite(out2, rellis_dir + "/converted/annotations/train/" + img_name + "_group6.png")
        i += 1


with open(osp.join(rellis_dir, 'val.txt'), 'r') as r:
    i = 0
    for l in r:
        print("val: {}".format(i))
        # w.writelines(l[:-5] + "\n")
        # w.writelines(l.split(".")[0] + "\n")
        file_client_args=dict(backend='disk')
        path = l.split("/")
        top_folder = path[0] + '/'
        img_name = path[1].strip()
        img_or_path = rellis_dir + annotation_folder + top_folder + label_folder + img_name.strip() + '.png'
        file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
        img_bytes = file_client.get(img_or_path) 
        gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
        out1, out2 = raw_to_seq(gt_semantic_seg)
        # find same file but of image and copy to val image
        dir = "./data/rellis/converted/images/val/" 
        curDir = "./data/rellis/image/" + top_folder + "pylon_camera_node" + "/" + img_name + ".jpg"
        shutil.copy(curDir, dir)
        # mmcv.imwrite(out1, rellis_dir + annotation_folder + l.strip() + "_orig.png")
        # mmcv.imwrite(out2, rellis_dir + annotation_folder + l.strip() + "_group6.png")
        mmcv.imwrite(out2, rellis_dir + "/converted/annotations/val/" + img_name + "_group6.png")
        i += 1



with open(osp.join(rellis_dir, 'test.txt'), 'r') as r:
    i = 0
    for l in r:
        print("test: {}".format(i))
        # w.writelines(l[:-5] + "\n")
        # w.writelines(l.split(".")[0] + "\n")
        file_client_args=dict(backend='disk')
        path = l.split("/")
        top_folder = path[0] + '/'
        img_name = path[1].strip()
        img_or_path = rellis_dir + annotation_folder + top_folder + label_folder + img_name.strip() + '.png'
        file_client = fileio.FileClient.infer_client(file_client_args, img_or_path)
        img_bytes = file_client.get(img_or_path) 
        gt_semantic_seg = mmcv.imfrombytes(img_bytes, flag='unchanged', backend='pillow').squeeze().astype(np.uint8)
        out1, out2 = raw_to_seq(gt_semantic_seg)

        # find same file but of image and copy to val image
        dir = "./data/rellis/converted/images/test/" 
        curDir = "./data/rellis/image/" + top_folder + "pylon_camera_node" + "/" + img_name + ".jpg"
        shutil.copy(curDir, dir)

        # mmcv.imwrite(out1, rellis_dir + annotation_folder + l.strip() + "_orig.png")
        # mmcv.imwrite(out2, rellis_dir + annotation_folder + l.strip() + "_group6.png")
        mmcv.imwrite(out2, rellis_dir + "/converted/annotations/test/" + img_name + "_group6.png")

        i += 1




print("successful")