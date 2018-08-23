import sys
from PIL import Image

def to_ascii(original_image, output_width=100, char_lut="@#S%?*+;:,."):
    (original_width, original_height) = original_image.size
    output_height = output_width * original_height // original_width
    resized_grayscale_image = original_image.resize((output_width, output_height)).convert('L')
    chars = [char_lut[lum * len(char_lut) // 256] for lum in list(resized_grayscale_image.getdata())]
    rows = [[chars[y * output_width + x] for x in range(output_width)] for y in range(output_height)]
    return '\r\n'.join([''.join(row) for row in rows])

if __name__ == '__main__':
    print(to_ascii(Image.open(sys.argv[1])))
