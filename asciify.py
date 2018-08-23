import sys
from PIL import Image

ASCII_CHARS = "@#S%?*+;:,."

def main(path, output_width):
    image = Image.open(path)
    (old_width, old_height) = image.size
    output_height = output_width * old_height // old_width
    resized_grayscale = image.resize((output_width, output_height)).convert('L')
    chars = [ASCII_CHARS[lum * len(ASCII_CHARS) // 256] for lum in list(resized_grayscale.getdata())]
    rows = [[chars[y * output_width + x] for x in range(output_width)] for y in range(output_height)]
    print('\r\n'.join([''.join(row) for row in rows]))

if __name__ == '__main__':
    path = sys.argv[1]
    main(path, 100)
