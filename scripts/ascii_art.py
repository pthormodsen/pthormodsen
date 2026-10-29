"""Convert a profile picture into the ASCII art used in the profile card.

Run manually when the picture changes (needs Pillow):

    pip install Pillow
    python scripts/ascii_art.py cutout.png --crop 85,0,395,410 > ascii.txt

The input should be a PNG with a transparent background; transparent
pixels become spaces. Characters are chosen for a dark background
(brighter pixel = denser character). today.py inverts the ramp for the
light-mode card.
"""

import argparse
import sys

from PIL import Image, ImageFilter, ImageOps

# Must match RAMP in today.py
RAMP = ".'`-:;~=+*xo%#&@"
CHAR_ASPECT = 0.48  # character width / line height in the SVG (6.6px / 13.75px)
GAMMA = 0.7  # < 1 lifts dark areas (hair, sweater) so they don't flatten out


def convert(path, cols, rows, crop=None):
    img = Image.open(path).convert("RGBA")
    if crop:
        img = img.crop(crop)
    img = img.crop(img.getchannel("A").getbbox())

    # Pad (centered horizontally, anchored to the bottom) to the aspect ratio
    # of the character grid so the picture isn't stretched
    target = cols * CHAR_ASPECT / rows
    w, h = img.size
    if w / h < target:
        new_w, new_h = round(h * target), h
    else:
        new_w, new_h = w, round(w / target)
    canvas = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    canvas.paste(img, ((new_w - w) // 2, new_h - h))

    # Sharpen before downscaling to keep facial features visible
    gray = ImageOps.grayscale(canvas).filter(ImageFilter.UnsharpMask(radius=4, percent=200, threshold=0))
    gray = gray.resize((cols, rows), Image.LANCZOS)
    alpha = canvas.getchannel("A").resize((cols, rows), Image.LANCZOS)

    # Stretch contrast between the 2nd and 98th percentile of the opaque pixels
    opaque = sorted(gray.getpixel((x, y)) for y in range(rows) for x in range(cols) if alpha.getpixel((x, y)) > 128)
    lo, hi = opaque[len(opaque) * 2 // 100], opaque[len(opaque) * 98 // 100]

    def char(x, y):
        if alpha.getpixel((x, y)) <= 128:
            return " "
        v = min(max((gray.getpixel((x, y)) - lo) / (hi - lo), 0), 1) ** GAMMA
        return RAMP[min(int(v * len(RAMP)), len(RAMP) - 1)]

    return "\n".join("".join(char(x, y) for x in range(cols)).rstrip() for y in range(rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("image")
    parser.add_argument("--cols", type=int, default=58)
    parser.add_argument("--rows", type=int, default=32)
    parser.add_argument("--crop", type=lambda s: tuple(map(int, s.split(","))), metavar="LEFT,TOP,RIGHT,BOTTOM",
                        help="crop the input (in pixels) before converting, e.g. to zoom in on the face")
    args = parser.parse_args()
    sys.stdout.write(convert(args.image, args.cols, args.rows, args.crop) + "\n")


if __name__ == "__main__":
    main()
