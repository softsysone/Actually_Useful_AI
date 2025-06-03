#!/usr/bin/env python3

"""Utility to vectorize a JPEG using the potrace library."""

import argparse
import os
import sys

from PIL import Image
import numpy as np
import potrace


def jpeg_to_svg(jpeg_path: str, svg_path: str, threshold: int = 128, *, fill: str = "black"):
    """Convert a JPEG image to an SVG using potrace.

    Parameters
    ----------
    jpeg_path: str
        Path to the source JPEG image.
    svg_path: str
        Output SVG file path.
    threshold: int, optional
        Grayscale threshold (0-255) for binarization.
    fill: str, optional
        Fill color used for the generated path.
    """
    # Load image and convert to grayscale
    image = Image.open(jpeg_path).convert('L')
    # Binarize image using threshold
    bitmap_data = np.array(image) > threshold
    bitmap = potrace.Bitmap(bitmap_data)
    path = bitmap.trace()

    # Write SVG output
    with open(svg_path, 'w') as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" ')
        f.write(f'width="{image.width}" height="{image.height}">\n')
        for curve in path:
            # Each curve represents a closed path starting at curve.start_point
            f.write('<path d="')
            # Move to the starting point of this curve
            start = curve.start_point
            f.write(f'M{start.x},{start.y} ')
            for segment in curve:
                if segment.is_corner:
                    # Corner segments specify a control point (c) and end point
                    c = segment.c
                    end = segment.end_point
                    f.write(f'L{c.x},{c.y} ')
                    f.write(f'L{end.x},{end.y} ')
                else:
                    # Bezier curve with control points c1/c2
                    c1, c2 = segment.c1, segment.c2
                    end = segment.end_point
                    f.write(f'C{c1.x},{c1.y} {c2.x},{c2.y} {end.x},{end.y} ')
            # Close the path and apply fill color
            f.write(f'Z" fill="{fill}"/>\n')
        f.write('</svg>\n')


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Convert a JPEG image to an SVG using potrace",
    )
    parser.add_argument("jpeg_path", help="Input JPEG file")
    parser.add_argument(
        "svg_path",
        nargs="?",
        help="Output SVG file (defaults to input name with .svg)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=128,
        help="Grayscale threshold used for binarization",
    )
    parser.add_argument(
        "--fill",
        default="black",
        help="Fill color for the generated path",
    )

    args = parser.parse_args()

    svg_path = args.svg_path or os.path.splitext(args.jpeg_path)[0] + ".svg"
    jpeg_to_svg(
        args.jpeg_path,
        svg_path,
        threshold=args.threshold,
        fill=args.fill,
    )
    print(f"SVG written to {svg_path}")


if __name__ == '__main__':
    main()
