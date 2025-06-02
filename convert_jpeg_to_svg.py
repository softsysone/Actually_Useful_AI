import base64
import os
import sys


def get_jpeg_dimensions(data: bytes):
    """Extract width and height from JPEG binary data."""
    # Skip first two bytes (SOI marker)
    idx = 2
    while idx < len(data):
        if data[idx] != 0xFF:
            idx += 1
            continue
        marker = data[idx + 1]
        idx += 2
        # skip padding bytes
        while marker == 0xFF:
            marker = data[idx]
            idx += 1
        if marker in (0xD9, 0xDA):  # EOI or SOS
            break
        length = data[idx] << 8 | data[idx + 1]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height = data[idx + 3] << 8 | data[idx + 4]
            width = data[idx + 5] << 8 | data[idx + 6]
            return width, height
        idx += length
    raise ValueError("Could not determine JPEG dimensions")


def jpeg_to_svg(jpeg_path: str, svg_path: str):
    with open(jpeg_path, 'rb') as f:
        data = f.read()
    width, height = get_jpeg_dimensions(data)
    encoded = base64.b64encode(data).decode('ascii')
    with open(svg_path, 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
        f.write(f'  <image href="data:image/jpeg;base64,{encoded}" width="{width}" height="{height}"/>\n')
        f.write('</svg>\n')


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_jpeg_to_svg.py <input.jpeg> [output.svg]")
        return
    jpeg_path = sys.argv[1]
    svg_path = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(jpeg_path)[0] + '.svg'
    jpeg_to_svg(jpeg_path, svg_path)
    print(f'SVG written to {svg_path}')


if __name__ == '__main__':
    main()
