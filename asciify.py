from PIL import Image

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
ASCII_CHARS = ASCII_CHARS[::-1]

'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''
def resize(image, new_width=100):
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image
'''
method grayscalify():
    - takes an image as a parameter
    - returns the grayscale version of image
'''
def grayscalify(image):
    return image.convert('L')

'''
method modify():
    - replaces every pixel with a character whose intensity is similar
'''
def modify(image, buckets=25):
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)

'''
method do():
    - does all the work by calling all the above functions
'''
def do(image, new_width=100):
    image = resize(image)
    image = grayscalify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    # Construct the image from the character list
    new_image = [pixels[index:index+new_width] for index in range(0, len_pixels, new_width)]

    return '\n'.join(new_image)

'''
method runner():
    - takes as parameter the image path and runs the above code
    - handles exceptions as well
    - provides alternative output options
'''
def runner(img_path, save_path):
    image = None
    try:
        image = Image.open(img_path)
    except Exception:
        print("Unable to find image in", img_path)
        #print(e)
        return
    image = do(image)

    # To print on console
    print(image)

    # Else, to write into a file
    # Note: This text file will be created by default under
    #       the same directory as this python file,
    #       NOT in the directory from where the image is pulled.
    try:
        with open(save_path, 'w') as f:
            f.write(image)
    except FileNotFoundError:
        print(f"\nNo such directory to save output to: {save_path}")
        print("Check for typos/mistakes or create the directories beforehand")
        return
    except PermissionError:
        print(f"\nPermission error when saving output to {save_path}")
        print("Ensure that sufficient permissions are given, or that a folder does not have the same name")
        return

'''
method main():
    - reads input from console
    - profit
'''
if __name__ == '__main__':
    import sys
    import urllib.request
    import urllib.error
    import os
    
    # No arguments given
    if len(sys.argv) == 1:
        print("Relative/absolute path or URL of image must be provided")
        print("usage: python asciify.py <image> [save_location]")
        sys.exit()
    
    # Find name of image file
    img_name = sys.argv[1][sys.argv[1].rfind("/") + 1:sys.argv[1].rfind(".")]
    
    if sys.argv[1].startswith('http://') or sys.argv[1].startswith('https://'):
        try:
            urllib.request.urlretrieve(sys.argv[1], img_name + ".jpg")
        except urllib.error.HTTPError:
            print("Invalid URL:", sys.argv[1])
            sys.exit()
        img_path = img_name + ".jpg"
    else:
        img_path = sys.argv[1]

    if len(sys.argv) > 2:
        if sys.argv[2].endswith(".txt"):
            save_path = sys.argv[2]
        else:
            save_path = sys.argv[2] + os.path.sep + img_name + "-asciified.txt"
    else:
        save_path = img_name + "-asciified.txt"

    runner(img_path, save_path)
