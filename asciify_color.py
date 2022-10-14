from PIL import Image
import copy

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
method colorize(): 
    - adds colors to the characters from the modify method. The initial string of pixels in the 
    modify method (which creates an array of characters) is the same length as the pixel rgb color array. We for loop 
    through the modify method's character array and assign those characters to colors from the original image, 
    and then append them to seperate lines 100 characters long to print later.
'''
def colorize(colorful_image, intensity_characters):
    initial_pixels = list(colorful_image.getdata())
    colorful_pixels = []
    temp_line = []
    for i, character in zip(initial_pixels,intensity_characters):
        new_character = f"\033[38;2;{i[0]};{i[1]};{i[2]}m{character}\033[0m"
        temp_line.append(new_character)
        if len(temp_line) > 99:
            temp_line_str = ''.join(temp_line)
            colorful_pixels.append(temp_line_str)
            temp_line = []
    return colorful_pixels


'''
method do():
    - does all the work by calling all the above functions
'''
def do(image):
    image = resize(image)
    full_color = copy.deepcopy(image)
    image_greyscale = grayscalify(image)

    pixels = modify(image_greyscale)
    colorful_pixels = colorize(full_color,pixels)

    # Construct the image from the line list
    new_image = '\n'.join(colorful_pixels)

    return new_image

'''
method runner():
    - takes as parameter the image path and runs the above code
    - handles exceptions as well
    - provides alternative output options
'''
def runner(path):
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        #print(e)
        return
    image = do(image)

    # To print on console
    print(image)

    # Else, to write into a file
    # Note: This text file will be created by default under
    #       the same directory as this python file,
    #       NOT in the directory from where the image is pulled.
    f = open('img_color.txt','w')
    f.write(image)
    f.close()

'''
method main():
    - reads input from console
    - profit
'''
if __name__ == '__main__':
    import sys
    import urllib.request
    if sys.argv[1].startswith('http://') or sys.argv[1].startswith('https://'):
        urllib.request.urlretrieve(sys.argv[1], "asciify.jpg")
        path = "asciify.jpg"
    else:
        path = sys.argv[1]
    runner(path)
