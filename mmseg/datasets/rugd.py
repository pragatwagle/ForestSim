from mmseg.registry import DATASETS
from .basesegdataset import BaseSegDataset


@DATASETS.register_module()
class RUGDDataset(BaseSegDataset):
    
    """RUGD dataset.

    """
    METAINFO = dict(
        classes=("grass", "tree", "pole", "water", "sky", \
                "vehicle", "container/generic-object", "asphalt", "gravel", \
                "mulch", "rock-bed", "log", "bicycle", "person", "fence", "bush", \
                "sign", "rock", "bridge", "concrete", "table", "building", \
                'void', 'generic ground'),
        palette=[[0, 102, 0],[3, 213, 5], [9, 130, 130],[0, 128, 255],[0, 0, 255], \
                 [255, 255, 1],[255, 0, 127], [64, 64, 64],[255, 128, 0], \
                 [154, 76, 0],[102, 102, 0],[102, 0, 0],[0, 255, 128],[204, 153, 255], [101, 0, 205],[255, 153, 204], \
                 [0, 102, 101],[153, 204, 255],[102, 255, 255],[101, 101, 11],[114, 85, 47], [66, 0, 0], \
                 [7, 39, 194 ], [187, 70, 156]] )

    def __init__(self,
                 img_suffix='.png',
                 seg_map_suffix='.png',
                 **kwargs) -> None:
        super().__init__(
            img_suffix=img_suffix, seg_map_suffix=seg_map_suffix, **kwargs)

# METAINFO = dict(
#         classes=("background", "L1 (Smooth)", "L2 (Rough)", "L3 (Bumpy)", "non-Nav (Forbidden)", "obstacle"),
#         palette=[[108, 64, 20], [255, 229, 204],[0, 102, 0],[0, 255, 0],
#             [0, 153, 153],[0, 128, 255]])

#     def __init__(self,
#             img_suffix='.png',
#             seg_map_suffix='_group6.png',
#             **kwargs) -> None:
#         super().__init__(
#             img_suffix=img_suffix, seg_map_suffix=seg_map_suffix, **kwargs)


        
        
