from mmseg.registry import DATASETS
from .basesegdataset import BaseSegDataset


@DATASETS.register_module()
class MixedDataset(BaseSegDataset):
    
    """ForestSim and Rugd dataset mixed.

    """
    METAINFO = dict(
        classes=('grass', 'tree', 'pole', 'water', 'sky', \
                 'vehicle', 'container generic object', 'asphalt', 'gravel', \
                 'mulch', 'rockbed', 'log', 'bicycle', 'person', 'fence', 'bush', \
                 'sign', 'rock', 'bridge', 'concrete', 'table', 'building', 'void', \
                 'generic ground'),
        palette=[[0, 102, 0], [3, 213, 5], [9, 130, 130], [0, 128, 255], [0, 0, 255], \
                 [255, 255, 1], [255, 0, 127], [64, 64, 64], [255, 128, 0], \
                 [154, 76, 0], [102, 102, 0], [102, 0, 0], [0, 255, 128],[204, 153, 255], [101, 0, 205], [255, 153, 204], \
                 [0, 102, 101], [153, 204, 255], [102, 255, 255], [101, 101, 11], [114, 85, 47], [66, 0, 0], [7, 39, 194], \
                 [187, 70, 156]])

    def __init__(self,
                 img_suffix='.png',
                 seg_map_suffix='.png',
                 **kwargs) -> None:
        super().__init__(
            img_suffix=img_suffix, seg_map_suffix=seg_map_suffix, **kwargs)
