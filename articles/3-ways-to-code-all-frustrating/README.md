# 3 Ways to Code Without All the Frustration

This folder contains sample utilities referenced in the corresponding article.

## Vectorizing a JPEG with colors

Use `potrace_vectorize.py` to convert `schoolsone_logo.jpeg` to an SVG while preserving colors:

```bash
python3 potrace_vectorize.py schoolsone_logo.jpeg output.svg
```

By default the script performs color quantization (up to eight colors). If you
set `--colors 1` the output will be monochrome, which may result in a black
SVG. To preserve the original colors, keep the default or specify a value
greater than 1:

```bash
python3 potrace_vectorize.py --colors 8 schoolsone_logo.jpeg colored_output.svg
```

The generated `schoolsone_logo.svg` was created with the above command and
preserves the original logo colors. The older `schoolsone_logo_color.svg` file
is kept for reference but contains the same output.
