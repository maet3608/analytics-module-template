"""
Analytics Module Template.
"""
from __future__ import print_function, absolute_import

import sys
from amod_template.module import *  # needed for resourcepath
from amod_template.specification import SPEC
from amod_template.analytics.bright_pixel_segmentation import segment
from amodule.base import Module
from amodule.util import resourcepath, create_analytics
from mmacommon.util.imageio import imagefile_to_ndarray, ndarray_to_imagefile


class Detector(Module):
    """Example detector."""

    def __init__(self, *args):
        """Constructor. Add your own parameters if needed."""
        Module.__init__(self, SPEC)
        print('additional cmdline arguments:', args)
        # Add own code here that load or create the model, e.g.
        # detector = Detector()
        # detector.load_weights(resourcepath('resources/weights.hd5'))

    def process(self, image, threshold):
        """
        Process data.

        :param ndarray image: The image to process.
        :param int threshold: Threshold for bright pixels.
        :return: (mask, #bright_pixels)
        :rtype: tuple
        """
        Module.checktype(self, 'process', 'input', image, threshold)

        # Replace with your code.
        mask, n_bright = segment(image, threshold)

        Module.checktype(self, 'process', 'output', mask, n_bright)
        return mask, n_bright


def test_module():
    """Pytest for module. Don't touch."""
    analytics = create_analytics(sys.modules[__name__])
    analytics.test()


def main_module(*argv):
    """Run from command line."""
    detector = Detector()
    print('SPEC:', detector.spec('module'))
    print('Module name:', detector.name())

    # run detector for some image
    testfile = resourcepath('testdata/image.png')
    filepath = argv[1] if len(argv) == 2 else testfile
    print('imagefile:', filepath)
    image = imagefile_to_ndarray(filepath)
    mask, n_bright = detector.process(image, 130)
    print('mask', mask)
    print('Number of bright pixels:', n_bright)
    # ndarray_to_imagefile(mask, 'mask.png')


if __name__ == "__main__":
    main_module(sys.argv)
