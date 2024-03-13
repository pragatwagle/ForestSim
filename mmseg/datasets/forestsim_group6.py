from mmseg.registry import DATASETS
from .basesegdataset import BaseSegDataset


@DATASETS.register_module()
class ForestSimDataset_Group6(BaseSegDataset):
    
    """ForestSim dataset.

    """
    METAINFO = dict(
        classes=("background", "L1 (Smooth)", "L2 (Rough)", "L3 (Bumpy)", "non-Nav (Forbidden)", "obstacle"),
        palette=[[108, 64, 20], [255, 229, 204],[0, 102, 0],[0, 255, 0],
           [0, 153, 153],[0, 128, 255]])

    def __init__(self,
                 img_suffix='.png',
                 seg_map_suffix='.png_group6.png',
                 **kwargs) -> None:
        super().__init__(
            img_suffix=img_suffix, seg_map_suffix=seg_map_suffix, **kwargs)