from collections import Counter
import numpy as np


def color_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))


def top_most_colors(img, n=10, threshold=50):
    img.convert("RGB")
    colors = list(img.getdata())
    count_colors = Counter(colors)

    unique_colors = {}
    c = 0
    for color, count in count_colors.most_common():
        is_similar = False
        for unique_color in unique_colors:
            if color_distance(color, unique_color) < threshold:
                is_similar = True
                break
        if not is_similar:
            hex_code = '#%02x%02x%02x' % color
            unique_colors[color] = [hex_code, count]
            c += count
        if len(unique_colors) >= n:
            break

    return unique_colors, c

