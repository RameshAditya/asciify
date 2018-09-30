from PIL import Image
from PIL import ImageDraw, ImageFont

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']
ASCII_CHARS = ASCII_CHARS[::-1]

'''
method resize():
    - takes as parameters the image, and the final width
    - resizes the image into the final width while maintaining aspect ratio
'''
def resize(image, new_width=100):
    (old_width, old_height) = image.size
    # print("original size:" + str((old_width, old_height)))
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    # print("new size:" + str(new_dim))
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
    image = resize(image,new_width)
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
def runner(path,revert_colors = False,pixel_per_line=100):
    
    if revert_colors:
        global ASCII_CHARS
        ASCII_CHARS = ASCII_CHARS[::-1]

    image = None
    try:
        image = Image.open(path)
        name = get_name_from_path(path)
    except Exception:
        print("Unable to find image in",path)
        #print(e)
        return
    image = do(image,pixel_per_line)

    # To print on console
    # print(image)

    # Else, to write into a file
    # Note: This text file will be created by default under
    #       the same directory as this python file,
    #       NOT in the directory from where the image is pulled.
    f = open(name + '.txt','w')
    f.write(image)
    f.close()

    create_img(name)

def create_img(name):
    # weird to open a file right after closing but it was to keep the
    # logic of the old script working 
    s=[]
    f= open(name + ".txt","r")
    for line in f:
        s.append(line)
    f.close()

    xlines = len(s[0])
    ylines = len(s)

    # must be a monospaced font 
    font = 'Anonymous.ttf'
    font_size_to_draw = 12

    # how much space each ascii code takes
    font_pixel_width = 10
    font_pixel_height = 10

    image_size_x = (xlines-1)*(font_pixel_width)
    image_size_y = (ylines)*(font_pixel_height)

    img = Image.new('RGB',(image_size_x,image_size_y) , color = (0, 0, 0))
    
    # draw background
    d = ImageDraw.Draw(img)

    fnt = ImageFont.truetype(font, font_size_to_draw)
    for y in range(len(s)):
        for x in range(len(s[y])):
            d.text((x*font_pixel_width,y*font_pixel_height), s[y][x], font=fnt, fill=(255, 255, 255))

    img.save(name + '_ascii.png')

def get_name_from_path(path):
    import os
    name = os.path.basename(path)
    name = name.split(".")
    return name[0]

'''
method main():
    - reads input from console
    - profit
'''
if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    runner(path)
