# PHILTER

CLUT/HALD image generation and processing toolkit.

(Based on imlementation of [@homm](https://github.com/homm/color-filters-reconstruction) with some usability and accuracy improvements.)

- - - - - - - - - - - 

```
usage: philter [cmd]

A CLI toolkit for creating LUTs

subcommands:

    gen            Generate a fotified identity THALD image (somewhat immune
                   to compression artifacts) which can be used to capture
                   color transformations.

    clut           Generate CLUT image and CUBE map file from a fortified
                   THALD image.

    cube           Generate CUBE file from a NON fortified HALD image.
```
