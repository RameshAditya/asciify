from PIL import Image
import os
from pathlib import Path
import yaml  # pip install pyyaml

ASCII_CHARS = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']
ASCII_CHARS = ASCII_CHARS[::-1]

'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''


def resize(image, new_width):

    old_width, old_height = image.size
    aspect_ratio = float(old_height) / float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = new_width, new_height
    new_image = image.resize(new_dim)
    return new_image


'''
method gray_scalify():
    - takes an image as a parameter
    - returns the grayscale version of image
'''


def gray_scarify(image):
    return image.convert('L')


'''
method modify():
    - replaces every pixel with a character whose intensity is similar
'''


def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value // buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)


'''
method do():
    - does all the work by calling all the above functions
'''


def do(image, new_width):
    image = resize(image, new_width)
    image = gray_scarify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    # Construct the image from the character list
    new_image = [pixels[index:index + new_width] for index in range(0, len_pixels, new_width)]

    return '\n'.join(new_image)


'''
method runner():
    - takes as parameter the image path and runs the above code
    - handles exceptions as well
    - provides alternative output options
'''


def runner(src_img_path: Path, output_path: Path, new_width: int):
    try:
        image = Image.open(src_img_path)
    except FileNotFoundError as e:
        print(f"Unable to find image in. {str(e)}")
        return
    image = do(image, new_width)

    # To print on console
    print(image)

    # Else, to write into a file
    # Note: This text file will be created by default under
    #       the same directory as this python file,
    #       NOT in the directory from where the image is pulled.
    with open(str(output_path), 'w') as f:
        f.write(image)
    os.startfile(output_path)


'''
method main():
    - reads input from console
    - profit
'''


def load_setting_from_config() -> tuple:
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    input_dict = config.get(Path(__file__).stem.upper())
    src_img_path = input_dict['SRC_IMG_PATH']
    download_dir = Path('./temp')
    os.makedirs(download_dir, exist_ok=True)
    if src_img_path.startswith('http://') or src_img_path.startswith('https://'):
        img_path = download_dir.joinpath(Path(src_img_path).name)
        urllib.request.urlretrieve(src_img_path, img_path)
        input_dict['SRC_IMG_PATH'] = img_path
    else:
        input_dict['SRC_IMG_PATH'] = Path(input_dict['SRC_IMG_PATH'])
    return input_dict['SRC_IMG_PATH'], Path(input_dict['OUTPUT_PATH']), input_dict.get('NEW_WIDTH', 100)


if __name__ == '__main__':
    import urllib.request
    _src_img_path, _output_path, _new_width = load_setting_from_config()
    runner(_src_img_path, _output_path, _new_width)
