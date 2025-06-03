import sys
import xml.etree.ElementTree as ET
from collections import Counter

def analyze_svg(svg_path: str) -> None:
    tree = ET.parse(svg_path)
    root = tree.getroot()
    fills = []
    images = 0
    for elem in root.iter():
        if elem.tag.endswith('path') or elem.tag.endswith('polygon'):
            fill = elem.get('fill')
            if fill:
                fills.append(fill.strip())
        if elem.tag.endswith('image'):
            images += 1
    counter = Counter(fills)
    print(f"File: {svg_path}")
    print(f"Number of <image> tags: {images}")
    print(f"Unique fill colors ({len(counter)}):")
    for color, count in counter.items():
        print(f"  {color}: {count}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python diagnose_svg.py file.svg')
        sys.exit(1)
    analyze_svg(sys.argv[1])
