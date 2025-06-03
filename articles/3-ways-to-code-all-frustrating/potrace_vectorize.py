#!/usr/bin/env python3

"""Utility to vectorize a JPEG using the potrace library."""

import argparse
import os
import sys

from PIL import Image
import numpy as np
import potrace


def jpeg_to_svg(
    jpeg_path: str,
    svg_path: str,
    threshold: int = 128,
    *,
    fill: str | None = None,
    colors: int = 8,
):
    """Convert a JPEG image to an SVG using potrace.

    Parameters
    ----------
    jpeg_path: str
        Path to the source JPEG image.
    svg_path: str
        Output SVG file path.
    threshold: int, optional
        Grayscale threshold (0-255) for binarization.
    fill: str | None, optional
        Fill color used for monochrome output. If ``None`` and ``colors`` is
        greater than 1, the image colors are preserved via quantization.
    """
    image = Image.open(jpeg_path).convert("RGB")

    with open(svg_path, "w") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" ')
        f.write(f'width="{image.width}" height="{image.height}">\n')

        if colors and colors > 1:
            # Quantize image to the requested number of colors
            quantized = image.convert("P", palette=Image.Palette.ADAPTIVE, colors=colors)
            palette = quantized.getpalette()[: colors * 3]
            data = np.array(quantized)

            for idx in range(colors):
                mask = data == idx
                if not mask.any():
                    continue
                bitmap = potrace.Bitmap(mask)
                path = bitmap.trace()
                color = "#%02x%02x%02x" % tuple(palette[idx * 3 : idx * 3 + 3])

                for curve in path:
                    f.write('<path d="')
                    start = curve.start_point
                    f.write(f'M{start.x},{start.y} ')
                    for segment in curve:
                        if segment.is_corner:
                            c = segment.c
                            end = segment.end_point
                            f.write(f'L{c.x},{c.y} ')
                            f.write(f'L{end.x},{end.y} ')
                        else:
                            c1, c2 = segment.c1, segment.c2
                            end = segment.end_point
                            f.write(
                                f'C{c1.x},{c1.y} {c2.x},{c2.y} {end.x},{end.y} '
                            )
                    f.write(f'Z" fill="{color}"/>\n')
        else:
            # Monochrome conversion
            gray = image.convert("L")
            bitmap_data = np.array(gray) > threshold
            bitmap = potrace.Bitmap(bitmap_data)
            path = bitmap.trace()

            for curve in path:
                f.write('<path d="')
                start = curve.start_point
                f.write(f'M{start.x},{start.y} ')
                for segment in curve:
                    if segment.is_corner:
                        c = segment.c
                        end = segment.end_point
                        f.write(f'L{c.x},{c.y} ')
                        f.write(f'L{end.x},{end.y} ')
                    else:
                        c1, c2 = segment.c1, segment.c2
                        end = segment.end_point
                        f.write(
                            f'C{c1.x},{c1.y} {c2.x},{c2.y} {end.x},{end.y} '
                        )
                f.write(f'Z" fill="{fill or "black"}"/>\n')

        f.write("</svg>\n")


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
        default=None,
        help="Fill color for monochrome output",
    )
    parser.add_argument(
        "--colors",
        type=int,
        default=8,
        help=(
            "Number of colors to preserve. If >1, performs color vectorization."
        ),
    )

    args = parser.parse_args()

    svg_path = args.svg_path or os.path.splitext(args.jpeg_path)[0] + ".svg"
    jpeg_to_svg(
        args.jpeg_path,
        svg_path,
        threshold=args.threshold,
        fill=args.fill,
        colors=args.colors,
    )
    print(f"SVG written to {svg_path}")


if __name__ == '__main__':
    main()
