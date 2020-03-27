import os

from PIL import Image as pimg

from philter import np_gen_hald_pixel_array, img_to_fortified, img_from_fortified, img_clut_to_cube


def cmd_gen_thald(size, scale, padding, reps, name):
    # STEP 1: Construct Image array:
    hald_pixels = np_gen_hald_pixel_array(size)
    hald_img = pimg.fromarray(hald_pixels)

    # STEP 2: Make Hald more resistant to artifacts:
    hald_img = img_to_fortified(hald_img, scale, padding, reps)

    # STEP 3: Done
    image_output_path = os.path.abspath("%s.%s.png" % (name, size))
    hald_img.save(image_output_path, format='png')
    print("GENERATED: %s" % image_output_path)


def cmd_thald_to_clut(scale, padding, reps, in_name, out_name):
    thald_img = pimg.open(in_name)

    if len(out_name) == 0:
        in_name_root, _ = os.path.splitext(in_name)
        out_name = os.path.join("%s_clut" % (in_name_root))
    elif os.path.isdir(out_name):
        in_name_root, _ = os.path.splitext(os.path.basename(in_name))
        out_name = os.path.join(out_name, "%s_clut" % in_name_root)

    image_output_path = os.path.abspath("%s.png" % out_name)
    hald_img = img_from_fortified(thald_img, scale, padding, reps, fast=False)
    hald_img.save(image_output_path, format='png')
    print("GENERATED: %s" % image_output_path)

    cubemap_output_path = os.path.abspath("%s.cube" % out_name)
    cube_str = img_clut_to_cube(hald_img)
    with open(cubemap_output_path, "w") as f:
        f.write(cube_str)
    print("GENERATED: %s" % cubemap_output_path)


def cmd_cube(in_name, out_name):
    clut_img = pimg.open(in_name)

    if len(out_name) == 0:
        in_name_root, _ = os.path.splitext(in_name)
        out_name = os.path.join("%s_clut" % (in_name_root))
    elif os.path.isdir(out_name):
        in_name_root, _ = os.path.splitext(os.path.basename(in_name))
        out_name = os.path.join(out_name, "%s_clut" % in_name_root)

    cube_str = img_clut_to_cube(clut_img)
    with open("%s.cube" % (out_name), "w") as f:
        f.write(cube_str)