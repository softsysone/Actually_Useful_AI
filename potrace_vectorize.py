import sys
import os
import potrace
from PIL import Image
import numpy as np


def jpeg_to_svg(jpeg_path: str, svg_path: str, threshold: int = 128):
    """Convert a JPEG image to an SVG using potrace."""
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
            f.write('<path d="')
            for segment in curve:
                if segment.is_corner:
                    c = segment.c
                    f.write(f'M{segment.start_point.x},{segment.start_point.y} ')
                    f.write(f'L{c.x},{c.y} ')
                else:
                    c1, c2 = segment.c1, segment.c2
                    f.write(f'M{segment.start_point.x},{segment.start_point.y} ')
                    f.write(f'C{c1.x},{c1.y} {c2.x},{c2.y} {segment.end_point.x},{segment.end_point.y} ')
            f.write('" fill="black"/>\n')
        f.write('</svg>\n')


def main():
    if len(sys.argv) < 2:
        print('Usage: python potrace_vectorize.py <input.jpeg> [output.svg]')
        sys.exit(1)
    jpeg_path = sys.argv[1]
    svg_path = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(jpeg_path)[0] + '.svg'
    jpeg_to_svg(jpeg_path, svg_path)
    print(f'SVG written to {svg_path}')


if __name__ == '__main__':
    main()
