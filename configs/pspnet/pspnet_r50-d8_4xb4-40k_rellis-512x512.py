_base_ = [
    '../_base_/models/pspnet_r50-d8.py', '../_base_/datasets/rellis_group6.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_40k.py'
]
#_base_ = [
#    'C:/Users/praga/OneDrive/Desktop/mmsegmentation/configs/_base_/models/pspnet_r50-d8.py', 'C:/Users/praga/OneDrive/Desktop/mmsegmentation/configs/_base_/datasets/rellis_group6.py',
#    'C:/Users/praga/OneDrive/Desktop/mmsegmentation/configs/_base_/default_runtime.py', 'C:/Users/praga/OneDrive/Desktop/mmsegmentation/configs/_base_/schedules/schedule_40k.py'
#]

crop_size = (512, 512)
data_preprocessor = dict(size=crop_size)
model = dict(
    data_preprocessor=data_preprocessor,
    decode_head=dict(num_classes=171),
    auxiliary_head=dict(num_classes=171))
