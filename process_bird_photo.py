#!/usr/bin/env python3
"""Create a non-generative photo banner with Pillow and NumPy.

Usage:
  python3 process_bird_photo.py /path/to/photo.ARW bird-banner.jpg

For ARW inputs, ExifTool reads the full-size camera-rendered JPEG embedded
in the RAW file. This does not demosaic or alter the sensor RAW data.
Dependencies: Pillow, NumPy; ExifTool for ARW inputs.
"""

import argparse
import io
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image, ImageCms, ImageFilter, ImageOps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--crop", type=int, nargs=4, default=(100, 1750, 4900, 3350),
                        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error("The source and output must be different files.")
    if args.source.suffix.lower() == ".arw":
        data = subprocess.run(
            ["exiftool", "-b", "-JpgFromRaw", str(args.source)],
            check=True, capture_output=True,
        ).stdout
        if not data:
            raise ValueError("No embedded full-size JPEG found in the ARW file.")
        source = Image.open(io.BytesIO(data))
    else:
        source = Image.open(args.source)
    image = ImageOps.exif_transpose(source).convert("RGB")
    left, top, right, bottom = args.crop
    if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
        parser.error("Crop rectangle is outside the source image.")
    image = image.crop((left, top, right, bottom))
    image = image.resize((2400, 800), Image.Resampling.LANCZOS)

    # All adjustments are deterministic pixel operations; no synthesis,
    # retouching, object replacement, denoising models, or generative fill.
    hsv = np.asarray(image.convert("HSV"), dtype=np.float32) / 255.0
    hue, saturation = hsv[..., 0], hsv[..., 1]
    green = np.minimum(np.clip((hue - .16) / .05, 0, 1),
                       np.clip((.55 - hue) / .07, 0, 1))
    green *= np.clip(saturation / .12, 0, 1)
    rgb = np.asarray(image, dtype=np.float32) / 255.0
    rgb *= np.array([1.018, 1.0, .989], dtype=np.float32)
    luminance = (rgb * np.array([.2126, .7152, .0722])).sum(axis=2, keepdims=True)
    rgb = luminance + (rgb - luminance) * (1.025 - .14 * green[..., None])
    rgb *= 1 - .085 * green[..., None]
    rgb = (rgb - .5) * 1.055 + .5
    rgb = np.clip(rgb, 0, 1)
    image = Image.fromarray(np.rint(rgb * 255).astype(np.uint8))
    image = image.filter(ImageFilter.UnsharpMask(radius=.8, percent=55, threshold=3))

    metadata = Image.Exif()
    metadata[315] = "Jianan Cui"
    metadata[305] = "Python / Pillow / NumPy: crop, color, contrast, unsharp mask"
    metadata[270] = "Original photograph by Jianan Cui; conventional non-generative photo adjustments."
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output, quality=91, subsampling=0, optimize=True,
               exif=metadata, icc_profile=profile)
    print(f"Saved {args.output}: {image.width} x {image.height}; crop {args.crop}")


if __name__ == "__main__":
    main()
