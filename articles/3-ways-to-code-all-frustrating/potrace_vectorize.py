import sys
import os
import potrace
from PIL import Image
import numpy as np


def jpeg_to_svg(jpeg_path: str, svg_path: str, colors: int = 8, threshold: int = 128):
    """Convert a JPEG image to a colored SVG using potrace."""
    image = Image.open(jpeg_path).convert('RGB')

    # Quantize the image to a limited set of colors so that each color can be traced separately.
    quantized = image.convert('P', palette=Image.ADAPTIVE, colors=colors)
    palette = quantized.getpalette()
    color_map = [tuple(palette[i:i+3]) for i in range(0, len(palette), 3)]
    index_data = np.array(quantized)

    # Write SVG output
    with open(svg_path, 'w') as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" ')
        f.write(f'width="{image.width}" height="{image.height}">\n')

        # Trace each color separately
        for index in sorted(np.unique(index_data)):
            if index >= colors:
                continue
            mask = index_data == index
            bitmap = potrace.Bitmap(mask)
            path = bitmap.trace()
            rgb = color_map[index]
            fill = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

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
                        f.write(f'C{c1.x},{c1.y} {c2.x},{c2.y} {end.x},{end.y} ')
                f.write(f'Z" fill="{fill}"/>\n')

        f.write('</svg>\n')


def main():
    if len(sys.argv) < 2:
        print('Usage: python potrace_vectorize.py <input.jpeg> [output.svg] [num_colors]')
        sys.exit(1)

    jpeg_path = sys.argv[1]
    svg_path = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(jpeg_path)[0] + '.svg'
    num_colors = int(sys.argv[3]) if len(sys.argv) > 3 else 8

    jpeg_to_svg(jpeg_path, svg_path, colors=num_colors)
    print(f'SVG written to {svg_path}')


if __name__ == '__main__':
    main()
