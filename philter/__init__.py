#!/bin/env python
import sys
import os
import math
import argparse

import numpy as np
import PIL.Image as pimg
import PIL.ImageDraw as pimg_d


def img_clut_to_cube(hald_img: pimg.Image):
    size = int(round(math.pow(hald_img.width, 1/3)))

    lines = list()

    lines.append('LUT_3D_SIZE %d' % (size ** 2))
    lines.append('DOMAIN_MIN 0.0 0.0 0.0')
    lines.append('DOMAIN_MAX 1.0 1.0 1.0')

    for pixel in hald_img.getdata():
        r, g, b = pixel[:3]
        lines.append('%f %f %f' % (r / 255.0, g / 255.0, b / 255.0))

    return "\n".join(lines)


def img_to_fortified(hald_img: pimg.Image, scale: int, padding: float, reps: int):
    """
        Increase the size so that hald image is less resistant to artifacts.
        TODO: write encoded parameter information.
    """

    size = hald_img.width
    sample_size = int(round(math.pow(size, 1/3), 2))

    scale = max(1, scale)

    new_size = int(size*scale)
    padding_size = max(0, int(new_size*padding))

    hald_img = hald_img.resize([new_size, new_size])
    padded_size = int(new_size * reps + padding_size * 2)

    output_hald = pimg.new('RGB', [padded_size, padded_size], 'grey')

    # Repeat the hald_image in a grid pattern.
    for i in range(0, reps):
        for j in range(0, reps):
            output_hald.paste(hald_img, [padding_size+new_size*i, padding_size+new_size*j])

    # Record parameter information in text form.
    img_draw = pimg_d.Draw(output_hald)
    img_draw.text(
        [10, 10],
        "size: %d, scale: %d, padding: %f, reps: %d" % (sample_size, scale, padding, reps),
        fill=(255, 255, 255, 255)
    )

    return output_hald


def img_from_fortified(thald_img: pimg.Image, scale: int, padding: float, reps: int, fast: bool):
    """
        Deduce the original hald image.
        TODO: read encoded parameter information.
    """

    # STEP 1: Find out cropped size.
    padded_size = thald_img.width
    unpadded_size = (reps * padded_size) / (reps + padding * 2)
    padding_size = int((padded_size - unpadded_size) / 2)

    # STEP 2: Crop out the padding.
    thald_img = thald_img.crop([
        padding_size,
        padding_size,

        padded_size - padding_size,
        padded_size - padding_size
    ])

    # STEP 3: Find the hald quads.
    thald_pix = np.array(thald_img)

    quads = []
    quad_size = int(unpadded_size / reps)
    for i in range(reps):
        for j in range(reps):
            qs = quad_size
            quads.append(thald_pix[
                         (qs * i): (qs * (i + 1)),
                         (qs * j): (qs * (j + 1)),
                         ])

    if fast:
        # (
        #  This process produces less accurate results if the compression artifacts
        #  are heavy. But is faster if that is not a concern, like when working
        #  with an uncompressed image.
        # )

        # STEP 4: Create a median of quads.
        hald_median_pix = np.median(
            np.stack(quads, axis=-1),
            axis=-1
        ).astype(np.uint8)
        hald_img = pimg.fromarray(np.asarray(hald_median_pix))

        # STEP 5: Resize the image using PILlow.
        new_size = int(hald_img.width / scale)
        hald_img = hald_img.resize([new_size, new_size], pimg.BOX)

        return hald_img
    else:
        # (
        #  This process produces a slightly more accurate results for colours on
        #  the borders of the hald image. It takes an average over all
        #  occurences of the given 'mega-pixel' (enlarged by scale pixel), then
        #  breaks those into an array of color values, and uses an overall mean
        #  of those values.
        #
        #  If desired this might be extended to take a mean of values within the
        #  first standard deviation.
        # )

        # STEP 4: Find out original size and enlarged pixel size.
        quads = np.array(quads).astype(np.uint8)
        quad_size = len(quads[0])
        original_size = int(quad_size / scale)
        single_pixel_size = int(quad_size / original_size)

        # STEP 5: Iterate over enlarged pixels and find the mode of their color values.
        avg_hald_pix = np.array([]).astype(np.uint8)
        for i in range(0, original_size):
            for j in range(0, original_size):
                s = int(single_pixel_size)
                pixel_versions = quads[
                                 :,
                                 i*s:(i+1)*s,
                                 j*s:(j+1)*s,
                                 ]

                pxm = np.median(np.reshape(pixel_versions, (-1, 3)), axis=0).astype(np.uint8)
                avg_hald_pix = np.append(avg_hald_pix, pxm)

        # STEP 6: Reshape int the final unfortified hald array.
        hald_pix = np.reshape(avg_hald_pix, (original_size,original_size,3))
        hald_img = pimg.fromarray(np.asarray(hald_pix))

        return hald_img


def np_gen_hald_pixel_array(size: int):
    """
    Generates a proper idendity HALD image array, which can be converted to CUBE
    map.

    :param size: Sample size of the HALD image. (i.e.
    :return:
    """
    # Create a mesh grid for RGB values with size^2 steps:
    mg = np.mgrid[
         0:255:size**2*1j,
         0:255:size**2*1j,
         0:255:size**2*1j,
         ].astype(np.uint8)

    # Split mesh grid into components:
    gC, bC, rC = mg

    # Recombine components and stack them so that we get all possible color combinations:
    # (Use last axis to get all combinations of components.)
    rgbStack = np.stack([rC, bC, gC], axis=-1)

    # Reshape the components so that they are a proper square matrix of color values.
    haldPixels = np.reshape(rgbStack, (size**3, size**3, 3))

    return np.asarray(haldPixels)