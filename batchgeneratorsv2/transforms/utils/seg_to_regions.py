from typing import Union, List, Tuple

import torch

from batchgeneratorsv2.transforms.base.basic_transform import SegOnlyTransform


class ConvertSegmentationToRegionsTransform(SegOnlyTransform):
    def __init__(self, regions: Union[List, Tuple], channel_in_seg: int = 0):
        super().__init__()
        self.regions = regions
        self.channel_in_seg = channel_in_seg

    def _apply_to_segmentation(self, segmentation: torch.Tensor, **params) -> torch.Tensor:
        num_regions = len(self.regions)
        region_output = torch.zeros((num_regions, *segmentation.shape[1:]), dtype=torch.bool, device=segmentation.device)
        for region_id, region_labels in enumerate(self.regions):
            region_output[:, region_id] |= np.isin(seg[:, self.seg_channel], region_labels)
        return region_output.to(segmentation.dtype)