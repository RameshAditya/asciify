import sys
from PIL import Image

ASCII_CHARS = "@#S%?*+;:,."

def to_ascii(original, output_width):
    (original_width, original_height) = original.size
    output_height = output_width * original_height // original_width
    resized_grayscale = original.resize((output_width, output_height)).convert('L')
    chars = [ASCII_CHARS[lum * len(ASCII_CHARS) // 256] for lum in list(resized_grayscale.getdata())]
    rows = [[chars[y * output_width + x] for x in range(output_width)] for y in range(output_height)]
    return '\r\n'.join([''.join(row) for row in rows])

if __name__ == '__main__':
    print(to_ascii(Image.open(sys.argv[1]), 100))
