#!/usr/bin/env python3

import os
import sys
import fileinput
from PIL import Image, ImageOps

def append_suffix(filename, suffix):
    name, ext = os.path.splitext(filename)
    return "{name}_{suffix}{ext}".format(name=name, suffix=suffix, ext=ext)

def slice_photo(file_path):
    # Load image and get size
    orig_image = Image.open(file_path)
    im = ImageOps.exif_transpose(orig_image) # requires Pillow>=6.0.0

    width, height = im.size
    short = min(width, height)
    long = max(width, height)

    # Calculate crop dimensions (assuming vertical image)
    top_box = (0, 0, short, short)
    center_box = (0, (long-short)/2, short, ((long-short)/2)+short)
    bottom_box = (0, long-short, short, long)

    target_size = (512, 512)

    # Crop the image into three slices and rescale them
    top_im = im.crop(top_box).resize(target_size)
    center_im = im.crop(center_box).resize(target_size)
    bottom_im = im.crop(bottom_box).resize(target_size)

    # Create paths
    base_n = os.path.basename(file_path)
    base_d = os.path.dirname(file_path)
    crop_d = "{}/crop".format(base_d)
    os.makedirs(crop_d, exist_ok=True)

    # Save images
    top_im.save("{}/{}".format(crop_d, append_suffix(base_n, "t")))
    center_im.save("{}/{}".format(crop_d, append_suffix(base_n, "c")))
    bottom_im.save("{}/{}".format(crop_d, append_suffix(base_n, "b")))

    print("[ OK ]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: {} file(s)".format(sys.argv[0]))
        exit(1)

    for filepath in sys.argv[1:]:
        print("Processing {} ...".format(filepath), end = '')
        slice_photo(filepath)
