"""Example of an analytics module that segments bright pixels."""

import numpy as np


def segment(image, threshold):
    """
    Return segmentation mask and number of bright pixels.

    :param np.ndarray image: RGB images of shape (3,w,h)
    :param int threshold: Threshold for bright pixels.
    :return: (mask, #bright_pixels)
    :rtype: tuple
    """
    mean_img = image.mean(2)
    is_bright = mean_img > threshold
    mask = np.zeros(image.shape[:2], dtype='uint8')
    mask[is_bright] = 255
    return mask, int(np.sum(is_bright))
