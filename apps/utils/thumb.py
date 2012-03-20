# -*- coding: utf-8 -*-

from PIL import Image, ImageColor


# for png thumbs only!
def colorspace(im, requested_size, opts):
    if 'bw' in opts and im.mode != "L":
        im = im.convert("RGBA")
        im = im.convert("LA")
    elif im.mode not in ("L", "RGB", "RGBA"):
        im = im.convert("RGBA")
    return im
colorspace.valid_options = ('bw',)
